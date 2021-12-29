#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# In[34]:


# data
# data
from sklearn import datasets

iris = datasets.load_iris()
df = pd.DataFrame(iris['data'])
df.columns = iris['feature_names']
df['target'] = iris['target']
df['x_test'] = df['target'].copy()
df[df['target'] == 2]['target'] = 0
df['y_test'] = np.random.randint(0, 2, size=(df['target'].count(), 1))
# df.head()


# In[35]:


# 构造分类变量
df['x_test_2'] = df['x_test'].copy()
df.loc[0:30, 'x_test_2'] = 3
df.loc[100:120, 'x_test_2'] = 4
df.loc[70:80, 'x_test_2'] = 5


# df.groupby('x_test_2').count()


# In[17]:


# woe/iv计算
def woe_iv(tar, var):
    """
    分组后的变量,woe,iv变换
    tar:target目标变量
    var:进行woe,iv转换的自变量（已经过离散化处理的变量）

    """

    total_bad = tar.sum()
    total_good = tar.count() - total_bad
    totalRate = total_good / total_bad
    totalCnt = tar.count()

    msheet = pd.DataFrame({tar.name: tar, var.name: var})
    grouped = msheet.groupby([var.name])

    groupBad = grouped.sum()[tar.name]
    groupTotal = grouped.count()[tar.name]
    groupGood = groupTotal - groupBad
    # 分组样本数占总比
    groupTotalRate = groupTotal / totalCnt
    # 分组中坏或好样本数为0，强制转成数为1
    groupBad = groupBad.replace(0, 1)
    groupGood = groupGood.replace(0, 1)
    groupRate = groupGood / groupBad
    groupBadRate = groupBad / groupTotal
    groupGoodRate = groupGood / groupTotal
    woe = np.log(groupRate / totalRate)
    iv = np.sum((groupGood / total_good - groupBad / total_bad) * woe)
    gpsheet = pd.DataFrame(list(zip(woe.index, groupTotal, groupTotalRate, groupGood, groupBad, groupRate, groupBadRate, woe)),
                           columns=['group', 'groupTotal', 'groupTotalRate', 'groupGood', 'groupBad', 'groupRate', 'groupBadRate', 'woe'])
    gpsheet['iv_sum'] = iv
    gpsheet['group'] = gpsheet['group'].astype('str')
    gpsheet['id'] = gpsheet.index
    return woe, iv, gpsheet  # ,woe.tolist()


# woe,iv,gpsheet=woe_iv(df['y_test'], df['group_x_test'])
# woe
# gpsheet


# In[ ]:


# In[31]:


# woe/iv 展示
def plot_woe(data):
    """
    data:函数woe_iv返回的集合gpsheet
    """
    # iv值
    print('iv值:' + str(data.loc[0]['iv_sum']))

    # 分组排序
    data = data.sort_values('group')

    data['group_1'] = data['group'].astype('str')

    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    # 分组样本数
    g1 = sns.barplot(x='group', y='groupTotal', data=data, ax=axes[0])
    group_cnt = data.groupby('id')['groupTotal'].sum().reset_index()
    for index, row in group_cnt.iterrows():
        g1.text(row.name, row.id, row.groupTotal, color='black', ha='center')

    # woe
    g2 = sns.lineplot(x='group', y='woe', data=data, ax=axes[1], markers=True, dashes=True)

    # BadRate
    g3 = sns.barplot(x='group', y='groupBadRate', data=data, ax=axes[2])

    plt.show()


# plot_woe(gpsheet)


# In[ ]:


# In[20]:


def concatGroup_category(var_stats_data, min_rate, var_type):
    """
    var_stats_data:调用woe函数返回的统计数据集
    min_rate:每个分组样本占总比例最小值（小于该值，则与相邻的woe的分组合并）
    var_type:原变量数据类型
    """
    df_gp = var_stats_data.sort_values(['groupTotal', 'woe'])[['group', 'groupTotal', 'groupTotalRate', 'woe']]
    df_gp['group_label'] = df_gp['group']
    # 合并样本量过少的分组
    while (df_gp.head(1)['groupTotalRate'].iloc[0] < min_rate):
        # 最小两个分组合并
        df_tmp = df_gp.iloc[0:2]
        df_tmp['group_label'] = ','.join(df_tmp.iloc[0:2]['group_label'].tolist())
        df_tmp['group'] = df_tmp['group'].max()
        # 其他记录
        df_tmp1 = df_gp.iloc[2:]
        # 重置分组
        df_gp = pd.concat([df_tmp.groupby(['group', 'group_label'], as_index=False).agg({'groupTotal': sum, 'groupTotalRate': sum, 'woe': max}), df_tmp1])
        df_gp = df_gp.sort_values(['groupTotal', 'woe'])
    df_gp = df_gp.reset_index(drop=True)
    df_gp['group'] = df_gp.index
    # 生成分组字典
    ser_bins = df_gp['group_label'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    dict_bins = ser_bins.to_frame().reset_index()
    dict_bins.columns = ['group', 'value']
    # 还原变量类型
    dict_bins['value'] = dict_bins['value'].astype(var_type)
    bins = dict_bins.set_index('value')['group'].to_dict()
    return bins, df_gp


# In[29]:


# 自定义分组（分类变量）
def group_category(data, var_name, target_name, bins=None, flag=1):
    """
    分类型变量离散化分组处理，在原数据集中增加分组结果group_变量名
    data：数据集
    var:待分组变量名称
    bins:分组定义{取值:分组编号}
    target:目标变量名称
    flag:是否需要调试
    """
    # 空值统一置为-9999
    data[var_name] = data[var_name].apply(lambda x: -9999 if pd.isnull(x) else x)

    # 不提供分组，则自动合并分组（确保每个分组数量不少于5%）
    if bins is None:
        # 以原始类别分组计算woe
        woe, iv, gpsheet = woe_iv(data[target_name], data[var_name])
        bins, df_gp = concatGroup_category(gpsheet, 0.05, data.dtypes[var_name])
    else:
        pass

    # 生成分组结果
    data['group_' + var_name] = data[var_name].map(bins)

    if flag == 1:
        # 计算woe
        woe, iv, gpsheet = woe_iv(data[target_name], data['group_' + var_name])
        # 展示分组效果
        plot_woe(gpsheet)

    else:
        # 完成
        pass

    # 返回分组信息
    if bins is None:
        cut = data.groupby(var_name).count().index.tolist()

    else:
        cut = bins
    return cut, gpsheet


cut, gpsheet = group_category(df, 'x_test_2', 'y_test'
                              , {5: 0, 0: 0, 4: 0, 2: 3, 3: 4, 1: 5}
                              , flag=1

                              )


# cut


# In[ ]:


# In[36]:


# 自定义分组（连续变量）
def group_numerical(data, var_name, target_name, bins=None, n=5, flag=1):
    """
    分类型变量离散化分组处理，在原数据集中增加分组结果group_变量名
    data：数据集
    var:待分组变量名称
    target:目标变量名称
    cut:切分点，如：[1,5,10……]
    n:自动划分分组数量，默认为5
    flag:是否需要调试
    """
    # 不提供切分点，按比例划分
    if bins is None:
        data['group_' + var_name] = pd.qcut(df[var_name], n, duplicates='drop').astype('str')

    else:
        data['group_' + var_name] = pd.cut(data[var_name], bins, right=True).astype('str')

    if flag == 1:
        # 计算woe
        woe, iv, gpsheet = woe_iv(data[target_name], data['group_' + var_name])
        # print(gpsheet)
        # 展示分组效果
        plot_woe(gpsheet)
    else:
        # 完成
        pass

    # 返回切分点
    if bins is None:
        cut = data.groupby('group_' + var_name)[var_name].min().sort_values().tolist()
        del (cut[0])
    else:
        cut = bins

    return cut


cut = group_numerical(df, 'petal length (cm)', 'y_test'
                      # ,bins=[0,1.5,4.3,5,9999]
                      , n=5
                      , flag=1
                      )
# cut


# In[37]:


# 需要参与计算的确定变量类型，连续变量（nvar）还是离散变量（cvar）
# 未自定义分组，采用默认分组
cvar = ['x_test']
nvar = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)']


def iv_vs(data, target):
    """
    计算数据集中所有变量的iv值
    data：数据集
    target:目标变量名称
    """
    for var in data.columns:
        # print(var)
        # 补全分组字段
        if var in cvar and 'group_' + var not in data.columns:
            cut = group_category(data, var, target, flag=0)
        elif var in nvar and 'group_' + var not in data.columns:
            cut = group_numerical(data, var, target, flag=0)

    # 计算所有变量的iv值
    df_result = pd.DataFrame(columns=['var', 'iv'])
    df_tmp = pd.DataFrame(columns=['var', 'iv'])
    for var in data.columns:
        if var.startswith('group_'):
            try:
                woe, iv, gpsheet = woe_iv(data[target], data[var])
                print(var + ':' + str(iv))
                df_tmp = pd.DataFrame({'var': var, 'iv': iv}, index=["0"])
                df_result = df_result.append(df_tmp, ignore_index=True)
            except:
                print(var)

    return df_result


r = iv_vs(df, 'y_test')
print(r.sort_values('iv', ascending=False))

# In[ ]:




