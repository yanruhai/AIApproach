import cv2
import numpy as np

# ========== 场景1：直接用自定义二维灰度矩阵 ==========
# 手动定义一个5×5的二维灰度矩阵（模拟小图像，值范围0-255）
gray_matrix = np.array([
    [120, 122, 121, 123, 120],
    [121, 150, 152, 151, 122],
    [120, 151, 180, 150, 121],
    [122, 150, 152, 151, 123],
    [121, 123, 122, 121, 120]
], dtype=np.uint8)  # 必须是uint8类型（符合图像像素值格式）

# ========== 场景2：从图片读取并转为二维灰度矩阵 ==========
# img = cv2.imread("your_image.jpg")
# gray_matrix = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成二维灰度矩阵


sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float32)

# 对二维矩阵执行卷积锐化
# 参数-1表示输出矩阵的深度和输入一致（uint8）
sharpened_matrix = cv2.filter2D(gray_matrix, -1, sharpen_kernel)

# 打印结果对比
print("原始二维灰度矩阵：")
print(gray_matrix)
print("\n锐化后的二维矩阵：")
print(sharpened_matrix)