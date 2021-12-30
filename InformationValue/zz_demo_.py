import pandas as pd
import numpy as np


# 使用已经分箱的结果，计算woe和vi
def cal_woe(input_df):
    groups = input_df.shape[0]
    # 对于统计项为0的actual_0和actual_1赋值为1
    input_df.loc[input_df['actual_0'] == 0, 'actual_0'] = 1
    input_df.loc[input_df['actual_1'] == 0, 'actual_1'] = 1
    all_0 = input_df['actual_0'].sum()
    all_1 = input_df['actual_1'].sum()
    woe = []
    vi = 0
    for i in range(groups):
        tmp = ((input_df.loc[i, 'actual_1'] * 1.0 / all_1) - (input_df.loc[i, 'actual_0'] * 1.0 / all_0)) * \
              np.log((input_df.loc[i, 'actual_1'] * 1.0 / all_1) / (input_df.loc[i, 'actual_0'] * 1.0 / all_0))
        woe.append(tmp)
        vi += tmp
    input_df['woe'] = woe

    return input_df, vi
