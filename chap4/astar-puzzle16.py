from functools import partial
import cProfile
import numpy as np
import enum
import math
import random
import copy

from chap3.astarsearch import AStarState, AstarSearch, T


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
    limit=4
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

    def __init__(self,limit=4):
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

    '''def get_elem(self,i,j):
        return self.bo[i,j]'''

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





class Astar_8puzzle_Search(AstarSearch):

    def actions(self, state: T):
        zi, zj = state.findZero()
        # move = [False, False, False, False]  # 表示上下左右四个动作
        move = []
        if zi > 0: move.append(Action.DOWN)
        if zi < line_limit - 1: move.append(Action.UP)  # 可以上
        if zj > 0: move.append(Action.RIGHT)  # 可以右
        if zj < line_limit - 1: move.append(Action.LEFT)  # 可以左
        return move

    def goal_test(self, state: T):
        return state == goal



    def result(self, state, act):
        tt= state.do_action(act)
        tt.compute_hvalue()#重新计算hvalue
        tt.set_gvalue(state.get_gvalue()+1)
        return tt

def my_hfunction(limit,goal,cur_state):
    hv=0
    for i in np.arange(limit):
        for j in np.arange(limit):
            t=goal[i,j]
            m1,m2 = cur_state.find_elem(t)
            if m1>=0 and m2>=0:#计算曼哈顿距离
                hv=hv+ math.fabs(m1-i)+math.fabs(m2-j)
    return hv


k=15#0为空格
random.seed(21)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
goal= Board()
init_state=Board()
init_state.shuffle()
# 打乱数组
goal2=Board(limit=4)
init_state2=Board(limit=4)
init_state2.shuffle()
hfunc=partial(my_hfunction,4,goal)
goal.set_hfunction(hfunc)
init_state.set_hfunction(hfunc)
init_state.compute_hvalue()
se=Astar_8puzzle_Search(init_state,goal)
tts= se.search()
#cProfile.run('se.search()')
while tts!=None:
    print(tts.get_id())
    tts=tts.parent