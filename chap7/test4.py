from z3 import *
import re

from z3.z3 import Solver, sat, Bool


def parse_expression(expr_str):
    # 检查括号是否匹配
    if expr_str.count('(') != expr_str.count(')'):
        raise ValueError("表达式中的括号不匹配")

    # 1. 提取所有变量
    variables = set(re.findall(r'[a-zA-Z]+', expr_str))
    # 创建Z3变量字典
    z3_vars = {var: Bool(var) for var in variables}

    # 2. 替换逻辑符号为Z3函数
    # 先处理蕴含符号 ->
    expr_str = expr_str.replace("->", "Implies")
    # 处理非符号 ~
    expr_str = expr_str.replace("~", "Not(")

    # 3. 为Not添加相应的右括号
    # 这个正则表达式会找到Not(后面的变量或表达式，并添加右括号
    # 处理简单情况：Not(变量)
    expr_str = re.sub(r'Not\(([a-zA-Z]+)\)', r'Not(\1)', expr_str)
    # 处理带括号的情况：Not(...)
    # 这里使用一个简单的计数器来匹配括号
    temp = []
    count = 0
    for c in expr_str:
        temp.append(c)
        if c == '(' and temp[-2:-1] == ['t'] and temp[-3:-2] == ['o'] and temp[-4:-3] == ['N']:
            count += 1  # 遇到Not(时增加计数
        elif c == ')' and count > 0:
            count -= 1
            if count == 0:
                temp.append(')')  # 添加一个右括号闭合Not

    expr_str = ''.join(temp)

    # 4. 处理其他逻辑运算符
    expr_str = expr_str.replace("&", "And")
    expr_str = expr_str.replace("|", "Or")

    # 5. 为二元运算符添加括号
    # 找到所有And、Or、Implies，为其添加括号
    # 简单处理二元运算符的情况
    expr_str = re.sub(r'(\w+)\s*And\s*(\w+)', r'And(\1, \2)', expr_str)
    expr_str = re.sub(r'(\w+)\s*Or\s*(\w+)', r'Or(\1, \2)', expr_str)
    expr_str = re.sub(r'(\w+)\s*Implies\s*(\w+)', r'Implies(\1, \2)', expr_str)

    try:
        # 使用eval转换为Z3表达式
        z3_expr = eval(expr_str, {}, z3_vars)
        return z3_expr, z3_vars
    except Exception as e:
        raise ValueError(f"表达式解析错误: {e}，处理后的表达式: {expr_str}")


# 测试用例
test_cases = [
    "p->~q",
    "(p&q)->~r",
    "p->(q|~r)",
    "~(p&q)->r"
]

for expr_str in test_cases:
    try:
        z3_expr, z3_vars = parse_expression(expr_str)
        s = Solver()
        s.add(z3_expr)
        if s.check() == sat:
            model = s.model()
            print(f"表达式: {expr_str}")
            print(f"满足条件的解: {model}\n")
    except Exception as e:
        print(f"处理表达式 '{expr_str}' 时出错: {e}\n")
