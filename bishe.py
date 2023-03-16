import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import SGDRegressor
# Fixing random state for reproducibility 
np.random.seed(19680801)
N =100 #3, 10(点的个数)
x = np.random.rand(N)#随机数
y = x+ 0.1*np.random.rand(N)#0.1*随机噪声
colors = np.random.rand(N)

#截距值为 a，斜率为 b 
#线性回归 计算 Pearson 相关系数
#  r （rvalue = 0.72）、
# p 值（pvalue = 3.42e-06）、
# 斜率 b 的标准偏差 （stderr = 3.85e-06）
# 以及截距项 a (intercept_stderr = 0.15)
a,b,r_value, p_value,std_err = stats.linregress(x, y)

plt.plot(x, a*x+b, label= "scipy.stats.linregress (MSE)")

linear_model = SGDRegressor(loss="epsilon_insensitive", epsilon=0)
x=np.array(x)
y=np.array(y)
linear_model.fit(x.reshape([-1,1]), y)
a = linear_model.coef_[0]
b = linear_model.intercept_[0]

plt.plot(x,a*x+b, label="sklearn.linear_model.SGDRegressor (MAE)")

#画图
plt.scatter(x,y, c=[[44/255,160/255, 4/255]]* N, alpha=0.5)
plt.legend()
plt.show()