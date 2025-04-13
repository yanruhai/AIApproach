import random
import math


def conflicts(board):
    """计算对角线冲突数（假设 board 是排列，无行/列冲突）"""
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(board[i] - board[j]):
                count += 1
    return count


def get_neighbor(board, T, T0):
    """生成邻居，通过交换两行保持排列性质"""
    n = len(board)
    new_board = board.copy()

    # 随机选择两行交换
    i, j = random.sample(range(n), 2)
    new_board[i], new_board[j] = new_board[j], new_board[i]

    # 可选：高温时更多随机性，低温时优化选择
    if T <= T0 / 10:
        # 选择高冲突行
        row_conflicts = [0] * n
        for i in range(n):
            for j in range(n):
                if i != j and abs(i - j) == abs(new_board[i] - new_board[j]):
                    row_conflicts[i] += 1#计算每个元素的冲突数量
        max_conflict_rows = [i for i in range(n) if row_conflicts[i] == max(row_conflicts)]
        i = random.choice(max_conflict_rows)
        j = random.choice([k for k in range(n) if k != i])
        new_board[i], new_board[j] = new_board[j], new_board[i]

    return new_board


def simulated_annealing(n):
    """模拟退火解决 n 皇后问题"""
    # 初始化为 0 到 n-1 的随机排列
    board = list(range(n))
    random.shuffle(board)
    current_conflicts = conflicts(board)

    # 参数
    T0 = 5000.0
    T = T0
    alpha = 0.999993
    max_iterations = 500000

    for i in range(max_iterations):
        if current_conflicts == 0:
            # 验证 board 是排列
            if len(set(board)) == n:
                return board
        neighbor = get_neighbor(board, T, T0)
        neighbor_conflicts = conflicts(neighbor)
        delta = neighbor_conflicts - current_conflicts
        if delta <= 0 or random.random() < math.exp(-delta / T):
            board = neighbor
            current_conflicts = neighbor_conflicts
        T *= alpha

    return None


# 测试 n=100
n = 1000
board = simulated_annealing(n)
if board:
    print("Board (row -> col):", board)
    print("My conflicts:", conflicts(board))  # 应为 0
    print("Is permutation:", len(set(board)) == n)  # 应为 True
else:
    print("No solution found")