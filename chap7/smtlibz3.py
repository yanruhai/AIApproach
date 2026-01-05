from z3.z3 import Solver, parse_smt2_string, sat, And

# 定义多个独立的 SMT-LIB 公式（每个公式对应不同任务）
# 公式1：任务A - 判定 (a∨b) ∧ ¬a 是否可满足
formula1_smt = """
(set-logic BOOL) 
(declare-const a Bool)
(declare-const b Bool)
(assert (and (or a b) (not a)))
"""
#(set-logic BOOL) 意思是处理布尔逻辑式子
# 公式2：任务B - 判定 (c→d) ∧ d 是否可满足
formula2_smt = """
(set-logic BOOL)  
(declare-const c Bool)
(declare-const d Bool)
(assert (and (implies c d) d))
"""

# 公式3：任务C - 验证 (x∧y)∨(¬x∧¬y) 是否为重言式（恒真）
# 补充说明：此公式实际是“x↔y”（等价），并非重言式，这里保留原逻辑用于演示
formula3_smt = """
(set-logic BOOL)  
(declare-const x Bool)
(declare-const y Bool)
(assert (not (or (and x y) (and (not x) (not y)))))  ; 否定等价公式
"""


# 定义通用求解函数（优化输出+补充逻辑说明）
def solve_formula(smt_lib_str, task_desc):
    """处理单个公式的求解任务"""
    s = Solver()  # 每个公式创建独立求解器（完全隔离）

    # 解析 SMT-LIB 并添加约束
    assertions = parse_smt2_string(smt_lib_str)
    if assertions:
        s.add(*assertions)

    # 执行求解
    result = s.check()
    print(f"=== 任务：{task_desc} ===")
    print(f"可满足性：{result}")

    # 格式化输出模型
    if result == sat:
        model = s.model()
        # 优化模型输出格式（去掉方括号，更易读）
        model_str = ", ".join([f"{var.name()} = {model[var]}" for var in model.decls()])
        print(f"模型：{model_str}")
        # 针对公式3补充逻辑说明
        if "重言式" in task_desc:
            print("结论：原公式不是重言式（存在使公式为假的赋值）\n")
        else:
            print("\n")
    else:
        if "重言式" in task_desc:
            print("结论：原公式是重言式（恒真）\n")
        else:
            print("无解（公式不可满足/恒假）\n")


# 执行不同任务
solve_formula(formula1_smt, "判定 (a∨b) ∧ ¬a 的可满足性")
solve_formula(formula2_smt, "判定 (c→d) ∧ d 的可满足性")
solve_formula(formula3_smt, "验证 (x∧y)∨(¬x∧¬y) 是否为重言式")

# 额外补充：演示真正的重言式验证（如 x∨¬x）
formula4_smt = """
(set-logic BOOL)
(declare-const x Bool)
(assert (not (or x (not x))))  ; 否定重言式 x∨¬x
"""
solve_formula(formula4_smt, "验证 x∨¬x 是否为重言式")