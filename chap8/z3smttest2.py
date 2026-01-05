from z3.z3 import *

solver = Solver()

# SMT-LIB字符串（包含完整的变量声明）
smtlib_constraint = """
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)

; 添加布尔逻辑约束
(assert (or p q))
(assert (=> p r))
(assert (not (and q r)))
(assert (xor p q))

(check-sat)
(get-model)
"""

# 解析并求解
result = parse_smt2_string(smtlib_constraint)
print("SMT-LIB结果:")
print(result)

# 或者使用solver.from_string（只添加约束，不包含check-sat）
solver2 = Solver()
constraints_only = """
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
(assert (or p q))
(assert (=> p r))
(assert (not (and q r)))
(assert (xor p q))
"""
solver2.from_string(constraints_only)

if solver2.check() == sat:
    model = solver2.model()
    print("\n模型值:")
    for decl in model:
        print(f"{decl.name()} = {model[decl]}")