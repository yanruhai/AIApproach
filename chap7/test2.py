from sympy import symbols, Implies, And, Or, Not, init_printing
from sympy.printing.latex import latex

init_printing(use_unicode=True)

p, q, r = symbols('p q r')

# 创建表达式
expr1 = Implies(p, q)
expr2 = And(p, Or(q, r))
expr3 = Or(Not(p), q)

# 获取 LaTeX 代码
latex1 = latex(expr1)
latex2 = latex(expr2)
latex3 = latex(expr3)

print("LaTeX 代码:")
print(f"p → q: {latex1}")
print(f"p ∧ (q ∨ r): {latex2}")
print(f"¬p ∨ q: {latex3}")

# 在 Jupyter Notebook 中直接显示
# expr1
# expr2
# expr3