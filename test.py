import math
import random


def objective_function(x):
    # 示例目标函数，这里使用简单的二次函数
    return x ** 2


def simulated_annealing(initial_solution, initial_temperature, cooling_rate, max_iterations):
    current_solution = initial_solution
    current_energy = objective_function(current_solution)
    best_solution = current_solution
    best_energy = current_energy
    temperature = initial_temperature

    for _ in range(max_iterations):
        # 生成邻域解
        neighbor_solution = current_solution + random.uniform(-1, 1)
        neighbor_energy = objective_function(neighbor_solution)

        # 计算能量差
        delta_energy = neighbor_energy - current_energy

        # 判断是否接受邻域解
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
            current_solution = neighbor_solution
            current_energy = neighbor_energy

        # 更新最优解
        if current_energy < best_energy:
            best_solution = current_solution
            best_energy = current_energy

        # 降温
        temperature *= cooling_rate

    return best_solution, best_energy


# 参数设置
initial_solution = random.uniform(-10, 10)
initial_temperature = 100
cooling_rate = 0.95
max_iterations = 1000

# 运行模拟退火算法
best_solution, best_energy = simulated_annealing(initial_solution, initial_temperature, cooling_rate, max_iterations)

print(f"最优解: {best_solution}")
print(f"最优值: {best_energy}")
