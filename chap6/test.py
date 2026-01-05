import numpy as np
from sympy import false
from torch.fx.experimental.unification import variables


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # 变量列表
        self.domains = domains  # 各变量的定义域 {变量: [可能的值]}
        self.constraints = constraints  # 约束条件 {变量: {邻居变量: 约束函数}}
        self.result = {}  # 保管结果，初始化为空字典

    def is_consistent(self, variable, assignment):
        """检查变量在当前赋值下是否满足所有相关约束"""
        for neighbor in self.constraints[variable]:
            if neighbor in assignment:
                constraint_func = self.constraints[variable][neighbor]
                if not constraint_func(assignment[variable], assignment[neighbor]):
                    return False
        return True

    count = 0  # 解的数量

    def print_result(self):
        self.count += 1
        print('解', self.count)
        for u, v in self.result.items():
            print(u, v)

    def dfs_search(self, k):
        if k == len(self.variables):  # 所有变量都已赋值
            self.print_result()
            return

        var = self.variables[k]
        for d in self.domains[var]:
            self.result[var] = d
            if self.is_consistent(var, self.result):  # 如果没有违反约束
                self.dfs_search(k + 1)
        # 回溯
        if var in self.result:
            del self.result[var]


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
    # 移除错误的约束：塔斯马尼亚与其他州不相邻
    # add_neighbor_constraint(constraints, 'V', 'T')  # 这行应该被注释掉或删除

    return CSP(variables, domains, constraints)


def add_neighbor_constraint(constraints, var1, var2):
    """添加相邻变量的约束（颜色不同）"""

    def constraint(x_val, y_val):
        return x_val != y_val

    # 确保var1的约束字典存在
    constraints[var1].setdefault(var2, constraint)
    # 确保var2的约束字典存在
    constraints[var2].setdefault(var1, constraint)


X = {'WA', 'NT', 'Q', 'SA', 'NSW', 'V', 'T'}
D = {}
c = create_map_coloring_csp()
c.dfs_search(0)
