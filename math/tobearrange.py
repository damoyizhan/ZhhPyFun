# 一维数组的累计求和：
import numpy as np

a = np.random.randint(1, 10, 5)
print(a)

# 一维数组求和，数组所有数字加和
print(a.sum())

# 一维数组累计求和，求数组前 i 个元素的和 即计算 1，1+2，1+2+3，1+2+3+4,......
print(a.cumsum())

