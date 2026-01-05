from sympy import symbols, Implies, And, Or, Not, Equivalent
from sympy.printing.str import StrPrinter


class LogicPrinter(StrPrinter):
    def _print_Implies(self, expr):
        return f"({self._print(expr.args[0])} → {self._print(expr.args[1])})"

    def _print_And(self, expr):
        return f"({' ∧ '.join(self._print(arg) for arg in expr.args)})"

    def _print_Or(self, expr):
        return f"({' ∨ '.join(self._print(arg) for arg in expr.args)})"

    def _print_Not(self, expr):
        return f"¬{self._print(expr.args[0])}"

    def _print_Equivalent(self, expr):
        return f"({self._print(expr.args[0])} ↔ {self._print(expr.args[1])})"


def print_logic(expr):
    printer = LogicPrinter()
    return printer.doprint(expr)


# 使用示例
p, q, r = symbols('p q r')

expr1 = Implies(p, q)
expr2 = And(p, Or(Not(q), r))
expr3 = Equivalent(Implies(p, q), Or(Not(p), q))

print("自定义逻辑符号打印:")
print(print_logic(expr1))
print( print_logic(expr2))
print( print_logic(expr3))