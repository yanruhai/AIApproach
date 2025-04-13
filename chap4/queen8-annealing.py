import copy
import math
import random
from abc import abstractmethod
from typing import Union

from numpy.ma.core import arange

from queen8 import  Queen
import abc

class SearchQuestion(abc.ABC):
    '''目标函数，需要实现的方法,'''
    @abstractmethod
    def objective_function(self,neighbor_step_nums):
        '''目标函数,调整状态并返回函数值,需要copy一个新对象后操作,返回元组，包括两个元素'''
        pass

    @abstractmethod
    def goal_check(self):
        '''检测是否已经有解'''
        pass

    @abstractmethod
    def get_cur_state(self):
        pass


class SimulatedAnnealing:

    def simulated_annealing(self,initial_state, initial_temperature, cooling_rate, max_iterations,search_question:SearchQuestion,k_discrete):
        '''k_discrete是分块的数量,8皇后里是8'''
        current_state = initial_state
        best_search_question,current_energy = search_question.objective_function(current_state)
        best_state = current_state
        best_energy = current_energy
        temperature = initial_temperature
        unit_step=1/k_discrete
        for _ in range(max_iterations):
            step=random.uniform(-1, 1)
            step_discrete=max(1,round(abs(step/unit_step)+1)%k_discrete)
            neighbor_state_float = current_state + step#获得随机值
            neighbor_state_float = max(-10, min(neighbor_state_float, 10))
            temp_search_question,neighbor_energy =search_question.objective_function(step_discrete)
            #print(f"step={step_discrete}")
            if temp_search_question.goal_check():
                return temp_search_question.get_cur_state(),neighbor_energy
            delta_energy = neighbor_energy - current_energy
            if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):#要是 delta_energy 小于 0，就意味着相邻状态的能量比当前状态的能量更低。在这种情况下，新状态是更优的，所以直接接受这个新状态
                current_state = neighbor_state_float
                current_energy = neighbor_energy
                search_question=temp_search_question

            if current_energy < best_energy:
                best_state = current_state
                best_energy = current_energy
                best_search_question = copy.deepcopy(search_question)
            temperature *= cooling_rate

        return best_search_question.get_cur_state(),best_energy



# 运行模拟退火算法
#best_solution = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,None)
#print(f"最优解: {best_solution}")
#print(f"最优值: {sa.objective_function(best_solution)}")

class QueeAnneal(Queen, SearchQuestion):
    sa=SimulatedAnnealing()

    def get_cur_state(self):
        return self.queens

    def __get_next_state(self,neighbor_step_nums):
        '''select_list = []
        for i in arange(self.limit):
            for j in arange(self.limit):
                if not self.queens[i] == j:
                    temp = copy.copy(self.queens)
                    temp[i] = j
                    select_list.append(temp)

        k = random.randint(0, self.limit**2-self.limit-1)  # 选中k做为当前动作
        self.queens = select_list[k]
        return self.count_attacking_pairs()'''


    def objective_function(self, neighbor_step_nums):
        qa= QueeAnneal(self.limit,self.queens)
        qa.tune_random(neighbor_step_nums)
        return qa,qa.count_attacking_pairs()






k=100
random.seed=21
q = [random.randint(0, k-1) for _ in range(k)]
#q=[1,1,1,1,1,1,1,1]

qu=QueeAnneal(k,q)
print(f"初始状态{qu.score}")
initial_state = 0
initial_temperature = 2000
cooling_rate = 0.9995
max_iterations = 500000
sa=SimulatedAnnealing ()
score=1
while score!=0:
    qu.tune_random(k)
    best_solution,score = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,qu,k)
    print(f"最优解: {best_solution}")
    print(best_solution)
    q=Queen(k,best_solution)
    print(q.score)

