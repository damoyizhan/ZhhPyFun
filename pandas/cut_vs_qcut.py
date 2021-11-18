# 比较 cut 和 qcut 的区别

# qcut方法，官网链接：http://pandas.pydata.org/pandas-docs/stable/generated/pandas.qcut.html
# cut方法 ，官网链接：http://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html

# 区别1：
#  cut  的关键词是 discrete intervals，即固定切分：间隔固定  ，等距切分，
#  qcut 的关键词是 Quantile-based    ，即分位切分：间隔不固定 ，按照排名切分

# 举例：
# 50个人 跑长跑，用时从60分钟到100分钟不等，分为4组
# cut  的拆分逻辑，是用时 60-70分钟的一组，70-80分钟的一组，80-90分钟的一组，90-100分钟的一组；
# qcut 的拆分逻辑，是排名 前25%的一组，25%-50%的一组，50%-75%的一组，75% 以后的一组；


# 代码验证：
# 代码验证：step1： 造案例数据 100个人跑长跑，用时从60分钟到100分钟不等，用时遵循正态分布（Normal distribution）

import pandas as pd
import numpy as np
import random

# 数据集
# 均匀分布（Uniform Distribution）
uniformDist = np.random.randint(low=60, high=100, size=50, dtype='int')

print(uniformDist)

print(uniformDist.__dict__)

# a.__add__(60)
# a.__add__(100)


# print("100个人的跑步成绩 %s" % uniformDist)
#
# # a_df = pd.DataFrame(a)
#
# cut_bins = pd.cut(uniformDist,  # 必填项  , 被cut 的数据对象,只能cut 一列
#                   bins=4,  # 必填项  , cut 的分箱数
#                   precision=0  # 非必填项,  分箱边界值精确度，0 代表整数
#                   )
#
# print("cut 分箱 结果 %s " % cut_bins)
#
# qcut_bins = pd.qcut(uniformDist,  # 必填项  , 被cut 的数据对象,只能cut 一列
#                     q=4,  # 必填项  , cut 的分箱数
#                     precision=0  # 非必填项,  分箱边界值精确度，0 代表整数
#                     )
#
# print("qcut 分箱 结果 %s " % qcut_bins)
