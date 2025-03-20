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
    def __init__(self,limit=3):
        self.limit=limit
        self.bo = np.zeros((limit, limit), dtype=int)
        for t1 in np.arange(limit):
            for t2 in np.arange(limit):
                self.bo[t1, t2] = t1 * limit + t2

    def shuffle(self):
        random.shuffle(array)
        init_state = np.zeros((line_limit, line_limit), dtype=int)
        goal = np.zeros((line_limit, line_limit), dtype=int)
        for t1 in np.arange(line_limit):
            for t2 in np.arange(line_limit):
                init_state[t1, t2] = array[t1 * line_limit + t2]
                goal[t1, t2] = t1 * line_limit + t2
        print("打乱后的数组:", init_state)




class PuzzleBFS(BFS.BFS):
    line_limit=3

    def __init__(self,init_state,goal=None,line_limit=3):
        super().__init__(init_state,goal)
        self.line_limit=line_limit

    def actions(self, state):
        zi, zj = self.findZero(state)
        move = [False, False, False, False]  # 表示上下左右四个动作
        if zi > 0: move[1] = True
        if zi < line_limit - 1: move[0] = True  # 可以上
        if zj > 0: move[3] = True  # 可以右
        if zj < line_limit - 1: move[2] = True  # 可以左
        return move, zi,zj

    def goal_test(self, state):
        for i in np.arange(line_limit):
            for j in np.arange(line_limit) :
                if state[i,j]!=goal[i,j]:
                    return False
        return True

    def result(self,state, act):
        zi,zj=self.findZero(state)
        match act:
            case Action.LEFT:
                state[zi, zj] = state[zi, zj + 1]
                state[zi, zj + 1] = 0
            case Action.RIGHT:
                state[zi, zj] = state[zi, zj - 1]
                state[zi, zj - 1] = 0
            case Action.UP:
                state[zi, zj] = state[zi + 1, zj]
                state[zi + 1, zj] = 0
            case Action.DOWN:
                state[zi, zj] = state[zi - 1, zj]
                state[zi - 1, zj] = 0

    def findZero(self,state):
        temp = np.arange(self.line_limit)
        for i in temp:
            for j in temp:
                if state[i, j] == 0:
                    return i, j
        return 0, 0


k=8#0为空格
random.seed(42)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
array = [t for t in np.arange(k+1)]

# 打乱数组
random.shuffle(array)
init_state=np.zeros((line_limit, line_limit), dtype=int)
goal=np.zeros((line_limit, line_limit), dtype=int)
for t1 in np.arange(line_limit):
    for t2 in np.arange(line_limit):
        init_state[t1,t2]=array[t1 * line_limit + t2]
        goal[t1,t2]= t1 * line_limit + t2
print("打乱后的数组:", init_state)

pb=PuzzleBFS(init_state,goal,3)
results= pb.search()
print(results)


