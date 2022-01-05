import pandas as pd
import numpy as np

# 样例
df = pd.DataFrame(np.array(([1, 2, 3],
                            [4, 5, 6],
                            [1, 22, 33])),
                  index=['mouse', 'rabbit', 'cat'],
                  columns=['one', 'two', 'three'])
print(df)
print("--df[df['one']== 1]--------------------------------------")
print(df[df['one'] == 1])

df_grouped = df.groupby(['one', 'two', 'three'])['one', 'two', 'three'].count()
print("--df_grouped--------------------------------------")
print(df_grouped)

# 这时候得不到想要的结果，发现过滤结果为空
print("--df_grouped[df_grouped['one']== 4]--------------------------------------")
print(df_grouped[df_grouped['one'] == 4])

# df.reset_index()

print("--df.reset_index()--------------------------------------")
print(df_grouped.reset_index)

print("--as_index=False--------------------------------------")
df_grouped_asindexfales = df.groupby(['one'], as_index=False)['one'].count()
print(df_grouped_asindexfales)
# todo 处理方式：1.使用 df.loc['column value ']
# print("--df.loc--------------------------------------")
# df_grouped.loc(1)
# print(df_grouped.loc('1'))

#
#
#
# df.groupby(['one', 'two'],as_index=False)['three'].count()
