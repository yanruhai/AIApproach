import abc

import numpy as np
from pydantic import BaseModel

class ConstrainedNode(abc.ABC,BaseModel):
    domain:set

    def __init__(self,id,domain,**kwargs):
        self.id=None#可能是字符串，整数，元组等
        self.domain=domain#可能的值
        self.value=None
        self.remark=kwargs
        #self.name=""#用于显示

    def set_value(self,value):
        self.value=value

class ConstrainedSet(abc.ABC):
    def __init__(self,variables:list,domain):
        self.nodes=[]
        for i in variables:
            node= ConstrainedNode(i,domain)
            self.nodes.append(node)

    def add_neighbor_constraint(self,constraints:dict, var1:ConstrainedNode, var2:ConstrainedNode,constraint:callable):
        """添加相邻变量的约束（颜色不同）"""
        # 正确方式：使用字典的setdefault方法安全添加约束
        constraints[var1.id].setdefault(var2, constraint)
        # 确保var2的约束字典存在
        constraints[var2.id].setdefault(var1, constraint)

class CSP(BaseModel):

    def __init__(self, variables, domains:list,constraints, result):
        self.variables = variables  # 变量列表
        self.domains = domains  # 各变量的定义域 {变量: [可能的值]}
        self.constraints = constraints  # 约束条件 {变量对: 约束函数}
        self.result=result #保管结果
        self.result_list= []#用于重复数据校验
        self.nodes=[]
        self.count=0
        for i,v in self.variables:
            n=ConstrainedNode(v,domains[i])
            self.nodes.append(n)


    def is_consistent(self, variable, assignment):
        """检查变量在当前赋值下是否满足所有相关约束"""
        for neighbor in self.constraints[variable]:
            if neighbor in assignment:
                constraint_func = self.constraints[variable][neighbor]
                if not constraint_func(assignment[variable], assignment[neighbor]):
                    return False
        return True


    def print_result(self):
        t=set(self.result.values())
        for re in self.result_list:
             if re==t:#集合校验
                    return
        self.count+=1
        self.result_list.append(set(self.result.values()))
        print('解',self.count)

        #for u,v in self.result.items():
            #print(u,v)


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


def create_map_coloring_csp():
    # 变量：州/省
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

    # 定义域：每个变量可以取的值（颜色）
    domains = {var: ['红', '绿', '蓝','白'] for var in variables}

    # 约束条件：相邻区域颜色不同
    constraints = {var: {} for var in variables}

    result={}
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
    return CSP(variables, domains, constraints,result)


def add_neighbor_constraint(constraints, var1, var2):
    """添加相邻变量的约束（颜色不同）"""

    def constraint(x_val, y_val):
        return x_val != y_val

    # 正确方式：使用字典的setdefault方法安全添加约束
    # 确保var1的约束字典存在
    constraints[var1].setdefault(var2, constraint)
    # 确保var2的约束字典存在
    constraints[var2].setdefault(var1, constraint)

class Node:
    def __init__(self,x,y):
        self.point=(x,y)
        self.color=None

    def compute_distance(self,x,y):
        distance=(x-self.point[0])**2+(y-self.point[1])**2
        return distance


X={'WA','NT','Q','SA','NSW','V','T'}
D={}
c=create_map_coloring_csp()
c.dfs_search(0)

num_x = np.random.uniform(0, 1,20)
num_y = np.random.uniform(0, 1,20)
point_list=np.array([])
for (x,y) in zip(num_x,num_y):
   np.append(point_list,(x,y))


