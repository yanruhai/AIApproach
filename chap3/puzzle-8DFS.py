import copy

import DFS
import numpy as np
import enum
import math
import random
from search import ExploredSet


class Action(enum.Enum):
    UP = 0
    DOWN=1
    LEFT= 2
    RIGHT = 3

class Board():
    limit=3
    bo=None
    num=12345678#默认值
    def get_id(self):
        return self.num

    def __str__(self):
        return f"{self.num}"

    def get_num(self):
        return self.num

    def __getitem__(self, item):
        return self.bo[item]
    def __setitem__(self, key, value):
        self.bo[key] = value

    def __init__(self,limit=3):
        self.limit=limit
        self.bo = np.zeros((limit, limit), dtype=int)
        for t1 in np.arange(limit):
            for t2 in np.arange(limit):
                self.bo[t1, t2] = t1 * limit + t2


    def findZero(self):
        temp = np.arange(self.limit)
        for i in temp:
            for j in temp:
                if self.bo[i, j] == 0:
                    return i, j
        return 0, 0

    def __convert_to_num(self):
        temp = 0
        for t1 in np.arange(self.limit):
            for t2 in np.arange(self.limit):
                temp = temp * 10 + self.bo[t1, t2]
        self.num = temp

    def do_action(self,act):
        temp=copy.deepcopy(self)
        zi, zj = temp.findZero()
        match act:
            case Action.LEFT:
                temp[(zi, zj)] = temp[(zi, zj + 1)]
                temp[zi, zj + 1] = 0
            case Action.RIGHT:
                temp[zi, zj] = temp[zi, zj - 1]
                temp[zi, zj - 1] = 0
            case Action.UP:
                temp[zi, zj] = temp[zi + 1, zj]
                temp[zi + 1, zj] = 0
            case Action.DOWN:
                temp[zi, zj] = temp[zi - 1, zj]
                temp[zi - 1, zj] = 0
        temp.__convert_to_num()
        return temp

    def get_elem(self,i,j):
        return self.bo[i,j]

    def __eq__(self, other):
        return  self.num==other.get_num()


    def shuffle(self):
        array = [t for t in np.arange(self.limit**2)]
        random.shuffle(array)
        temp=0
        for t1 in np.arange(self.limit):
            for t2 in np.arange(self.limit):
                self.bo[t1, t2] = array[t1 * self.limit + t2]
                temp=temp*10+self.bo[t1,t2]
        self.num=temp
        print("打乱后的数组:", self.bo)


class ExploredDict(ExploredSet):
    def check(self, state):
        '''temp= self.expl.get(state.get_num())
        if temp==None:
            return True
        return False'''
        if state.get_num() in self.expl:
            return False
        return True

    def put(self, state):
        self.expl[state.get_num()] = state


class PuzzleDFS(DFS.DFS):
    def init_exploredset(self):
       return ExploredDict()

    line_limit=3

    def __init__(self,init_state,goal=None,line_limit=3):
        super().__init__(init_state,goal)
        self.line_limit=line_limit

    def actions(self, state):
        zi, zj = state.findZero()
        #move = [False, False, False, False]  # 表示上下左右四个动作
        move=[]
        if zi > 0: move.append(Action.DOWN)
        if zi < line_limit - 1: move.append(Action.UP)  # 可以上
        if zj > 0: move.append(Action.RIGHT)  # 可以右
        if zj < line_limit - 1: move.append(Action.LEFT)  # 可以左
        return move

    def goal_test(self, state):
        return state==goal

    def result(self,state, act):
        return state.do_action(act)



def node_print(n):
    print(math.floor(n/1000000))
    print(math.floor((n/1000)%1000))
    print(n%1000)
    print()

k=8#0为空格
random.seed(24)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
goal= Board()
init_state=Board()
init_state.shuffle()
# 打乱数组

pb=PuzzleDFS(init_state,goal,3)
results= pb.search()
#n=123456789
#node_print(n)
print(f"共有{len(results)}个解")
'''for k in results:
    while k!=None:
        node_print(k.get_num())
        k=k.parent'''


