import random
from functools import partial

import numpy as np

from chap3.astarsearch import AstarSearch, T, AStarState
from chap3.search import ExploredSet

inf = 10 ** 100
cost_map = [[inf, 10,12,inf,inf],
       [10, inf, 7, inf, 14],
       [12, 7, inf, 6, inf],
       [inf, inf, 6, inf, 5],
       [inf, 14, inf, 5, inf]]
heuristic=[17,13,9,4,0]


class MyState(AStarState):
    def __init__(self,id,hfunction=None):
        super().__init__(hfunction)
        self.id=id
        self.gvalue=0
    def do_action(self,ind):
        return ind




class ExploredDict(ExploredSet):

    def check(self, state):

        if state.get_id() in self.expl:
            return False
        return True

    def put(self, state):
        self.expl[state.get_id()] = state

class Astar_heu_Search(AstarSearch):

    def actions(self, state: T):
        mov=[]
        for ind,k in enumerate(cost_map[state.get_id()]):
            if k<inf:
                temp=MyState(ind)
                temp.set_gvalue(k+state.get_gvalue())
                temp.set_hfunction(hf)
                mov.append(temp)
        return mov

    def goal_test(self, state: T):
        return state.get_id() == goal_state.get_id()

    def init_exploredset(self):
        return ExploredDict()

    def result(self, state, act):
        tt= state.do_action(act)
        return tt

def my_hfunction(goal,cur_state):
    return heuristic[cur_state.get_id()]


random.seed(24)
init_state=MyState(0)

goal_state=MyState(4)
hf=partial(my_hfunction,goal_state)
init_state.set_hfunction(hf)
goal_state.set_hfunction(hf)
st= Astar_heu_Search(init_state,goal_state)
r= st.search()
print(r)

