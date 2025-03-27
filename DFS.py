import numpy as np
import abc
from search import ExploredSet,Node,Frontier

class DFS(abc.ABC):
    init_state = None
    goal = None
    path = []

    def __init__(self, init_state, goal=None):
        self.init_state = init_state
        self.goal = goal

    @abc.abstractmethod
    def actions(self, state):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def goal_test(self, state):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def init_exploredset(self):
        """获得状态可以使用的action列表"""
        pass

    def __frontier_explored_test(self, frontier, explored_set, state):
        t=frontier.check(state)
        if not t: return False
        t = explored_set.check(state)
        if not t: return False
        return True

    def search(self):
        self.path.append(self.init_state)
        if self.goal_test(self.init_state):
            return
        frontier = Frontier(True)
        explored_set = self.init_exploredset()
        single_path = []
        frontier.put_state(self.init_state)
        cur_node = Node(self.init_state)  # 树根
        single_path.append(cur_node)
        count = 0
        found_result = []
        while len(frontier) > 0:
            count += 1
            if count % 1000 == 0:
                print(f"frontier:{len(frontier)}")
            cur_state = frontier.pop()  # 出队
            cur_node = single_path.pop()  # 出队
            explored_set.put(cur_state)
            action_list = self.actions(cur_state)  # 获得后继节点的action
            for act in action_list:
                state = self.result(cur_state, act)
                if self.__frontier_explored_test(frontier, explored_set, state):  # 该节点未访问过
                    if self.goal_test(state):
                        child_node = Node(state, cur_node)
                        found_result.append(child_node)
                        #return found_result
                    else:
                        frontier.put_state(state)
                        child_node = Node(state, cur_node)
                        single_path.append(child_node)
                        cur_node.add_child(child_node)
        return found_result

    @abc.abstractmethod
    def result(self, state, act):
        """获得action后的状态"""
        pass
