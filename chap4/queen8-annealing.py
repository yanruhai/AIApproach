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
    def objective_function(self,neighbor_step_nums)->Union[int, float]:
        '''目标函数,调整状态并返回函数值'''
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
        current_energy = search_question.objective_function(current_state)
        best_state = current_state
        best_energy = current_energy
        temperature = initial_temperature
        unit_step=10/k_discrete
        for _ in range(max_iterations):
            step=random.uniform(-1, 1)
            neighbor_state_float = current_state + step#获得随机值
            neighbor_state_float = max(-10, min(neighbor_state_float, 10))
            neighbor_step_nums=round(abs(neighbor_state_float)/unit_step)#获得需要变化的块数
            neighbor_energy =search_question.objective_function(neighbor_step_nums)
            if search_question.goal_check():
                return search_question.get_cur_state()
            delta_energy = neighbor_energy - current_energy
            if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
                current_state = neighbor_state_float
                current_energy = neighbor_energy

            if current_energy < best_energy:
                best_state = current_state
                best_energy = current_energy

            temperature *= cooling_rate

        return best_state



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
        self.tune_random(neighbor_step_nums)
        return self.count_attacking_pairs()






k=8
random.seed=21
q = [random.randint(0, k-1) for _ in range(k)]
#q=[1,1,1,1,1,1,1,1]
qu=QueeAnneal(k,q)

initial_state = 0
initial_temperature = k**2*50
cooling_rate = 0.95
max_iterations = 10000
sa=SimulatedAnnealing ()
best_solution = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,qu,k)
print(f"最优解: {best_solution}")
print(qu.queens)

