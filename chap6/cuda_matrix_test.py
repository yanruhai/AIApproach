import numpy as np
from numba import cuda

# 二维 GPU 核函数（只处理数字！）
@cuda.jit
def process_2d_matrix(mat):
    # 同一个线程，拿到自己的 (行, 列)
    x, y = cuda.grid(2)

    # 判断是否在 2x2 矩阵范围内
    if x < mat.shape[0] and y < mat.shape[1]:
        # 每个线程填入自己的坐标（数字！）
        mat[x, y] = x * 10 + y  # 填入 0,1,10,11

# ----------------------
# 主程序
# ----------------------
if __name__ == "__main__":
    # 建立 2x2 数字矩阵（必须是数字！）
    mat = np.zeros((2, 2), dtype=np.int32)

    # 拷贝到显卡
    d_mat = cuda.to_device(mat)

    # 二维线程配置
    threads_per_block = (2, 2)
    blocks_per_grid = (1, 1)

    # 运行显卡函数
    process_2d_matrix[blocks_per_grid, threads_per_block](d_mat)

    # 结果拷回 CPU
    result = d_mat.copy_to_host()

    # 打印
    print("2×2 矩阵结果：")
    print(result)