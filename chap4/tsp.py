from copy import copy, deepcopy
from functools import partial

import numpy as np

from chap3.search import ExploredSet
from mst import MST_Prim
from chap3.astarsearch import AstarSearch, AStarState, T, OrderedFrontier

inf=float('inf')

class TspState(AStarState):
    visited_nodes=[]
    current_node1=None#扩展点
    current_node2=None#接回点
    unvisited_nodes=[]

    def __init__(self,visited_nodes:set,current_node1,unvisited_nodes:set,current_node2,hfunction=None):
        super().__init__(hfunction)
        self.visited_nodes=visited_nodes
        self.current_node1=current_node1
        self.unvisited_nodes=unvisited_nodes
        self.current_node2=current_node2

    def get_visited_nodes(self):
        return self.visited_nodes

    def get_current_node1(self):
        return self.current_node1

    def get_current_node2(self):
        if self.current_node2 is None:
            return self.current_node1
        return self.current_node2

    def get_unvisited_nodes(self):
        return self.unvisited_nodes



class TspAstarSearch(AstarSearch[TspState]):


    def actions(self, state: T)->list:
        lts=[]
        for c_node in state.get_unvisited_nodes():
                 t_unvisited_nodes = copy(state.get_unvisited_nodes())
                 t_visited_nodes=copy(state.get_visited_nodes())
                 if t_visited_nodes is None:
                     t_visited_nodes=set()
                 t_unvisited_nodes.discard(c_node)
                 temp_state=TspState(t_visited_nodes.add(state.get_current_node1()),c_node,t_unvisited_nodes,state.get_current_node2(),hfunc)
                 temp_state.compute_fvalue()
                 temp_state.set_gvalue(arc_map3[state.get_current_node1()][c_node]+state.get_gvalue())
                 temp_state.set_id(str(state.get_id())+str(c_node))
                 lts.append(temp_state)
        return lts



    def goal_test(self, state: T)->bool:
       if state.get_unvisited_nodes()is None:
            return True
       if len(state.get_unvisited_nodes())==0:
           return True
       return False


    def result(self, state, act)->T:
        act.compute_fvalue()
        return act




arc_map3= [[inf,4,1,3,2],
           [4,inf,5,6,3],
           [1,5,inf,2,4],
           [3,6,2,inf,5],
           [2,3,4,5,inf]]

def heurisitic_function(state):
    if len(state.get_unvisited_nodes())==0:return 0
    mst_t=MST_Prim(arc_map3,copy(state.get_unvisited_nodes()))
    r=mst_t.search()
    hvalue=0
    for temp in r:
        hvalue+=temp[1]#将所有树的边相加
    min=inf#先假定最小值
    for node in state.get_unvisited_nodes():
        temp_dis=arc_map3[state.get_current_node1()][node]+arc_map3[node][state.get_current_node2()]
        if temp_dis<min:
            min=temp_dis
    return hvalue+min

hfunc=partial(heurisitic_function)
all_nodes=set(np.arange(len(arc_map3[0]))[1:])
start_node=set()
unvisited_nodes=all_nodes
init_state=TspState(start_node,0,unvisited_nodes,0,hfunc)
tsp=TspAstarSearch(init_state)
r=tsp.search()
while not r is None:
    print(r.state.get_current_node1())
    r=r.parent
