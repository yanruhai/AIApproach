import numpy as np
from networkx.classes import nodes

inf=10**100
class MST_Prim:
    arc_map=None#邻接矩阵表示的图
    result_arcs=[]

    nodes=[]#总节点数

    def __init__(self,arc_map,nodes):
        self.arc_map=arc_map
        self.nodes=nodes

    def __refresh_arcs(self,visited_nodes,unvisited_nodes):
        '''找到visited_nodes中与unvisited_nodes中最近的边,返回边列表和最小边'''
        arcs=[]
        min=inf
        min_arc=None
        for node in visited_nodes:
            for jnode in unvisited_nodes:
                temp_arc=((node,jnode),self.arc_map[node][jnode])
                if temp_arc[1] < inf:
                    arcs.append(temp_arc)
                    if temp_arc[1]<min:
                        min=temp_arc[1]
                        min_arc=temp_arc
        return arcs,min_arc

    def search(self)->list:
        visited_nodes= {self.nodes[0]}  #任取一个节点
        unvisited_nodes= set(self.nodes[1:])
        result_arcs=[]
        while len(unvisited_nodes) > 0:
            arcs,min_arc=self.__refresh_arcs(visited_nodes,unvisited_nodes)
            if not min_arc is None:#正常情况下，min_arc不为空
                visited_nodes.add(min_arc[0][1])
                unvisited_nodes -= {min_arc[0][1]}
                result_arcs.append(min_arc)
            #如果min_arc为空，说明所有节点都已经访问完毕，退出循环
        return result_arcs


arc_map = [[inf, 45, 23, 78, 12, 56, 89, 34],
           [32, inf, 67, 43, 90, 21, 76, 54],
           [11, 88, inf, 36, 65, 44, 22, 99],
           [55, 33, 81, inf, 77, 13, 66, 47],
           [25, 60, 38, 92, inf, 50, 84, 16],
           [73, 28, 52, 40, 69, inf, 37, 91],
           [80, 19, 71, 58, 49, 30, inf, 62],
           [68, 95, 26, 83, 17, 53, 70, inf]]
arc_map2 = [[inf,1,2],[1,inf,3],[2,3,inf]]
mst=MST_Prim(arc_map,list(range(len(arc_map))))
r=mst.search()
print(r)




