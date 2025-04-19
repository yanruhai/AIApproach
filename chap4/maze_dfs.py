import enum

import numpy as np

from chap3 import DFS
from chap3.search import ExploredSet, State


class CoorState(State):
    def __init__(self,x,y):
        self.cur_state=(x,y)
    def __getitem__(self, item):
        return self.cur_state[item]
    def __eq__(self, other):
        if self.cur_state[0]==other[0] and self.cur_state[1]==other[1]:
            return True
        return False
    def get_id(self):
        return f"{self.cur_state[0]},{self.cur_state[1]}"
    def set_id(self,d):
        print("未实现")
    cur_state=(0,0)

class Action(enum.Enum):
    UP = 0
    DOWN=1
    LEFT= 2
    RIGHT = 3

class Maze(DFS.DFS):
    def actions(self, state):
        x=state[0]
        y=state[1]
        act_list=[]
        if x>0 and self.data[x-1][y]==0: act_list.append(Action.UP)
        if x<self.limit-1 and self.data[x+1][y]==0:act_list.append(Action.DOWN)
        if y>0 and self.data[x][y-1]==0 :act_list.append(Action.LEFT)
        if y<self.limit-1 and self.data[x][y+1]:act_list.append(Action.RIGHT)
        return act_list

    def goal_test(self, state):
        if state==self.goal_point:
            return True
        return False

    def init_exploredset(self):
        return ExploredSet()

    def result(self, state, act):
        match act:
            case Action.RIGHT: return CoorState(state[0],state[1]+1)
            case Action.LEFT:return CoorState(state[0],state[1]-1)
            case Action.UP:return CoorState(state[0]-1,state[1])
            case Action.DOWN:return CoorState(state[0]+1,state[1])


    # 0代表空地，可以移动, 1代表墙,2代表
    data=[
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]]
    cur=CoorState(0,0)
    start_point=CoorState(0,0)
    goal_point=CoorState(5,9)
    limit=10

m=Maze(CoorState(0,0))
r= m.search()
r=r[0]
while r!=None:
    print(r.get_id())
    r=r.parent

