import copy

from sympy import limit

import BFS
import numpy as np
import enum
import math
import random

class Action(enum.Enum):
    UP = 0
    DOWN=1
    LEFT= 2
    RIGHT = 3

class Board():
    limit=3
    bo=None
    num=12345678#默认值
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
        '''for i in np.arange(self.limit):
            for j in np.arange(self.limit):
                if self.bo[i,j]!=other.get_elem(i,j):
                   # print(self.bo,end="")
                    #print(f"!={other.bo}")
                   # print()'''
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


class PuzzleBFS(BFS.BFS):
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




k=8#0为空格
random.seed(4)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
goal= Board()
init_state=Board()
init_state.shuffle()
# 打乱数组

pb=PuzzleBFS(init_state,goal,3)
results= pb.search()
print(results)


