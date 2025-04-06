from functools import partial

import numpy as np
import enum
import math
import random
import copy

from chap3.astarsearch import AStarState


class Action(enum.Enum):
    UP = 0
    DOWN=1
    LEFT= 2
    RIGHT = 3

class Board(AStarState):
    def compute_hvalue(self):
        if not self.hfunction is None:
            self.hvalue=self.hfunction(self)


    def get_id(self):
        return self.num
    limit=3
    bo=None
    num=12345678#默认值
    def __str__(self):
        return f"{self.num}"

    def get_num(self):
        return self.num

    def __getitem__(self, item):
        return self.bo[item]
    def __setitem__(self, key, value):
        self.bo[key] = value

    def __init__(self,limit=3):
        super().__init__()
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

    def find_elem(self,num):
        temp = np.arange(self.limit)
        for i in temp:
            for j in temp:
                if self.bo[i, j] == num:
                    return i, j
        return -1, -1

    def __convert_to_num(self):
        temp = 0
        for t1 in np.arange(self.limit):
            for t2 in np.arange(self.limit):
                temp = temp * 10 + self.bo[t1, t2]
        self.num = temp
        self.id=self.num

    def do_action(self,act):
        temp=copy.deepcopy(self)
        zi, zj = temp.findZero()
        match act:
            case Action.LEFT:
                temp[zi, zj] = temp[zi, zj + 1]
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

    def __eq__(self, other):
        return  self.num==other.get_num()

    def compute_hv(self):
        '''计算曼哈顿距离'''
        hv = 0
        for i in np.arange(line_limit):
            for j in np.arange(line_limit):
                t = goal[i, j]
                m1, m2 = self.find_elem(t)
                if m1 >= 0 and m2 >= 0:  # 计算曼哈顿距离
                    hv = hv + math.fabs(m1 - i) + math.fabs(m2 - j)
        return hv

    def shuffle(self):
        array = [t for t in np.arange(self.limit**2)]
        random.shuffle(array)
        temp=0
        for t1 in np.arange(self.limit):
            for t2 in np.arange(self.limit):
                self.bo[t1, t2] = array[t1 * self.limit + t2]
                temp=temp*10+self.bo[t1,t2]
        self.num=temp


class PuzzleSearch:
    goal=None
    state=None
    def __init__(self,init_state:Board,goal:Board):
        self.state=init_state
        self.goal=goal

    def search_climb_random_restart(self):
        if self.state==self.goal:
            return None
        r_s = None
        b=False

        while not b:
            lz = self.actions(self.state)
            min = self.state.compute_hv()
            r_s = None
            b = True
            count = 0
            for k_act in lz:
                st_a=self.state.do_action(k_act)
                hv= st_a.compute_hv()
                if hv<min:
                    min=hv
                    r_s=st_a
                    b=False
                    count+=1
                    print(f"调整{count}次")
            if min < self.state.compute_hv():#出现更好的结果
                self.state=r_s
            else:
                self.state.shuffle()
                b=False
            if self.goal_test(self.state):
                return self.state
        return self.state



    def actions(self, state:Board):
        zi, zj = state.findZero()
        move = []
        if zi > 0: move.append(Action.DOWN)
        if zi < line_limit - 1: move.append(Action.UP)  # 可以上
        if zj > 0: move.append(Action.RIGHT)  # 可以右
        if zj < line_limit - 1: move.append(Action.LEFT)  # 可以左
        return move


    def goal_test(self, state: Board):
        return state == goal

    def result(self, state, act):
        tt= state.do_action(act)
        tt.compute_hvalue()#重新计算hvalue
        tt.set_gvalue(state.get_gvalue()+1)
        return tt


k=8#0为空格
random.seed(21)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
goal= Board()
init_state=Board()
init_state.shuffle()
# 打乱数组
goal2=Board(limit=3)
init_state2=Board(limit=3)
init_state2.shuffle()
p=PuzzleSearch(init_state,goal)
r= p.search_climb_random_restart()
print(r)






