
from enum import Enum

class Action(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3



class MiniMax:
    tree = [0, 0, 0, 0, 0, 3, 12, 8, 2, 4, 6, 14, 5, 2]  # 0单元未用

    def __init__(self,tree):
        self.tree=tree

    def actions(self,state):
        return [Action.FIRST,Action.SECOND,Action.THIRD]

    def result(self,state,action):
        match action:
            case Action.FIRST: return state*3-1
            case Action.SECOND:return state*3
            case Action.THIRD:return state*3+1

    def terminal_test(self,state):
        if self.tree[state]==0:return False
        return True

    def utility(self,state):
        return self.tree[state]

    def max_value(self,state):
        if self.terminal_test(state):return self.utility(state)
        v=-float('inf')
        for a in self.actions(state):
            vt=self.min_value(self.result(state,a))
            if vt>v:v=vt
        return v

    def min_value(self,state):
        if self.terminal_test(state): return self.utility(state)
        v = float('inf')
        for a in self.actions(state):
            vt = self.max_value(self.result(state, a))
            if vt < v: v = vt
        return v

    def mini_max_decision(self,state):
        v=-float('inf')
        for a in self.actions(state):
            vt = self.min_value(self.result(state, a))
            print(f"{state},{a}:{vt}")
            if vt > v: v = vt
        return v

tree = [0, 0, 0, 0, 0, 3, 12, 8, 2, 4, 6, 14, 5, 2]
t33=MiniMax(tree)
r=t33.mini_max_decision(1)
print(r)



