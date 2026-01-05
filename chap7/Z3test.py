from z3 import *
from z3.z3 import *

# 1. 创建单个布尔变量（命题变元）
p = Bool('p')
q = Bool('q')
r = Bool('r')

# 2. 批量创建布尔变量（适合多变量场景）
# 方式1：逐个指定名称
a, b, c = Bools('a b c')
# 方式2：列表推导式（比如创建10个变量：x0~x9）
xs = [Bool(f'x{i}') for i in range(10)]

# 1. 否定：¬p
f1 = Not(p)

# 2. 合取：p ∧ q ∧ r
f2 = And(p, q, r)
# 也可传入列表（适合动态生成的子式）
f2_list = And([p, q, r])

# 3. 析取：p ∨ q
f3 = Or(p, q)

# 4. 蕴含：p → q（等价于 ¬p ∨ q）
f4 = Implies(p, q)
# 手动验证等价性：Implies(p,q) == Not(p) | q
f4_eq = f4 == (Not(p) | q)

# 5. 等价：p ↔ q（等价于 (p→q) ∧ (q→p)）
f5 = p == q  # 或 Eq(p, q)
f5_alt = And(Implies(p, q), Implies(q, p))  # 等价写法

s=Solver()
all_solutions = []
s.add(f5_alt)
while s.check()==sat:
    model = s.model()

    # 提取解的具体值（封装成字典，方便查看）
    solution = {
        "x": model[x].as_long(),  # 整数转Python原生int
        "y": model[y].as_long()
    }
    all_solutions.append(solution)

    # 关键：添加“排除当前解”的约束，避免重复找到同一个解
    # 构造“x≠当前x值 OR y≠当前y值”的否定约束（即 x==当前x ∧ y==当前y 不成立）
    block = []
    for var in model:
        # var 是模型中的变量（z3.ArithRef类型）
        var_value = model[var]
        block.append(var != var_value)
    s.add(Or(block))  # 添加排除约束

# 6. 异或：p ⊕ q（等价于 (p∨q) ∧ ¬(p∧q)）
f6 = Xor(p, q)

# 7. 复杂组合公式：(p ∧ q) → (¬r ∨ q)
f7 = Implies(And(p, q), Or(Not(r), q))

# 8. 条件公式：如果p为真则返回q，否则返回r
f8 = If(p, q, r)

p, q, r = Bools('p q r')

# 示例公式：(p ∧ q) ∨ (p → r)
# 先把蕴含式转成基础运算符：p→r ≡ ¬p ∨ r
f = Or(And(p, q), Implies(p, r))
sol=Solver()
sol.add(f)
if sol.check()==sat:
    print(sol.model())