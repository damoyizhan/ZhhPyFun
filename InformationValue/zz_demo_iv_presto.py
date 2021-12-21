#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import numpy as np
from common.pub_func import conn_presto
import ast
# 显示全部结果
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"


# In[52]:


# woe/iv计算
def woe_iv(table_name, var_name, target_name):
    """
    单变量woe/iv计算
    table_name:样本集（presto中的表名）
    var_name:待计算的自变量名称（已经过离散化处理的变量）
    target_name:target目标变量名 
    
    """
    # 组内统计
    sql = '''
    select ''' + var_name + ''',
       count(1)  as groupTotal,
       sum(target) as groupBad,
       count(1)-sum(target) as groupGood
   from ''' + table_name + '''
group by ''' + var_name + '''
order by ''' + var_name

    df_group_stats = conn_presto(sql)
    df_group_stats.columns = ['group', 'groupTotal', 'groupBad', 'groupGood']

    # 分组中坏或好样本数为0，强制转为数量1
    df_group_stats['groupBad'] = df_group_stats['groupBad'].apply(lambda x: 1 if x == 0 else x)
    df_group_stats['groupGood'] = df_group_stats['groupGood'].apply(lambda x: 1 if x == 0 else x)

    df_group_stats['groupRate'] = df_group_stats['groupGood'] / df_group_stats['groupBad']
    df_group_stats['groupBadRate'] = df_group_stats['groupBad'] / df_group_stats['groupTotal']
    df_group_stats['groupGoodRate'] = df_group_stats['groupGood'] / df_group_stats['groupTotal']
    # print(df_group_stats)
    # 整体统计
    df_group_stats['total_bad'] = df_group_stats['groupBad'].sum()
    df_group_stats['total_good'] = df_group_stats['groupGood'].sum()
    df_group_stats['totalCnt'] = df_group_stats['groupTotal'].sum()
    df_group_stats['totalRate'] = df_group_stats['total_good'] / df_group_stats['total_bad']
    df_group_stats['groupTotalRate'] = df_group_stats['groupTotal'] / df_group_stats['totalCnt']
    # 计算结果
    df_group_stats['woe'] = np.log(df_group_stats['groupRate'] / df_group_stats['totalRate'])
    df_group_stats['iv'] = (df_group_stats['groupGood'] / df_group_stats['total_good'] - df_group_stats['groupBad'] / df_group_stats['total_bad']) * df_group_stats['woe']
    iv = df_group_stats['iv'].sum()
    return iv, df_group_stats


iv, df_group_stats = woe_iv('tmp.anl_lmt_list_20211010_1', 'adjust_lmt_gender', 'target')
iv


# In[276]:


# 分组处理（分类变量）
def group_category(table_name, group_table_name, var_name, bins):
    """
    table_name:原始表名
    group_table_name:分组后记录写入的表名
    var_name:待分组的变量
    target_name:目标变量名
    bins:分组映射，格式：{取值:分组编号}
    """
    import ast
    sql = '''delete from tmp.etl_mid_iv_var_group'''
    # 清空目标表
    df_tmp = conn_presto(sql)
    # 分组case语句
    str_cond = ''
    str_case = ''
    # 转为字典
    bins = ast.literal_eval(bins)
    for k, v in bins.items():
        str_tmp = 'when cast(%s as varchar) =\'%s\' then \'%s\'' % (var_name, str(k), str(v))
        str_cond = str_cond + ' ' + str_tmp
        # print(str_cond)

    sql = '''
    insert into %s
    (
    id,var_name,target,group_id
     )
    select id,
       '%s' as var_name,
       target,
       case
       %s
            else '-9999'
       end as group_id     
from (select t.id,target,coalesce(cast(%s as varchar),'-9999') as %s from %s t)
    ''' % (group_table_name, var_name, str_cond, var_name, var_name, table_name)
    # print(sql)
    # 执行分组
    df_tmp = conn_presto(sql)
    return 1


group_category("tmp.anl_lmt_list_20211010_1"
               , "tmp.etl_mid_iv_var_group"
               , "adjust_lmt_gender"
               , "{'-9999': 0, '110101002': 1, '110101001': 2}"

               )
iv, df_group_stats = woe_iv('tmp.etl_mid_iv_var_group', 'group_id', 'target')
iv
df_group_stats


# In[301]:


# 分组处理（数值型变量）
def group_numerical(table_name, group_table_name, var_name, bins):
    """
    table_name:原始表名
    group_table_name:分组后记录写入的表名
    var_name:待分组的变量
    target_name:目标变量名
    bins:分组切分点,不包含最大最小值，格式：[1,5,10]
    """

    sql = '''delete from tmp.etl_mid_iv_var_group'''
    # 清空目标表
    df_tmp = conn_presto(sql)
    # 分组case语句
    str_cond = ''
    str_case = ''
    str_tmp = ''
    # 转为字典
    bins = pd.DataFrame(ast.literal_eval(bins), columns=['bin'])
    # 升序排序
    bins = bins.sort_values('bin')
    bins['lag'] = bins.sort_values('bin').shift(1)

    for k, v in bins.iterrows():
        if pd.isnull(v[1]):
            str_tmp = ' when %s<%s then \'%s\'' % (var_name, v[0], k)
        else:
            str_tmp = ' when %s>=%s and %s<%s then \'%s\'' % (var_name, v[1], var_name, v[0], k)
        str_cond = str_cond + ' ' + str_tmp
    # 最大值
    str_tmp = 'when %s>=%s then \'%s\'' % (var_name, bins['bin'].max(), k + 1)
    str_cond = str_cond + ' ' + str_tmp
    # print(str_cond)

    sql = '''
    insert into %s
    (
    id,var_name,target,group_id
     )
    select id,
       '%s' as var_name,
       target,
       case
       %s
            else '-9999'
       end as group_id     
from (select t.id,t.target ,coalesce(%s,-9999) as %s from %s t) --空值统一置为-9999
    ''' % (group_table_name, var_name, str_cond, var_name, var_name, table_name)
    # print(sql)
    # 执行分组
    df_tmp = conn_presto(sql)
    return 1


group_numerical('tmp.anl_lmt_list_20211010_1'
                , 'tmp.etl_mid_iv_var_group'
                , 'adjust_lmt_bill_date'
                , '[17, 26]'
                )
iv, df_group_stats = woe_iv('tmp.etl_mid_iv_var_group', 'group_id', 'target')
iv


# In[300]:


def var_iv(sample_table_name, var_name, var_type, bins):
    """
    计算单一变量的iv值
    sample_table_name:样本表表名
    var_name:变量名称
    var_type:变量类型，数字类型/枚举
    bins:分组条件，数字类型格式如：'[切分点1，切分点2，……]'
                   枚举类型格式如：'{取值1:分组id1,取值2:分组id2,……}'
    """
    iv = 0
    # 样本分组
    if var_type.strip() == '数字类型':
        group_numerical(sample_table_name
                        , 'tmp.etl_mid_iv_var_group'
                        , var_name
                        , bins
                        )

    elif var_type.strip() == '枚举':
        group_category(sample_table_name
                       , 'tmp.etl_mid_iv_var_group'
                       , var_name
                       , bins

                       )
    else:
        pass

    # iv计算
    iv, df_group_stats = woe_iv('tmp.etl_mid_iv_var_group', 'group_id', 'target')
    return iv, df_group_stats


# 代码执行前的预准备工作 ，数据放在 tmp.anl_lmt_list_20211010_1
#  tmp.anl_lmt_list_20211010_1 格式： uid  x，x，x...... y
#  adjust_lmt_bill_date:特征名，一个x值
#  "数值" ---枚举或数值类
#  "[17, 26]" 分箱切分点， < 17 一组，17~26 一组，>= 26 一组
#  todo 缺乏样本cut 逻辑

# 返回值：
# IV值 ， df_group_stats woe 的每个分组计算统计结果;
iv, df_group_stats = var_iv("tmp.anl_lmt_list_20211010_1", "adjust_lmt_bill_date", "数值", "[17, 26]")

# 配置信息
df_config = pd.read_excel('cols_config_result.xlsx')
df_config.head()

# In[303]:


# 计算所有变量的iv值
import time

# 开始时间
time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 样本表名
sample_table_name = 'tmp.anl_lmt_list_20211010_1'

# 每一个 iv值计算结果的清单
l = ['']

# 没有提供分组信息的变量不参与计算
df_config.replace(r'\[\]', np.nan, regex=True, inplace=True)

for k, v in df_config[pd.notnull(df_config['bins'])].iterrows():

    iv, df_group_stats = var_iv(sample_table_name, v[1], v[4], v[5])


    print(v[1] + ':' + str(iv))
    l.append(v[1] + ':' + str(iv))

df_iv = pd.DataFrame(l)[0].str.split(':', expand=True)
df_iv.columns = ['column', 'iv']
df_result = df_config.merge(df_iv, on='column', how='left')

# 结束时间
time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# In[306]:


df_result.to_excel('iv_adjust_lmt.xlsx')
df_result[pd.notnull(df_result['bins'])].head()

# In[ ]:


# In[ ]:
