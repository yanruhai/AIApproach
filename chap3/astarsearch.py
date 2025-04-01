import numpy as np
import abc
from search import ExploredSet, Node, Frontier,State
from typing import TypeVar, Generic, override
from collections import Counter

class AStarState(State):
    fvalue = 0
    gvalue=0
    hvalue=0
    hfunction=None#heu函数，默认为空,参数为goal,cur_state,应传入partial带有goal对象
    def __init__(self,hfunction=None):
        self.hfunction=hfunction
    def set_hfunction(self,hfunction):
        self.hfunction=hfunction
        self.hvalue=hfunction(self)
        self.__compute_fvalue()

    def get_fvalue(self):
        return self.fvalue

    def __compute_fvalue(self):
        self.hvalue=0
        if  not self.hfunction is None:
            self.hvalue=self.hfunction(self)
        self.fvalue=self.get_hvalue()+self.get_gvalue()

    def get_hvalue(self):
      return self.hvalue

    def get_gvalue(self):
        return self.gvalue
    def set_gvalue(self,gvalue):
        self.gvalue=gvalue
        self.__compute_fvalue()



# 定义类型变量并添加约束
T = TypeVar('T', bound=AStarState)
class OrderedFrontier(Frontier,Generic[T]):

    @override
    def put_state(self,state:T):
        '''插入新的状态进入frontier队列'''
        self.use_dict=True
        i=len(self.state_list)-1
        if len(self.state_list)==0:
            self.state_list.append(state)
            self.dict_for_check[state.get_id()] = state
            return
        while i >= 0 and state.get_fvalue()<self.state_list[i].get_fvalue():
            i=i-1
        if i+1<len(self.state_list):
            self.state_list.insert(i+1,state)#插入数据
        else:
            self.state_list.append(state)
        self.dict_for_check[state.get_id()]=state




    def get_state_dict(self,state):
        return self.dict_for_check.get(state.get_id())

    def update(self,state):
        '''将state状态更新到队列里，前提是该状态在队列中'''
        ind=0
        k=None
        for ind,k in enumerate(self.state_list):
            if k==state:
                break
        self.state_list.pop(ind)
        self.put_state(state)
        self.dict_for_check[state.get_id()]=state





# 定义抽象基类
class AstarSearch(abc.ABC,Generic[T]):  # iterative lengthening search
    init_state = None
    goal=None
    path=[]

    def __init__(self, init_state:T,goal=None):
        self.init_state = init_state
        self.goal=goal


    @abc.abstractmethod
    def actions(self,state:T):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def goal_test(self, state:T):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def init_exploredset(self):
        """获得状态可以使用的action列表"""
        pass

    def __frontier_explored_test(self,frontier,explored_set,state:T):

            t = frontier.check(state)
            if not t: return False
            t=explored_set.check(state)
            if not t: return False
            return True


    def __print_frontier__(self,frontier):
        for k in frontier.state_list:
            print(f"id={k.get_id()}",end='')
        print()

    def __check_frontier(self,frontier):
        temp_map={}
        c_count=0
        for k in frontier.state_list:
            if k.get_id() in temp_map:
                c_count+=1
            else: temp_map[k.get_id()]=k
        print(f"重复={c_count}")

    def search(self):
        self.path.append(self.init_state)
        if self.goal_test(self.init_state):
            return
        frontier = OrderedFrontier()
        explored_set = self.init_exploredset()
        single_path = []#用于保存结果树结构
        frontier.put_state(self.init_state)
        cur_node = Node(self.init_state)#树根
        single_path.append(cur_node)
        count=0
        nodes= {}
        found_result={}#解集合
        nodes[cur_node.get_id()]=cur_node
        while len(frontier)>0:
            count+=1
            if count%1000==0:
                print(f"frontier:{len(frontier)}")
            cur_state=frontier.pop(0)#出队
            #print(f"检测{cur_state.get_id()}")
            cur_node=nodes[cur_state.get_id()]
            if self.goal_test(cur_state):#判断是否是解
                found_result[cur_state.get_id()]= cur_node
                #return cur_node
            else:
                explored_set.put(cur_state)
                action_list=self.actions(cur_state)#获得后继节点的action
                for act in action_list:
                    state=self.result(cur_state,act)
                    if self.__frontier_explored_test(frontier,explored_set,state):#该节点未访问过
                            child_node = Node(state, cur_node)
                            nodes[state.get_id()]=child_node
                            frontier.put_state(state)
                    else:
                            already_in=frontier.get_state_dict(state)#获得frontier内已有相同id的状态
                            if not already_in is None:
                                if already_in.get_fvalue()>state.get_fvalue():
                                    child_node = Node(state, cur_node)#对已有状态生成新节点，准备更换
                                    #print("更新节点")
                                    nodes[state.get_id()] = child_node  # 更换
                                    frontier.update(state)
        return found_result




    @abc.abstractmethod
    def result(self,state,act):
        """获得action后的状态"""
        pass





