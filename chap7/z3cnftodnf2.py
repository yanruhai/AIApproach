from z3.z3 import *


def parse_dimacs_cnf(cnf_str):
    lines = [line.strip() for line in cnf_str.split('\n') if line.strip() and not line.startswith('c')]
    header = lines[0].split()
    num_vars = int(header[2])

    vars_map = {i: Bool(f"x{i}") for i in range(1, num_vars + 1)}
    clauses = []

    for line in lines[1:]:
        nums = list(map(int, line.split()))
        if nums and nums[-1] == 0:
            nums = nums[:-1]
        clause = [vars_map[abs(lit)] if lit > 0 else Not(vars_map[abs(lit)]) for lit in nums]
        if clause:
            clauses.append(Or(*clause))

    return And(*clauses), vars_map


def get_all_solutions(cnf_formula, vars_map):
    s = Solver()
    s.add(cnf_formula)
    solutions = []

    while s.check() == sat:
        model = s.model()
        solution = {}

        # 关键修正：使用 model.eval() 获取变量值
        for var_id, var in vars_map.items():
            # model.eval(var) 返回具体值，然后判断
            val = model.eval(var)
            solution[var] = is_true(val)  # 直接返回Python bool

        solutions.append(solution)

        # 排除当前解
        block = [var != val for var, val in solution.items()]
        s.add(Or(*block))

    return solutions


def solutions_to_dnf(solutions):
    if not solutions:
        return False

    dnf_terms = []
    for sol in solutions:
        term = [var if val else Not(var) for var, val in sol.items()]
        dnf_terms.append(And(*term))

    return Or(*dnf_terms) if dnf_terms else False


def print_solutions(solutions, vars_map):
    for i, sol in enumerate(solutions, 1):
        sol_dict = {}
        for var_id, var in vars_map.items():
            val = sol[var]
            sol_dict[f"x{var_id}"] = val
        print(f"解{i}: {sol_dict}")


def print_dnf(dnf, vars_map):
    if dnf == False:
        print("False")
        return

    def lit_str(lit):
        if lit.decl().name() == 'not':
            var = lit.children()[0]
            var_id = [k for k, v in vars_map.items() if v == var][0]
            return f"¬x{var_id}"
        else:
            var_id = [k for k, v in vars_map.items() if v == lit][0]
            return f"x{var_id}"

    if dnf.decl().name() == 'or':
        terms = []
        for term in dnf.children():
            if term.decl().name() == 'and':
                lits = [lit_str(lit) for lit in term.children()]
                terms.append(" ∧ ".join(lits))
            else:
                terms.append(lit_str(term))
        print(" ∨ ".join(terms))
    else:
        print(lit_str(dnf))


# 测试
if __name__ == "__main__":
    cnf_dimacs = """
    p cnf 3 2
    1 -2 3 0
    -1 2 0
    """

    cnf, vars_map = parse_dimacs_cnf(cnf_dimacs)
    print(f"CNF: {cnf}")

    solutions = get_all_solutions(cnf, vars_map)
    print(f"\n找到 {len(solutions)} 个解:")
    print_solutions(solutions, vars_map)

    dnf = solutions_to_dnf(solutions)
    print("\n等价DNF:")
    print_dnf(dnf, vars_map)