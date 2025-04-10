import math
import random

def objective_function(x):
    return x ** 2 + 3 * x + 5


def simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations,jump_probability=0.1, target_energy=None, tolerance=1e-6):
    current_state = initial_state
    current_energy = objective_function(current_state)
    best_state = current_state
    best_energy = current_energy
    temperature = initial_temperature

    for _ in range(max_iterations):
        # 线性调整：在当前状态基础上，加上一个小的随机值
        # 这里通过 random.uniform(-1, 1) 生成一个 -1 到 1 之间的随机小数
        # 使得新状态是在当前状态附近小范围变动
        neighbor_state_linear = current_state + random.uniform(-1, 1)

        # 跳跃型调整：随机选取一个新的状态，这里直接在 -10 到 10 区间内随机选值
        # 不依赖于当前状态，可能会产生较大幅度的状态改变
        neighbor_state_jump = random.uniform(-10, 10)

        # 根据概率决定使用哪种调整方式
        if random.random() < jump_probability:
            neighbor_state = neighbor_state_jump
        else:
            neighbor_state = neighbor_state_linear

        neighbor_energy = objective_function(neighbor_state)

        delta_energy = neighbor_energy - current_energy
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
            current_state = neighbor_state
            current_energy = neighbor_energy

        if current_energy < best_energy:
            best_state = current_state
            best_energy = current_energy

        # 检查是否达到目标能量
        if target_energy is not None and abs(best_energy - target_energy) <= tolerance:
            print("提前达到目标能量，终止迭代。")
            break

        temperature *= cooling_rate

    return best_state


initial_state = random.uniform(-10, 10)
initial_temperature = 100
cooling_rate = 0.95
max_iterations = 1000

best_solution = simulated_annealing(initial_state, initial_temperature, cooling_rate, max_iterations)
print(f"最优解: {best_solution}")
print(f"最优值: {objective_function(best_solution)}")