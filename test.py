import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 生成一些示例数据
np.random.seed(0)
X = np.linspace(0, 10, 100)
y = 2 * X + 1 + np.random.normal(0, 1, 100)

# 添加常数项
X = sm.add_constant(X)

# 拟合线性回归模型
model = sm.OLS(y, X).fit()

# 获取studentized残差
studentized_residuals = model.get_influence().resid_studentized_internal

# 绘制Studentize图
plt.scatter(model.fittedvalues, studentized_residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Studentized Residuals')
plt.title('Studentized Residuals Plot')
plt.show()