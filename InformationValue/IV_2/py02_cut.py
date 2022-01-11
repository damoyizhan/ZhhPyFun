# coding: utf-8
"""
 目标： 对数据进行分箱
"""
import os
import sys
import pandas as pd
from pprint import pprint

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("iv_analysis") + len("iv_analysis")]
sys.path.append(rootPath)

from py01_data import df

# 等频分箱
# cut 前确认事项
# 1.确定分箱数量
# 2.确定分箱值

df['cut_group_xf'] = pd.cut(df['xf'], bins=4, precision=0)
df['cut_group_xi'] = pd.cut(df['xi'], bins=4, precision=0)

# 枚举类型的，枚举值即为分箱值，不做cut
# 下面这段代码有误，无法cut varchar 类型的 枚举值
# df['cut_group_xv'] = pd.cut(df['xv'], bins=4)  # varchar 类型不适用 precision参数

df['cut_group_xv'] = '[' + df['xv'] + ']'

# TODO: 合并小分箱，连续分箱需要连续合并，枚举分箱可以小+小合并

# 过滤，只保留分箱结果，去掉原始值
df = df.filter(items=['cut_group_xf', 'cut_group_xi', 'cut_group_xv', 'y'])
# pprint(df)
