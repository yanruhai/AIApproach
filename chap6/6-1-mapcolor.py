import numpy as np


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # 变量列表
        self.domains = domains  # 各变量的定义域 {变量: [可能的值]}
        self.constraints = constraints  # 约束条件 {变量对: 约束函数}

    def is_consistent(self, variable, assignment):
        """检查变量在当前赋值下是否满足所有相关约束"""
        for neighbor in self.constraints[variable]:
            if neighbor in assignment:
                constraint_func = self.constraints[variable][neighbor]
                if not constraint_func(variable, assignment[variable], neighbor, assignment[neighbor]):
                    return False
        return True


# 示例：地图着色问题
def create_map_coloring_csp():
    # 变量：州/省
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

    # 定义域：每个变量可以取的值（颜色）
    domains = {var: ['红', '绿', '蓝'] for var in variables}

    # 约束条件：相邻区域颜色不同
    constraints = {var: {} for var in variables}

    # 添加相邻关系约束
    add_neighbor_constraint(constraints, 'WA', 'NT')
    add_neighbor_constraint(constraints, 'WA', 'SA')
    add_neighbor_constraint(constraints, 'NT', 'SA')
    add_neighbor_constraint(constraints, 'NT', 'Q')
    add_neighbor_constraint(constraints, 'SA', 'Q')
    add_neighbor_constraint(constraints, 'SA', 'NSW')
    add_neighbor_constraint(constraints, 'SA', 'V')
    add_neighbor_constraint(constraints, 'Q', 'NSW')
    add_neighbor_constraint(constraints, 'NSW', 'V')
    add_neighbor_constraint(constraints, 'V', 'T')  # 注意：T与其他州不相邻

    return CSP(variables, domains, constraints)


def add_neighbor_constraint(constraints, var1, var2):
    """添加相邻变量的约束（颜色不同）"""

    def constraint(x, x_val, y, y_val):
        return x_val != y_val

    # 双向添加约束
    constraints[var1][var2] = constraint
    constraints[var2][var1] = constraint

X={'WA','NT','Q','SA','NSW','V','T'}
D={}
create_map_coloring_csp()