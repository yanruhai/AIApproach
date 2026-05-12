from z3 import *

Person = DeclareSort('Person')

# 声明谓词和函数
Female = Function('Female', Person, BoolSort())
Male = Function('Male', Person, BoolSort())
Parent = Function('Parent', Person, Person, BoolSort())
Child = Function('Child', Person, Person, BoolSort())
Grandparent = Function('Grandparent', Person, Person, BoolSort())
# Grandchild 暂时不定义（因为你没用到）

solver = Solver()

# 1. 男性和女性互斥（可选）
x = Const('x', Person)
solver.add(ForAll([x], Male(x) == Not(Female(x))))

# 2. 父母和孩子是逆关系
p, c, g= Consts('p c g', Person)
solver.add(ForAll([p, c], Parent(p, c) == Child(c, p)))

# 3. 祖父母定义（最关键）
solver.add(ForAll([g, c, p],
    Grandparent(g, c) == Exists([p], And(Parent(g, p), Parent(p, c)))
))

# 可选：不允许自己是自己的祖父母
solver.add(ForAll([g, c], Implies(Grandparent(g, c), Not(g == c))))

# 人物
a1, b1, c1, d1 = Consts('a1 b1 c1 d1', Person)
solver.add(Distinct(a1, b1, c1, d1))

# 事实（这些关系完全一致）
solver.add(Parent(a1, b1))           # a1 → b1
solver.add(Parent(b1, c1))           # b1 → c1
solver.add(Parent(b1, d1))           # b1 → d1

# 这两条其实可以不加，因为可以从上面推出来（但加了也没问题）
solver.add(Grandparent(a1, c1))
solver.add(Grandparent(a1, d1))

print("开始求解...")
result = solver.check()
print(f"结果: {result}")

if result == sat:
    m = solver.model()
    print("\n找到模型！以下是关键关系：\n")

    # 显示父子关系
    print("Parent 关系：")
    print(f"Parent(a1, b1) = {m.evaluate(Parent(a1, b1))}")
    print(f"Parent(b1, c1) = {m.evaluate(Parent(b1, c1))}")
    print(f"Parent(b1, d1) = {m.evaluate(Parent(b1, d1))}")

    # 显示祖孙关系
    print("\nGrandparent 关系：")
    print(f"Grandparent(a1, c1) = {m.evaluate(Grandparent(a1, c1))}")
    print(f"Grandparent(a1, d1) = {m.evaluate(Grandparent(a1, d1))}")

    # 如果你想看 Child（逆关系）
    print("\nChild 关系（自动推导）：")
    print(f"Child(b1, a1) = {m.evaluate(Child(b1, a1))}")
    print(f"Child(c1, b1) = {m.evaluate(Child(c1, b1))}")
    print(f"Child(d1, b1) = {m.evaluate(Child(d1, b1))}")

else:
    print("无解（unsat）")
    print("如果还是 unsat，请检查是否还有其他断言残留")