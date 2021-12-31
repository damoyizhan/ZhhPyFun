import os
import sys
import pandas as pd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("ZhhPyFun") + len("ZhhPyFun")]
sys.path.append(rootPath)

from Pandas import 01_sample
# pandas的groupby函数一般会配合合计函数使用，比如，count、avg等等。
# 
# 首先讲解几种模式，然后示例上场：
# 
# 第一种：df.groupby(col)，返回一个按列进行分组的groupby对象；
# 
# 第二种：df.groupby([col1,col2])，返回一个按多列进行分组的groupby对象；
# 
# 第三种：df.groupby(col1)[col2]或者df[col2].groupby(col1)，两者含义相同，返回按列col1进行分组后，col2的值；

