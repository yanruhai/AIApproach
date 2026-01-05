


import numpy as np
from sympy import false
from torch.fx.experimental.unification import variables


class CSP:
    def __init__(self, variables, domains, constraints,result):
        self.variables = variables  # 变量列表
        self.domains = domains  # 各变量的定义域 {变量: [可能的值]}
        self.constraints = constraints  # 约束条件 {变量对: 约束函数}
        self.result=result #保管结果

    def is_consistent(self, variable, assignment):
        """检查变量在当前赋值下是否满足所有相关约束"""
        for neighbor in self.constraints[variable]:
            if neighbor in assignment:
                constraint_func = self.constraints[variable][neighbor]
                if not constraint_func(assignment[variable], assignment[neighbor]):
                    return False
        return True


    count=0#解的数量
    def print_result(self):
        self.count+=1
        print('解',self.count)
        for u,v in self.result.items():
            print(u,v)

    def dfs_search(self,k):
        var = self.variables[k]
        for d in self.domains[self.variables[k]]:
            self.result[self.variables[k]] = d
            if self.is_consistent(self.variables[k],self.result):#如果没有违法约束
                if k==len(self.variables)-1:#变量全部赋值完成
                    self.print_result()
                else:
                    self.dfs_search(k+1)
        del self.result[var]






# 示例：骑士问题
def create_csp(n,k):

    variables = ['k'+str(i) for i in range(k)]
    base_list = []
    for i in range(n):
        for j in range(n):
            base_list.append((i,j))
    # 定义域：每个变量可以取的值（颜色）
    domains = {var: base_list.copy() for var in variables}

    # 约束条件：相邻区域颜色不同
    constraints = {var: {} for var in variables}

    result={}
    # 添加相邻关系约束
    for i in variables:
        for j in variables:
            if i!=j:
                add_neighbor_constraint(constraints, i, j)

    return CSP(variables, domains, constraints,result)


def add_neighbor_constraint(constraints, var1, var2):
    """添加相邻变量的约束（颜色不同）"""

    def constraint(a_val, b_val):
        if a_val[0]==b_val[0] and a_val[1]==b_val[1]:
            return False
        val_list=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for i in range(8):
            if a_val[0]==b_val[0]+val_list[i][0] and a_val[1]==b_val[1]+val_list[i][1]:
                return False
        return True

    # 正确方式：使用字典的setdefault方法安全添加约束
    # 确保var1的约束字典存在
    constraints[var1].setdefault(var2, constraint)
    # 确保var2的约束字典存在
    #constraints[var2].setdefault(var1, constraint)


c=create_csp(4,6)
c.dfs_search(0)
