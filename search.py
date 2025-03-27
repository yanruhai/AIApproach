import numpy as np
import abc

class State:
    id=0#用于标识状态，如果无法确定，可以在搜索的时候自增

    def get_id(self):
        return self.id


class Node:
    children=[]
    parent=None
    state=None
    def get_id(self):
        return self.state.get_id()

    def get_num(self):
        return self.state.get_num()

    def __str__(self):
            return f"{self.state.get_num()}"

    def __init__(self,state,parent=None):
        self.state=state
        self.parent=parent

    def add_child(self,child):
        self.children.append(child)


class ExploredSet(abc.ABC):
    expl={}

    @abc.abstractmethod
    def put(self, state):
        """获得状态可以使用的action列表"""
        pass

    @abc.abstractmethod
    def check(self,state):
        pass

class Frontier(abc.ABC):
    state_list=[]
    use_dict = False
    dict_for_check = {}  # 用于check的哈希表,可以不使用

    def __len__(self):
        return len(self.state_list)

    def __init__(self,use_dict=False):
        self.use_dict=use_dict

    def check(self,state):
        """测试state是否在数据集中"""
        if self.use_dict:
            if state.get_id() in self.dict_for_check:
                return False
        else:
            for temp in self.state_list:
                if temp == state:
                    return False
        return True

    def put_state(self, state):
        self.state_list.append(state)

    def pop(self,ind=None):
      if ind is None:
          return self.state_list.pop()
      return  self.state_list.pop(ind)