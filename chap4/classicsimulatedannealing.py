import numpy as np
import math


# 目标函数：f(x) = x^2，目标是找到使 f(x) 最小的 x
def objective_function(x):
    return x ** 2


# 经典模拟退火算法for discrete
def classic_simulated_annealing(initial_x, initial_temp, cooling_rate, min_temp, max_iterations,num):
    '''num为离散情况下的分类数量，[0,temp*0.1/num],[temp*0.1/num,temp*0.2/num]...,'''
    # 初始化当前解
    x_current = initial_x
    f_current = objective_function(x_current)

    # 记录最优解
    x_best = x_current
    f_best = f_current

    # 当前温度
    temp = initial_temp
    iteration = 0
    unit_for_discrete=(temp*0.1)/num
    while temp > min_temp and iteration < max_iterations:
        # 基于当前温度生成扰动幅度
        # 高温时扰动幅度大，低温时扰动幅度小
        perturbation_scale = temp * 0.1  # 扰动幅度与温度成正比
        perturbation = np.random.uniform(0, perturbation_scale)
        perturbation_for_discrete=perturbation/unit_for_discrete
        #x_new = x_current + perturbation

        # 计算新解的目标函数值
        f_new = objective_function(perturbation_for_discrete)

        # 计算能量差
        delta_E = f_new - f_current

        # Metropolis 准则：如果新解更优，或者以一定概率接受较差的解
        if delta_E < 0 or np.random.rand() < math.exp(-delta_E / temp):
            x_current = x_new
            f_current = f_new

            # 更新最优解
            if f_current < f_best:
                x_best = x_current
                f_best = f_current

        # 降低温度（几何冷却）
        temp *= cooling_rate
        iteration += 1

        # 打印当前状态
        print(f"Iteration {iteration}: x_current = {x_current:.6f}, f_current = {f_current:.6f}, temp = {temp:.6f}")

    return x_best, f_best


# 设置参数
initial_x = 10.0  # 初始解
initial_temp = 1000.0  # 初始温度
cooling_rate = 0.99  # 冷却速率
min_temp = 1e-3  # 最小温度
max_iterations = 1000  # 最大迭代次数

# 运行模拟退火算法
best_x, best_f = classic_simulated_annealing(initial_x, initial_temp, cooling_rate, min_temp, max_iterations)

# 打印结果
print(f"\nBest solution found: x = {best_x:.6f}, f(x) = {best_f:.6f}")