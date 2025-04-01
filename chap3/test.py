from typing import TypeVar, Generic

from chap3.search import Frontier, State
from typing import TypeVar, Generic, override

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
            self.state_list.insert(i+1,self.state_list[i])
            i=i-1
        if i+1<len(self.state_list):
            self.state_list.pop(i+1)#删除原数据
            self.state_list.insert(i+1,state)#插入数据
        else:
            self.state_list.append(state)
        self.dict_for_check[state.get_id()]=state
        super().check_for_debug()
        if len(self.state_list)!=len(self.dict_for_check):
            print()


    def get_state_dict(self,state):
        return self.dict_for_check.get(state.get_id())

    def update(self,state):
        '''将state状态更新到队列里，前提是该状态在队列中'''
        ind=0
        k=None
        for ind,k in self.state_list:
            if k==state:
                break
        self.state_list.pop(ind)
        self.put_state(state)
        self.dict_for_check[state.get_id()]=state

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

ou=OrderedFrontier()
s1=My_Astar_State(0,0)
s2=My_Astar_State(1,5)
s3=My_Astar_State(2,1)
s4=My_Astar_State(3,2)
ou.put_state(s1)
ou.put_state(s2)
t=ou.pop(0)
ou.put_state(s3)
t=ou.pop(1)
ou.put_state(s4)
print()

