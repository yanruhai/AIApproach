import numpy as np
import abc



# 定义抽象基类
class BFS(abc.ABC):  # iterative lengthening search
    init_state = None
    goal=None
    path=[]

    def __init__(self, init_state,goal=None):
        self.init_state = init_state
        self.goal=goal

    @abc.abstractmethod
    def actions(self,state):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def goal_test(self, state):
        """获得状态可以使用的action列表"""
        pass

    def __frontier_explored_test(self,frontier,explored_set,state):
            for temp in frontier:
                if temp==state:
                    return False
            for temp in explored_set:
                if temp==state:
                    return False
            return True

    def search(self):
        self.path.append(self.init_state)
        if self.goal_test(self.init_state):
            return
        frontier = []
        explored_set = []
        single_path = []
        frontier.append(self.init_state)
        while len(frontier)>0:
            cur_state=frontier.pop(0)#出队
            single_path.append(cur_state)
            explored_set.append(cur_state)
            action_list=self.actions(cur_state)#获得后继节点的action
            for act in action_list:
                state=self.result(cur_state,act)
                if self.__frontier_explored_test(frontier,explored_set,state):#该节点未访问过
                    if self.goal_test(state):
                        single_path.append(state)
                        return single_path
                    else:
                        frontier.append(state)
            #single_path.pop()

    @abc.abstractmethod
    def result(self,state,act):
        """获得action后的状态"""
        pass