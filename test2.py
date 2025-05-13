import random

import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

# 先验：Beta(1,1)，均匀分布
a, b = 1, 1
# 观测：10次抛硬币，6次正面
heads, total = 6, 10
# 后验：Beta(a + heads, b + total - heads)
posterior = beta(a + heads, b + total - heads)

x = np.linspace(0, 1, 100)
plt.plot(x, posterior.pdf(x), label='Posterior')
plt.plot(x, beta(a, b).pdf(x), label='Prior')
plt.legend()
plt.show()