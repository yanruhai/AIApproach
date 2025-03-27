import numpy as np

from astarsearch import AstarSearch, T, AStarState
from search import ExploredSet, Node, Frontier,State

#人工智能教材P84图3.15
#sibiu=0 Rimnicu=1 Fagaras=2 Pitesti=3 Bucharest=4





class My_Astar_State(AStarState):
    gvalue=0
    hvalue=0
    def __init__(self,id,gvalue,hvalue=0):
        self.gvalue=gvalue
        self.hvalue=hvalue
        self.id=id

    def get_hvalue(self):
        return 0

    def get_gvalue(self):
        return self.gvalue


class My_Astarsearch(AstarSearch):
    inf = 10 ** 100
    map = [[inf, 80, 99, inf, inf],
           [80, inf, inf, 97, inf],
           [99, inf, inf, inf, 211],
           [inf, 97, inf, inf, 101],
           [inf, inf, 211, 101, inf]]

    def actions(self, state: T):
        id=state.get_id()
        action_list=[]
        for ind,k in enumerate(self.map[id]):
            if k<self.inf:
                action_list.append(ind)
        return action_list

    def goal_test(self, state: T):
        if state.get_id()==4:
            return True
        return False

    def init_exploredset(self):
        return ExploredDict()

    def result(self, state, act):
        cost=self.map[state.get_id()][act]
        new_state=My_Astar_State(act,cost)
        return new_state

class ExploredDict(ExploredSet):

    def check(self, state):

        if state.get_id() in self.expl:
            return False
        return True

    def put(self, state):
        self.expl[state.get_id()] = state

init_state=My_Astar_State(0,0)
test= My_Astarsearch(init_state)
r= test.search()
while not r is None:
    print(r.get_id())
    print(r.state.get_gvalue())
    r=r.parent
