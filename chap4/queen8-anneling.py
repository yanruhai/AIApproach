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
    def objective_function(self,state)->Union[int, float]:
        '''目标函数,返回函数值'''
        pass

    @abstractmethod
    def get_next_state(self) :
        '''获得领域状态'''
        pass


class SimulatedAnnealing:


    def simulated_annealing(self, initial_state, initial_temperature, cooling_rate, max_iterations, search_obj:SearchQuestion):
        """
        模拟退火算法实现
        :param initial_state: 初始状态
        :param initial_temperature: 初始温度
        :param cooling_rate: 冷却率
        :param max_iterations: 最大迭代次数
        :return: 最优状态
        """
        current_state = initial_state
        current_energy = search_obj.objective_function(current_state)
        best_state = current_state
        best_energy = current_energy
        temperature = initial_temperature

        for i in range(max_iterations):
            print(f"iter={i}")
            # 生成一个邻域状态
            neighbor_state = search_obj.get_next_state()
            # 确保邻域状态在区间 [-10, 10] 内

            neighbor_energy = search_obj.objective_function(neighbor_state)

            # 计算能量差
            delta_energy = neighbor_energy - current_energy

            # 判断是否接受邻域状态
            if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
                current_state = neighbor_state
                current_energy = neighbor_energy

            # 更新最优状态
            if current_energy < best_energy:
                best_state = current_state
                best_energy = current_energy

            # 降温
            temperature *= cooling_rate

        return best_state



# 运行模拟退火算法
#best_solution = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,None)
#print(f"最优解: {best_solution}")
#print(f"最优值: {sa.objective_function(best_solution)}")

class QueeAnneal(Queen, SearchQuestion):
    sa=SimulatedAnnealing()

    def get_next_state(self):
        select_list = []
        for i in arange(self.limit):
            for j in arange(self.limit):
                if not self.queens[i] == j:
                    temp = copy.copy(self.queens)
                    temp[i] = j
                    select_list.append(temp)

        k = random.randint(0, self.limit**2-self.limit-1)  # 选中k做为当前动作
        self.queens = select_list[k]
        return self.count_attacking_pairs()

    def objective_function(self, state):
        return self.count_attacking_pairs()






k=8
random.seed=21
q = [random.randint(0, k-1) for _ in range(k)]
#q=[1,1,1,1,1,1,1,1]
qu=QueeAnneal(k,q)

initial_state = random.uniform(-10, 10)
initial_temperature = 100
cooling_rate = 0.95
max_iterations = 10000
sa=SimulatedAnnealing ()
best_solution = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,qu)
print(f"最优解: {best_solution}")
print(qu.queens)

