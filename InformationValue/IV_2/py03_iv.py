# coding: utf-8
"""
pip install woe

计算逻辑：
i        = 第i分箱
Y[i]     = 第i分箱 中y=1 的个数
N[i]     = 第i分箱 中y=0 的个数
Y[total] =         y=1 的个数
N[total] =         y=0 的个数
Py[i]    = Y[i] /Y[total] = 第i分箱 中y=1 的个数 / y=1 的个数
Pn[i]    = N[i] /N[total] = 第i分箱 中y=0 的个数 / y=0 的个数
woe[i]   = ln(Py[i]/Pn[i])
iv[i]    = (Py[i]-Pn[i])*woe[i]
iv       = sum(iv[i])

todo 处理变量的分组中出现响应比例为0或100%的情况
"""

import os
import sys
import pandas as pd
import math
from pprint import pprint

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("iv_analysis") + len("iv_analysis")]
sys.path.append(rootPath)

from py02_cut import df


def IV_group(Y_total, N_total, __column, __groupkey):
    """
    计算指定分箱的woe值
    """

    print("==计算 列：" + __column + "   分箱：" + str(__groupkey) + " 的woe 值 ==============================================================")

    Y_i = df.groupby([__column, 'y'])['y'].count()[__groupkey][1]
    N_i = df.groupby([__column, 'y'])['y'].count()[__groupkey][0]
    Py_i = Y_i / Y_total
    PN_i = N_i / N_total
    WOE_i = math.log(Py_i / PN_i)
    IV_i = (Py_i - PN_i) * WOE_i

    print("==Y_i  :" + str(Y_i))
    print("==N_i  :" + str(N_i))
    print("==Py_i :" + str(Py_i))
    print("==PN_i :" + str(PN_i))
    print("==WOE_i:" + str(WOE_i))
    print("==IV_i :" + str(IV_i))
    return IV_i
    # todo /这部分需要改写，按照分组逐个计算woe 效率过低
    # print(y_i)
    # print(y_i[__groupkey][1])
    # print(y_i[__groupkey][0])
    # todo /


def IV_column(Y_total, N_total, __column):
    """
    计算指定列所有分箱的woe值
    """

# 计算逻辑：
# i        = 第i分箱
# Y[i]     = 第i分箱 中y=1 的个数
# N[i]     = 第i分箱 中y=0 的个数
# Y[total] =         y=1 的个数
# N[total] =         y=0 的个数
# Py[i]    = Y[i] /Y[total] = 第i分箱 中y=1 的个数 / y=1 的个数
# Pn[i]    = N[i] /N[total] = 第i分箱 中y=0 的个数 / y=0 的个数
# woe[i]   = ln(Py[i]/Pn[i])
# iv[i]    = (Py[i]-Pn[i])*woe[i]
# iv       = sum(iv[i])

    IV = 0
    for groupkey in df.groupby(__column).groups.keys():
        IV += IV_group(Y_total, N_total, __column, groupkey)

    print("==列：" + __column + " IV值" + str(IV))



pd.set_option('display.max_columns', 1000000)
pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_colwidth', 1000000)
pd.set_option('display.width', 1000000)
print(df)
print("==计算 Y[total] 和 N[total] ==============================================================")
count_total = df.groupby('y')['y'].count()
Y_total = count_total[1]
N_total = count_total[0]

print("count_total  :" + str(count_total) + "\n"
                                            "Y_total :" + str(Y_total) + "\n"
                                                                         "N_total :" + str(N_total) + "\n")

print("==循环计算每一列的WOE ==============================================================")
for column in df.columns:

    # 原始数据列不参与计算
    if not column.startswith("cut_group"):
        continue

    # 计算一个列的woe值
    print("==计算 " + column + " 的woe 值 ==============================================================")
    IV_column(Y_total, N_total, column)

#
#
#
# df['cut_group_xf'] = pd.cut(df['xf'], bins=4, precision=0)
# df['cut_group_xi'] = pd.cut(df['xi'], bins=4, precision=0)
#
# # 枚举类型的，枚举值即为分箱值，不做cut
# # 下面这段代码有误，无法cut varchar 类型的 枚举值
# # df['cut_group_xv'] = pd.cut(df['xv'], bins=4)  # varchar 类型不适用 precision参数
#
# df['cut_group_xv'] = df['xv']
#
# # TODO: 合并小分箱，连续分箱需要连续合并，枚举分箱可以小+小合并
#
#
# # pprint(df)

# 计算每个字段的woe

# pprint(df)

# print(df.__dict__)

# [99 rows x 7 columns]
# {'_is_copy': None, '_mgr': BlockManager
# Items: Index(['xf', 'xi', 'xv', 'y', 'cut_group_xf', 'cut_group_xi', 'cut_group_xv'], dtype='object')
# Axis 1: RangeIndex(start=0, stop=99, step=1)
# NumericBlock: slice(0, 1, 1), 1 x 99, dtype: float64
# NumericBlock: slice(1, 5, 2), 2 x 99, dtype: int64
# ObjectBlock: slice(2, 3, 1), 1 x 99, dtype: object
# CategoricalBlock: slice(4, 5, 1), 1 x 99, dtype: category
# CategoricalBlock: slice(5, 6, 1), 1 x 99, dtype: category
# ObjectBlock: slice(6, 7, 1), 1 x 99, dtype: object, '_item_cache': {'xf': 0     265.2829


# print(df.columns)
# print("==============================================")
