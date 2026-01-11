from z3.z3 import *

Person = DeclareSort('Person')

# 声明谓词和函数
Female = Function('Female', Person, BoolSort())
Male = Function('Male', Person, BoolSort())
Parent = Function('Parent', Person, Person, BoolSort())
Child = Function('Child', Person, Person, BoolSort())
Spouse = Function('Spouse', Person, Person, BoolSort())
Grandparent = Function('Grandparent', Person, Person, BoolSort())
Grandchild = Function('Grandchild', Person, Person, BoolSort())

solver = Solver()

# 1. 男性和女性互斥
x = Const('x', Person)
solver.add(ForAll([x], Male(x) == Not(Female(x))))

# 2. 父母和孩子是逆关系
p, c = Consts('p c', Person)
solver.add(ForAll([p, c], Parent(p, c) == Child(c, p)))

# 3. 祖父母定义
g = Const('g', Person)

solver.add(ForAll([g, c],
    And((Grandparent(g, c) == Exists([p], And(Parent(g, p), Parent(p, c)))),Not(g==c))))

# 4. 孙辈定义
x, y,z = Consts('x y z', Person)
solver.add(ForAll([x, y],
                  Grandchild(x, y) == Exists([z], And(Child(x, z), Child(z, y)))
                  ))


# 添加具体的人和关系
a1, b1, c1 = Consts('a1 b1 c1', Person)
solver.add(Distinct(c1,a1,b1))
# 添加事实
solver.add(Grandchild(a1, b1))  # a是b的孙辈
solver.add(Parent(b1,c1))  # b是c的父母

print("开始求解...")
result = solver.check()
print(f"结果: {result}")

if result == sat:
    m = solver.model()

    # 查询特定关系
    print(f"\n查询Parent(a, c): {m.evaluate(Parent(a1, a1))}")

    # 显示所有关系
    print("\n所有关系:")
    persons = [a1, b1, c1]
    names = ['a1', 'b1', 'c1']

    for i in range(len(persons)):
        for j in range(len(persons)):
            if i != j:  # 使用索引比较，而不是直接比较符号
                p1, p2 = persons[i], persons[j]
                parent_val = m.evaluate(Parent(p1, p2))
                child_val = m.evaluate(Child(p1, p2))
                grandchild_val = m.evaluate(Grandchild(p1, p2))

                if is_true(parent_val):
                    print(f"{names[i]} 是 {names[j]} 的父母")
                if is_true(child_val):
                    print(f"{names[i]} 是 {names[j]} 的孩子")
                if is_true(grandchild_val):
                    print(f"{names[i]} 是 {names[j]} 的孙辈")

elif result == unknown:#设置超时（毫秒）
                    #s.set("timeout", 100)  # 100毫秒超时
    print("求解器超时或无法确定")
else:
    print("无解")