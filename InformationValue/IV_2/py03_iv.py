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

import numpy as np
import pandas as pd
import math

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("iv_analysis") + len("iv_analysis")]
sys.path.append(rootPath)

from py02_cut import df
from log.logger import Logger

log_file = os.path.join(os.sep, rootPath, "run.log")
logger = Logger().getLogger(__file__, log_file, "INFO")


def IV_column(df_column, Y_total, N_total, __column):
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

    logger.info("\n %s" % df_column)

    # 计算Y[i]  和N[i]
    YN_i = df_column.groupby([__column, 'y'], as_index=False)['cnt'].count()
    logger.info("\n %s" % YN_i)
    logger.info("--------------------------------------------------------------------------------")

    # 计算Py[i] 和Pn[i]
    YN_i['pct'] = YN_i['cnt'] * YN_i['y'] / Y_total + YN_i['cnt'] * (1 - YN_i['y']) / N_total

    logger.info("\n %s" % YN_i)
    logger.info("--------------------------------------------------------------------------------")
    # 计算 woe[i]   = ln(Py[i]/Pn[i])

    PY_i = YN_i[YN_i['y'] == 1]
    PN_i = YN_i[YN_i['y'] == 0]
    PY_i.set_index(['cut_group_xf'], inplace=True)
    PN_i.set_index(['cut_group_xf'], inplace=True)

    WOE_i = PY_i.div(PN_i, axis=0)
    WOE_i['woe'] = np.log(WOE_i['pct'])

    # logger.info("\n %s" % YN_i[YN_i['y'] == 1])
    # logger.info("\n %s" % YN_i[YN_i['y'] == 0])

    # logger.info("\n %s" % PY_i.div(PN_i, axis=0))
    # logger.info("\n %s" % WOE_i)

    # 计算 iv[i] = (Py[i] - Pn[i]) * woe[i]

    IV_i = (PY_i - PN_i) * WOE_i
    logger.info("\n %s" % PY_i)
    logger.info("\n %s" % PN_i)
    logger.info("\n %s" % IV_i)
    exit(1)
    #
    # logger.info(YN_i.keys())
    #
    # logger.info(YN_i.columns)
    # logger.info(Pyn_i)

    #  ##/ Y_total

    # logger.info(Pyn_i)

    # raise Exception("主动抛出错误")
    # Y_N_i = df_column.groupby([__column, 'y']).groups
    # logger.info(Y_N_i)
    # Y_N_i = df_column.groupby([__column, 'y']).count()
    # logger.info(Y_N_i)
    # logger.info(Y_N_i.__module__)
    # logger.info(Y_N_i.__dict__)

    #    df[(df[‘column_name’] == target_value)]

    logger.info(Y_N_i)

    Py_i = Y_N_i[Y_N_i['y'] == 1] / Y_total
    logger.info(Py_i)
    # Py_i = Y_N_i[] / Y_total
    # logger.info(Py_i)

    IV = IV_list.sum()

    IV = 0
    for groupkey in df.groupby(__column).groups.keys():
        IV += IV_group(Y_total, N_total, __column, groupkey)

    print("==列：" + __column + " IV值" + str(IV))


# ##############################################################################################################

logger.debug("==start                   ==============================================================")
pd.set_option('display.max_columns', 1000000)
pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_colwidth', 1000000)
pd.set_option('display.width', 1000000)
logger.debug(df)
logger.info("==计算 Y[total] 和 N[total] ==============================================================")
count_total = df.groupby('y')['y'].count()
Y_total = count_total[1]
N_total = count_total[0]

logger.debug("count_total  :" + str(count_total))
logger.info("Y_total :" + str(Y_total))
logger.info("N_total :" + str(N_total))

logger.info("==循环计算每一列的IV ==============================================================")

for column in df.columns:

    # 原始数据列不参与计算
    if not column.startswith("cut_group"):
        continue

    # 计算一个列的woe值
    logger.info("==计算 " + column + " 的IV 值 ==============================================================")

    df_column = df[[column, 'y']]
    # 增加一列 cnt 列 用于计算
    df_column['cnt'] = 0

    logger.debug(df_column)
    IV_column(df_column, Y_total, N_total, column)

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
