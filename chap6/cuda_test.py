import numpy as np
from numba import cuda

# ==============================
# 🔥 显卡核函数：检查数组是否有重复元素
# ==============================
@cuda.jit
#如果有临时变量，是放到cuda内核里
def check_duplicate_gpu(data, results):
    # 每个线程负责检查 1 个元素
    idx = cuda.grid(1)
    #x, y = cuda.grid(2) 二维坐标,同一个线程内
    '''threads = (16, 16)   # 小组：16x16
blocks = (
    (mat.shape[0] + threads[0] - 1) // threads[0],
    (mat.shape[1] + threads[1] - 1) // threads[1]
)'''

    # 不越界
    if idx < data.size:
        current = data[idx]

        # 检查前面所有元素是否重复
        for i in range(idx):
            if data[i] == current:
                results[idx] = 1  # 标记重复
                return

        results[idx] = 0  # 不重复

# ==============================
# 主程序：调用显卡查重
# ==============================
if __name__ == "__main__":
    # 你的数据（列表转 numpy）
    data = np.array([1, 5, 3, 5, 9, 2], dtype=np.int32)

    # 结果数组：每个位置标记是否重复
    results = np.zeros_like(data)

    # 配置显卡线程，每个block内的线程数
    '''可以定的线程数,必须要<=1024,threads_per_block = 32
threads_per_block = 64
threads_per_block = 128
threads_per_block = 256
threads_per_block = 512
threads_per_block = 1024'''
    threads_per_block = 128
    blocks = (data.size + threads_per_block - 1) // threads_per_block

    # 传到显卡,check_duplicate_gpu函数在显卡上运行，所有参数需要放到显卡(cuda)内
    d_data = cuda.to_device(data)
    d_res = cuda.to_device(results)

    # [blocks, threads_per_block]表示告诉显卡有几个小组，每个小组多少线程
    check_duplicate_gpu[blocks, threads_per_block](d_data, d_res)

    # 结果拷回 CPU
    final_res = d_res.copy_to_host()

    # 输出
    print("数据：", data)
    print("重复标记：", final_res)
    print("是否存在重复：", np.any(final_res == 1))