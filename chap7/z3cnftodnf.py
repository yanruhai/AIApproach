from z3 import *
from z3.z3 import *


# ---------------------- 1. 解析 CNF（DIMACS 格式） ----------------------
def parse_dimacs_cnf(cnf_str):
    """
    解析 DIMACS 格式的 CNF 字符串，返回 Z3 公式和变量映射
    """
    lines = [line.strip() for line in cnf_str.split('\n') if line.strip() and not line.startswith('c')]
    header = lines[0].split()
    assert header[0] == 'p' and header[1] == 'cnf', "非 DIMACS CNF 格式"
    num_vars = int(header[2])
    num_clauses = int(header[3])

    vars_map = {i: Bool(f"x{i}") for i in range(1, num_vars + 1)}
    clauses = []

    for line in lines[1:num_clauses + 1]:
        literals = [int(x) for x in line.split() if x != '0']
        clause = []
        for lit in literals:
            var = vars_map[abs(lit)]
            clause.append(var if lit > 0 else Not(var))
        clauses.append(Or(*clause))

    cnf_formula = And(*clauses)
    return cnf_formula, vars_map


# ---------------------- 2. 枚举 CNF 的所有满足解 ----------------------
def get_all_solutions(cnf_formula, vars_map):
    """枚举 CNF 的所有满足解，返回解列表（每个解是 {变量: 布尔值}）"""
    s = Solver()
    s.add(cnf_formula)
    solutions = []

    while s.check() == sat:
        model = s.model()
        # 提取当前解的变量取值
        solution = {}
        for var_id in sorted(vars_map.keys()):
            var = vars_map[var_id]
            # 使用 eval_in_model 来获取变量的实际值
            try:
                val = model.eval(var, model_completion=True)
                if is_true(val):
                    solution[var] = True
                elif is_false(val):
                    solution[var] = False
                else:
                    # 如果仍然无法确定，尝试简化
                    simplified = simplify(var)
                    if is_true(simplified):
                        solution[var] = True
                    elif is_false(simplified):
                        solution[var] = False
                    else:
                        # 默认为True（自由变量可以选择任意值）
                        solution[var] = True
            except:
                # 如果出错，默认为True
                solution[var] = True

        solutions.append(solution)

        # 添加排除当前解的约束
        # 构建阻止当前具体赋值的约束
        block_clauses = []
        for var, val in solution.items():
            if val is True:
                block_clauses.append(Not(var))
            elif val is False:
                block_clauses.append(var)

        if block_clauses:
            s.add(Or(*block_clauses))
        else:
            break  # 没有更多解了

    return solutions


# ---------------------- 3. 获取所有变量的完整赋值 ----------------------
def get_all_solutions_complete(cnf_formula, vars_map):
    """更可靠的解决方案：确保每个变量都有明确赋值"""
    s = Solver()
    s.add(cnf_formula)
    solutions = []

    # 为每个变量创建辅助变量，确保它们都有赋值
    var_list = [vars_map[i] for i in sorted(vars_map.keys())]

    while s.check() == sat:
        model = s.model()
        solution = {}

        # 获取每个变量的值
        for var in var_list:
            # 强制模型为变量赋值
            val = model.eval(var, model_completion=True)
            if is_true(val):
                solution[var] = True
            else:
                # 如果模型返回的不是True，则为False
                solution[var] = False

        solutions.append(solution)

        # 构建阻止当前解的约束
        block = []
        for var, val in solution.items():
            if val:
                block.append(Not(var))
            else:
                block.append(var)

        s.add(Or(*block))

    return solutions


# ---------------------- 4. 将解转换为 DNF 公式 ----------------------
def solutions_to_dnf(solutions):
    """将解列表转换为 DNF 公式（每个解是一个合取项，所有项析取）"""
    if not solutions:
        return False  # 无解的 CNF 等价于 False

    dnf_terms = []
    for sol in solutions:
        term = []
        for var, val in sol.items():
            if val is True:
                term.append(var)
            elif val is False:
                term.append(Not(var))
        if term:  # 确保项非空
            dnf_terms.append(And(*term))

    if not dnf_terms:
        return False

    dnf_formula = Or(*dnf_terms)
    return dnf_formula


# ---------------------- 5. 辅助：打印 DNF（易读格式） ----------------------
def print_dnf(dnf_formula, vars_map):
    """打印 DNF 的易读字符串"""
    if dnf_formula == False:
        print("DNF: False（CNF 无解）")
        return

    # 递归解析 DNF 结构
    def term_to_str(term):
        """将合取项转为字符串"""
        literals = []
        if term.decl().name() == 'and':
            for child in term.children():
                literals.append(literal_to_str(child))
        else:
            literals.append(literal_to_str(term))
        return " ∧ ".join(literals)

    def literal_to_str(lit):
        """将文字转为字符串"""
        if lit.decl().name() == 'not':
            var = lit.children()[0]
            var_id = [k for k, v in vars_map.items() if v == var][0]
            return f"¬x{var_id}"
        else:
            var_id = [k for k, v in vars_map.items() if v == lit][0]
            return f"x{var_id}"

    # 解析 DNF 顶层的 Or
    terms = []
    if dnf_formula.decl().name() == 'or':
        for child in dnf_formula.children():
            terms.append(term_to_str(child))
    else:
        terms.append(term_to_str(dnf_formula))

    print(f"DNF: {' ∨ '.join(terms)}")


# ---------------------- 6. 验证 DNF 的正确性 ----------------------
def verify_dnf(cnf_formula, dnf_formula):
    """验证 CNF 和 DNF 是否等价"""
    s = Solver()
    # 检查 CNF → DNF 和 DNF → CNF 是否都成立
    s.add(Not(Implies(cnf_formula, dnf_formula)))
    if s.check() == unsat:
        s2 = Solver()
        s2.add(Not(Implies(dnf_formula, cnf_formula)))
        if s2.check() == unsat:
            return True
    return False


# ---------------------- 测试：CNF 转 DNF ----------------------
if __name__ == "__main__":
    # 示例 CNF（DIMACS 格式）：(x1∨¬x2∨x3) ∧ (¬x1∨x2)
    cnf_dimacs = """
    p cnf 3 2
    1 -2 3 0
    -1 2 0
    """

    print("=" * 60)
    print("CNF 转 DNF 转换器")
    print("=" * 60)

    # 步骤1：解析 CNF
    cnf_formula, vars_map = parse_dimacs_cnf(cnf_dimacs)
    print(f"\n原始 CNF 公式：{cnf_formula}")

    # 列出所有变量
    print(f"变量：{[f'x{i}' for i in sorted(vars_map.keys())]}")

    # 步骤2：使用改进的方法枚举所有解
    print("\n正在枚举所有解...")
    solutions = get_all_solutions_complete(cnf_formula, vars_map)

    print(f"\n找到 {len(solutions)} 个解：")
    for i, sol in enumerate(solutions, 1):
        sol_str = {}
        for var, val in sol.items():
            var_id = [k for k, v in vars_map.items() if v == var][0]
            sol_str[f"x{var_id}"] = val
        print(f"解 {i}: {sol_str}")

    # 步骤3：转换为 DNF
    dnf_formula = solutions_to_dnf(solutions)
    print("\n等价 DNF 公式：")
    print_dnf(dnf_formula, vars_map)

    # 验证等价性
    print("\n验证 CNF 和 DNF 是否等价：")
    if verify_dnf(cnf_formula, dnf_formula):
        print("✓ CNF 和 DNF 逻辑等价")
    else:
        print("✗ CNF 和 DNF 不等价")

    # 测试一个具体的赋值
    print("\n测试一个具体赋值：x1=True, x2=False, x3=True")
    test_solver = Solver()
    test_solver.add(cnf_formula)
    test_solver.add(vars_map[1] == True)
    test_solver.add(vars_map[2] == False)
    test_solver.add(vars_map[3] == True)
    if test_solver.check() == sat:
        print("CNF: 该赋值可满足")
    else:
        print("CNF: 该赋值不可满足")

    test_solver2 = Solver()
    test_solver2.add(dnf_formula)
    test_solver2.add(vars_map[1] == True)
    test_solver2.add(vars_map[2] == False)
    test_solver2.add(vars_map[3] == True)
    if test_solver2.check() == sat:
        print("DNF: 该赋值可满足")
    else:
        print("DNF: 该赋值不可满足")