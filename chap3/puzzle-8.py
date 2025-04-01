import enum
import math
import random
import numpy as np

class Action(enum.Enum):
    UP = 0
    DOWN=1
    LEFT= 2
    RIGHT = 3

def findZero(board,line_limit):
    temp=np.arange(line_limit)
    for i in temp:
        for j in temp:
            if board[i,j]==0:
                return i,j
    return 0,0

def do_result(board,line_limit,act):
    can_do,zi,zj=actions(board,line_limit)
    if can_do:
        match act:
            case Action.LEFT:
                board[zi,zj]=board[zi,zj+1]
                board[zi,zj+1]=0
            case Action.RIGHT:
                board[zi,zj]=board[zi,zj-1]
                board[zi,zj-1]=0
            case Action.UP:
                board[zi,zj]=board[zi+1,zj]
                board[zi+1,zj]=0
            case Action.DOWN:
                board[zi,zj]=board[zi-1,zj]
                board[zi-1,zj]=0


def actions(board,line_limit):
    zi,zj=findZero(board,line_limit)
    move=[False,False,False,False]#表示上下左右四个动作
    if zi>0:move[1]=True
    if zi<line_limit-1: move[0]=True#可以上
    if zj>0:move[3]=True#可以右
    if zj<line_limit-1:move[2]=True#可以左
    return move,zi,zj


k=8#0为空格
random.seed(42)
line_limit=math.floor(math.sqrt(k+1))
# 定义一个一维数组
array = [t for t in np.arange(k+1)]

# 打乱数组
random.shuffle(array)
init_state=np.zeros((line_limit, line_limit), dtype=int)
result=np.zeros((line_limit,line_limit),dtype=int)
for t1 in np.arange(line_limit):
    for t2 in np.arange(line_limit):
        init_state[t1,t2]=array[t1 * line_limit + t2]
        result[t1,t2]=t1*line_limit+t2
print("打乱后的数组:", init_state)
frontier=[]

do_result(init_state, line_limit, Action.RIGHT)
print()