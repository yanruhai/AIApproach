import numpy as np
import abc

class State:
    id=0#用于标识状态，如果无法确定，可以在搜索的时候自增
    data=None#存放数据的字段，可以是表格或整数
    def get_id(self):
        return self.id

    def set_id(self, d):
        self.id = d



class Node:
    children=[]
    parent=None
    state=None
    def get_id(self):
        return self.state.get_id()

    def get_num(self):
        return self.state.get_num()

    def __str__(self):
            return f"{self.state.get_id()}"

    def __init__(self,state,parent=None):
        self.state=state
        self.parent=parent

    def add_child(self,child):
        self.children.append(child)


class ExploredSet(abc.ABC):
    expl={}

    def __len__(self):
        return len(self.expl)

    def put(self, state):
        self.expl[state.get_id()]=state


    def check(self,state):
        if state.get_id() in self.expl:
            return False
        return True

class Frontier(abc.ABC):
    state_list=[]
    use_dict = True
    dict_for_check = {}  # 用于check的哈希表,可以不使用
    last_op=None#调试用
    def check_for_debug(self):
        for ind,t in enumerate(self.state_list):
            for ind2, t2 in enumerate(self.state_list):
                if t.get_id()==t2.get_id() and ind!=ind2 :
                    print()
        if len(self.state_list)!=len(self.dict_for_check):
            print(self.last_op)



    def __len__(self):
        return len(self.state_list)

    def __init__(self,use_dict=False):
        self.last_op=self.__init__
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
        self.last_op =self.put_state
        self.state_list.append(state)
        self.dict_for_check[state.get_id()]=state

    def pop(self,ind=None):
      if ind is None:
          t= self.state_list.pop()
          self.dict_for_check.pop(t.get_id())
          return t
      t=  self.state_list.pop(ind)
      self.dict_for_check.pop(t.get_id())

      return t