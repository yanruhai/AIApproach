import abc
import time

import numpy as np
from pydantic import BaseModel

class CSPNode(abc.ABC):
    domain:list

    def __init__(self, id, domain, **kwargs):
        super().__init__()
        self.id=id#可能是字符串，整数，元组等
        self.domain=domain#可能的值
        self.value=None
        self.value_index=-1
        self.remark=kwargs
        self.constraint={}
        #self.name=""#用于显示

    def set_value(self,value):
        if value in self.domain:
            self.value=value
            self.value_index=self.domain.index(value)

    def clear_value(self):
        self.value=None
        self.value_index=-1

    def next_value(self):
        if self.value_index<len(self.domain):
            self.value_index+=1
            self.value=self.domain[self.value_index]

    def add_constraint(self,cspNode:"CSPNode",func:callable,is_dual=True):
        if is_dual:#双向约束
            self.constraint[cspNode]=func
            cspNode.constraint[self]=func
        else:
            self.constraint[cspNode] = func

    def is_consistent(self):
        '''if cspNode.id in self.constraint.keys():#判断cspnode是不是相邻节点
            if not self.constraint[cspNode.id](self.value,cspNode.value):
                return False
        return True'''
        for node in self.constraint.keys():
            if node.value is not None:#相邻节点已经赋值
                if not self.constraint[node](self.value,node.value):#约束不满足
                    return False
        return True




class CSP:
    variables:list

    def __init__(self, variables, domains:dict):
        '''domain 各变量的定义域 {变量: [可能的值]}
            contraints={(var1,var2):function}'''
        self.variables=variables
        self.result_list= []#用于重复数据校验
        self.result={}
        self.nodes={}
        self.count=0
        for v in variables:
            n=CSPNode(v,domains[v])
            self.nodes[v]=n


    def add_contraint(self,var1,var2,func:callable):
        self.nodes[var1].add_constraint(self.nodes[var2],func)

    def print_result(self):
        self.count += 1
        for value in self.nodes.keys():
            print(f"{self.nodes[value].id}:{self.nodes[value].value}")
        print(f'over,this is the {self.count}th solve')


    def dfs_search(self,k):
        node = self.nodes[self.variables[k]]#测试第k个节点
        for d in node.domain:#对该节点值域做迭代
            node.set_value(d)
            if node.is_consistent():#如果没有违法约束
                if k==len(self.variables)-1:#变量全部赋值完成
                    self.print_result()
                else:
                    self.dfs_search(k+1)
        node.clear_value()



def create_map_coloring_csp():
    # 变量：州/省
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

    # 定义域：每个变量可以取的值（颜色）
    domains = {var: ['红', '绿', '蓝','白'] for var in variables}

    # 约束条件：相邻区域颜色不同
    constraints = {var: {} for var in variables}

    result={}
    csp=CSP(variables, domains)

    def constraint(x_val, y_val):
        return x_val != y_val
    # 添加相邻关系约束
    #add_neighbor_constraint(constraints, 'WA', 'NT')
    csp.add_contraint('WA', 'NT',constraint)
    #add_neighbor_constraint(constraints, 'WA', 'SA')
    csp.add_contraint('WA', 'SA',constraint)
    #add_neighbor_constraint(constraints, 'NT', 'SA')
    csp.add_contraint('NT', 'SA',constraint)
    #add_neighbor_constraint(constraints, 'NT', 'Q')
    csp.add_contraint('NT', 'Q',constraint)
    #add_neighbor_constraint(constraints, 'SA', 'Q')
    csp.add_contraint('SA', 'Q',constraint)
    #add_neighbor_constraint(constraints, 'SA', 'NSW')
    csp.add_contraint('SA', 'NSW',constraint)
    #add_neighbor_constraint(constraints, 'SA', 'V')
    csp.add_contraint('SA', 'V',constraint)
    #add_neighbor_constraint(constraints, 'Q', 'NSW')
    csp.add_contraint('Q', 'NSW',constraint)
    #add_neighbor_constraint(constraints, 'NSW', 'V')
    csp.add_contraint('NSW', 'V',constraint)
    return csp

class Timer:
    """Record multiple running times."""
    def __init__(self):
        """Defined in :numref:`sec_minibatch_sgd`"""
        self.times = []
        self.start()

    def start(self):
        """Start the timer."""
        self.tik = time.time()

    def stop(self):
        """Stop the timer and record the time in a list."""
        self.times.append(time.time() - self.tik)
        return self.times[-1]

    def avg(self):
        """Return the average time."""
        return sum(self.times) / len(self.times)

    def sum(self):
        """Return the sum of time."""
        return sum(self.times)

    def cumsum(self):
        """Return the accumulated time."""
        return np.array(self.times).cumsum().tolist()

class Benchmark:
    """For measuring running time."""
    def __init__(self, description='Done'):
        """Defined in :numref:`sec_hybridize`"""
        self.description = description

    def __enter__(self):
        self.timer = Timer()
        return self

    def __exit__(self, *args):
        print(f'{self.description}: {self.timer.stop():.4f} sec')

class PointNode(CSPNode):
    def __init__(self,x,y,domain):
        super.__init__((x,y),domain)
        self.color=None

    def compute_distance(self,x,y):
        distance=(x-self.point[0])**2+(y-self.point[1])**2
        return distance


X={'WA','NT','Q','SA','NSW','V','T'}
D={}
c=create_map_coloring_csp()
c.dfs_search(0)

rng = np.random.default_rng(seed=42)

num_x = rng.uniform(0, 1, 20)
num_y = rng.uniform(0, 1, 20)

point_list=[]
for (x,y) in zip(num_x,num_y):
   point_list.append((x,y))



