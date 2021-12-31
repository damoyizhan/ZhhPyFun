import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("iv_analysis") + len("iv_analysis")]
sys.path.append(rootPath)

import 01_sample

pandas的groupby函数一般会配合合计函数使用，比如，count、avg等等。

首先讲解几种模式，然后示例上场：

第一种：df.groupby(col)，返回一个按列进行分组的groupby对象；

第二种：df.groupby([col1,col2])，返回一个按多列进行分组的groupby对象；

第三种：df.groupby(col1)[col2]或者df[col2].groupby(col1)，两者含义相同，返回按列col1进行分组后，col2的值；

作者：默直
链接：https://www.jianshu.com/p/e46eb6e447e3
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。