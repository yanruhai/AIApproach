import BFS
import numpy as np

#用BFS类测试图的找路
class TreeTravel(BFS.BFS):
    graph=None
    def __init__(self,init_state,graph,goal=None):
        super().__init__(init_state,goal)
        self.graph=graph

    def actions(self,state):
        """获得状态可以使用的action列表"""
        li=[]
        for ind,t in enumerate(graph[state]):
            if t==1:
                li.append(ind)
        return li

    def goal_test(self, state):
        """获得状态可以使用的action列表"""
        return state==self.goal


    def result(self, act):
        """获得action后的状态"""
        return act



t=0

graph=[[0,1,0,0],
       [0,0,1,0],
       [0,0,0,1],
       [0,0,0,0]]
tt= TreeTravel(t,graph,3)
results=tt.search()
print(results)