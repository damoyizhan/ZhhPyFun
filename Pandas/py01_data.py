import pandas as pd
import numpy as np

# 样例
df = pd.DataFrame(np.array(([1,  2,  3],
                            [4,  5,  6],
                            [1, 22, 33])),
                  index=['mouse', 'rabbit', 'cat'],
                  columns=['one', 'two', 'three'])
print(df)
