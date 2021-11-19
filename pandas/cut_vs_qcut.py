# 比较 cut 和 qcut 的区别

# cut方法 ，官网链接：http://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html
# qcut方法，官网链接：http://pandas.pydata.org/pandas-docs/stable/generated/pandas.qcut.html


# 区别1：
#  cut  的关键词是 discrete intervals，等距 等宽
#  qcut 的关键词是 Quantile-based    ，等频 等比

# 举例：
# 一群人长跑，跑最快的人用了60分钟，跑最慢的人用了100分钟，现在要求把这堆人的成绩分为4组；
# cut  的分箱，是[67,70] ,  (70,80],  (80,90], (90,100]
# qcut 的分箱，是[0%,25%],(25%,50%],(50%,75%],(75%,100]

# 代码验证：
# 代码验证：step1： 造案例数据 100个人跑长跑，用时从60分钟到100分钟不等，用时遵循正态分布（Normal distribution）
from pprint import pprint
import pandas as pd
import numpy as np
import random

# 数据集
# 均匀分布（Uniform Distribution）
uniformDist = np.random.randint(low=60, high=100, size=50, dtype='int')

# 一维度 ndarray 转 list ，添加边界值，目的是为了让边界值更清晰
uniformDist = uniformDist.tolist()
uniformDist.append(60)
uniformDist.append(100)

uniformDist_cut = pd.cut(uniformDist,  # 必填项  , 被cut 的数据对象,只能cut 一列
                         bins=4,  # 必填项  , cut 的分箱数
                         precision=0  # 非必填项,  分箱边界值精确度，0 代表整数
                         )
uniformDist_qcut = pd.qcut(uniformDist,  # 必填项  , 被cut 的数据对象,只能cut 一列
                           q=4,  # 必填项  , cut 的分箱数
                           precision=0  # 非必填项,  分箱边界值精确度，0 代表整数
                           )

print("---------------uniformDist------------------------------------------")
print("均匀分布成绩   %s " % uniformDist)
print("cut  分箱categories  %s " % uniformDist_cut.categories)
print("qcut 分箱categories  %s " % uniformDist_qcut.categories)

print("cut  分箱codes %s " % uniformDist_cut.codes)
print("qcut 分箱codes %s " % uniformDist_qcut.codes)

print("cut  分箱ordered %s " % uniformDist_cut.ordered)
print("qcut 分箱ordered %s " % uniformDist_qcut.ordered)


print("cut  分箱labels %s " % uniformDist_cut.labels)
print("qcut 分箱labels %s " % uniformDist_qcut.labels)


print("---------------------------------------------------------")

#
# a.__add__(60)
# a.__add__(100)
# print("100个人的跑步成绩 %s" % uniformDist)
#
# # a_df = pd.DataFrame(a)
#
