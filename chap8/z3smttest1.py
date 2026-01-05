from z3.z3 import *

solver = Solver()

# SMT-LIB字符串需要包含完整的变量声明
smtlib_constraint = """
(declare-const x Int)
(declare-const y Int)
(assert (> x 0))
(assert (> y 0))
(assert (= (+ (* 2 x) y) 30))
"""

# 将SMT-LIB字符串添加到求解器
solver.from_string(smtlib_constraint)

# 检查可满足性
if solver.check() == sat:
    model = solver.model()
    # 从模型中获取值
    print(f"x = {model[0]}")
    print(f"y = {model[1]}")
    # 或者遍历所有声明
    for decl in model:
        print(f"{decl.name()} = {model[decl]}")
else:
    print("无解")