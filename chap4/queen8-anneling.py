import math
import random
from abc import abstractmethod

from queen8 import  Queen
import abc

class ObjectFunction(abc.ABC):
    @abstractmethod
    def objective_function(self,state):
        pass


class SimulatedAnnealing:


    def simulated_annealing(self,initial_state, initial_temperature, cooling_rate, max_iterations,objective_function:ObjectFunction):
        """
        模拟退火算法实现
        :param initial_state: 初始状态
        :param initial_temperature: 初始温度
        :param cooling_rate: 冷却率
        :param max_iterations: 最大迭代次数
        :return: 最优状态
        """
        current_state = initial_state
        current_energy = objective_function.objective_function(current_state)
        best_state = current_state
        best_energy = current_energy
        temperature = initial_temperature

        for _ in range(max_iterations):
            # 生成一个邻域状态
            neighbor_state = current_state + random.uniform(-1, 1)
            # 确保邻域状态在区间 [-10, 10] 内
            neighbor_state = max(-10, min(neighbor_state, 10))
            neighbor_energy = objective_function.objective_function(neighbor_state)

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


# 参数设置
initial_state = random.uniform(-10, 10)
initial_temperature = 100
cooling_rate = 0.95
max_iterations = 1000
sa=SimulatedAnnealing ()
# 运行模拟退火算法
best_solution = sa.simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations)
print(f"最优解: {best_solution}")
print(f"最优值: {sa.objective_function(best_solution)}")

class QueeAnneal(Queen,ObjectFunction):
    sa=SimulatedAnnealing()

    def objective_function(self, state):
        pass

    def search(self):
        pass


k=100
random.seed=21
q = [random.randint(0, k-1) for _ in range(k)]
#q=[1,1,1,1,1,1,1,1]
qu=Queen(k,q)
q=qu.search()
print(q)