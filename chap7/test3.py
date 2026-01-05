from z3 import *
from z3.z3 import Bool, Implies, Not, And, Or, Solver, sat

# 1. 定义布尔变量（A-E 对应之前的逻辑符号）
A = Bool('A')  # 神话
B = Bool('B')  # 不朽
C = Bool('C')  # 哺乳动物
D = Bool('D')  # 长角
E = Bool('E')  # 有魔力

# 2. 定义逻辑约束（对应之前修正后的 4 个条件）
# 条件1：A→B（如果是神话，则不朽）
cond1 = Implies(A, B)
# 条件2：~A→(~B ∧ C)（如果不是神话，则非不朽且是哺乳动物）
cond2 = Implies(Not(A), And(Not(B), C))
# 条件3：(B∨C)→D（如果不朽或哺乳动物，则长角）
cond3 = Implies(Or(B, C), D)
# 条件4：D→E（如果长角，则有魔力）
cond4 = Implies(D, E)

# 3. 创建求解器并添加所有约束
s = Solver()
s.add(cond1, cond2, cond3, cond4)

# 4. 检查是否存在 A 为真的模型
print("检查 A 为真的情况：")
s.push()  # 保存当前状态
s.add(A)  # 额外添加约束 A=True
if s.check() == sat:
    print("可满足，模型：")
    print(s.model())
else:
    print("不可满足")
s.pop()  # 恢复状态，移除 A=True 的约束

# 5. 检查是否存在 A 为假的模型
print("\n检查 A 为假的情况：")
s.push()
s.add(Not(A))  # 额外添加约束 A=False
if s.check() == sat:
    print("可满足，模型：")
    print(s.model())
else:
    print("不可满足")
s.pop()
