import os
import sys

import pandas as pd
import numpy as np

# 样例
df = pd.DataFrame(np.array(([1,  2,  3],
                            [4,  5,  6],
                            [1, 22, 33])),
                  index=['mouse', 'rabbit', 'cat'],
                  columns=['one', 'two', 'three'])

print(df)
# 第一种：df.groupby(col)，返回一个按列进行分组的groupby对象；
print("==第一种：df.groupby(col)，返回一个按列进行分组的groupby对象；")
print(df.groupby('one').count())

# 第二种：df.groupby([col1,col2])，返回一个按多列进行分组的groupby对象
print("==第二种：df.groupby([col1,col2])，返回一个按多列进行分组的groupby对象")
print(df.groupby(['one', 'two']).count())

print("==第二种：特殊情况，group by 字段是df 所有字段时，无法count ，写法需要变形")

#   下面这个例子会发现group by 后的DataFrame 是空的
print(df.groupby(['one', 'two','three']).count())

#  下面这个例子是预期的结果
print(df.groupby(['one', 'two','three'])['one'].count())

print("==第三种：df.groupby(col1)[col2]或者df[col2].groupby(col1)，两者含义相同，返回按列col1进行分组后，col2的值；")
print(df.groupby('one')['two'].count())
print(df.groupby('two')['one'].count())

