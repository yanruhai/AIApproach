from z3.z3 import *

Person = DeclareSort('Person')

# 声明谓词和函数
Female = Function('Female', Person, BoolSort())
Male = Function('Male', Person, BoolSort())
Parent = Function('Parent', Person, Person, BoolSort())
Mother = Function('Mother', Person,  Person,BoolSort())
Father=Function('Father', Person,  Person,BoolSort())#函数
Husband= Function('Husband', Person, Person, BoolSort())#
Wife= Function('Wife', Person, Person, BoolSort())#
Sibling= Function('Sibling', Person, Person, BoolSort())#
Child = Function('Child', Person, Person, BoolSort())
Spouse = Function('Spouse', Person, Person, BoolSort())
Grandparent = Function('Grandparent', Person, Person, BoolSort())
Grandchild = Function('Grandchild', Person, Person, BoolSort())


solver = Solver()

# 启用跟踪
solver.set(unsat_core=True)
# 1. 男性和女性互斥
x = Const('x', Person)
malenotfemale_def=ForAll([x], Male(x) == Not(Female(x)))
solver.assert_and_track(malenotfemale_def,Bool('malnotfemale_def'))

# 2. 父母和孩子是逆关系
p, c = Consts('p c', Person)
parentnotchild=ForAll([p, c], Implies(Parent(p, c),And(Child(c, p),c!=p)))
solver.assert_and_track(parentnotchild,Bool('parentnotchild_def'))

child_def=ForAll([p, c], Child(c,p)==And(Parent(p,c),c!=p))
solver.assert_and_track(child_def,Bool('child_def'))

# 3. 祖父母定义
g = Const('g', Person)
MiddleMan = Function('MiddleMan', Person, Person, Person)

'''grandparent_def=ForAll([g, c],
    And(Grandparent(g, c) == Exists([p], And(Parent(g, p), Parent(p, c),Not(g==c)))))'''
grandparent_def=ForAll([g, c],
        Implies(Grandparent(g, c), And(Parent(g, MiddleMan(g, c)), Parent(MiddleMan(g, c), c))))

solver.assert_and_track(grandparent_def,Bool("grandparent_def"))

# 4. 孙辈定义
x, y,z = Consts('x y z', Person)

grandchild_def=ForAll([x, y],
                  Implies(Grandchild(x, y) , And(Child(x, MiddleMan(x,y)),
                                            Child(MiddleMan(x,y),y),~(Grandchild(y,x)),x!=y,Grandparent(y,x))))
solver.assert_and_track(grandchild_def,Bool('grandchild_def'))
'''solver.add(ForAll([x, y],
                  Grandchild(x, y) == Exists([z], And(Child(x, z), Child(z, y)))))'''

mother_def=ForAll([x,y],Mother(x,y)==And(Female(y),Parent(x,y),x!=y))
solver.assert_and_track(mother_def,Bool("mother_def"))#Mother
father_def=ForAll([x,y],Father(x,y)==And(Male(y),Parent(x,y),x!=y))
solver.assert_and_track(father_def,Bool("father_def"))#father
husband_def=ForAll([x,y],Husband(x,y)==And(Male(x),Spouse(x,y)))
solver.assert_and_track(husband_def,Bool("husband_def"))#husband
wife_def=ForAll([x,y],Wife(x,y)==And(Female(x),Spouse(x,y)))
solver.assert_and_track(wife_def,Bool('wife_def'))#wife
'''
sibling_def=ForAll([x,y],Sibling(x,y)==And(Not(x==y),Exists([z],And(Parent(z,x),Parent(z,y)))))
solver.assert_and_track(sibling_def,Bool('sibling_def'))#sibling
'''

# 输入两个孩子，返回那个“共同的父母”
CommonParent = Function('CommonParent', Person, Person, Person)

# 2. 将等价关系拆解或重构为中间人形式
# 这样 Z3 在处理 Sibling 时，会直接指向一个确定的占位符，而不是盲目搜索
sibling_def = ForAll([x, y],
    Sibling(x, y) == And(
        x != y,
        Parent(CommonParent(x, y), x),
        Parent(CommonParent(x, y), y)
    )
)

# 3. 使用 assert_and_track
solver.assert_and_track(sibling_def, Bool('tp_sibling_def'))
# 添加具体的人和关系
a1, b1, c1,d1 = Consts('a1 b1 c1 d1', Person)
solver.add(Distinct(c1,a1,b1,d1))
# 添加事实
solver.assert_and_track(And(Grandparent(a1, c1),Grandparent(a1,d1)) ,Bool("gradpapa_a1c1"))
solver.assert_and_track(Mother(a1,b1),Bool("mother_a1_b1"))
solver.assert_and_track(Father(b1,c1),"father_b1_c1")
solver.assert_and_track(Father(b1,d1),"father_b1_d1")
solver.assert_and_track(Parent(a1,b1),Bool('parent_a1_b1'))
solver.assert_and_track(Parent(b1,c1),Bool('parent_b1_c1'))
solver.assert_and_track(Parent(b1,d1),Bool('parent_b1_d1'))


print("开始求解...")
result = solver.check()
print(f"结果: {result}")

if result == sat:
    m = solver.model()

    # 查询特定关系
    print(f"\n查询Parent(a, c): {m.evaluate(Parent(a1, a1))}")

    # 显示所有关系
    print("\n所有关系:")
    persons = [a1, b1, c1,d1]
    names = ['a1', 'b1', 'c1','d1']

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

elif result==unsat:
    print("矛盾！以下是导致 unsat 的核心断言：")
    core = solver.unsat_core()
    for c in core:
        print(f" - {c}")  # 打印名字
elif result == unknown:#设置超时（毫秒）
                    #s.set("timeout", 100)  # 100毫秒超时
    print("求解器超时或无法确定")
else:
    print("无解")