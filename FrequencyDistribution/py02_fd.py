import os
import sys
import numpy as np

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("iv_analysis") + len("iv_analysis")]
sys.path.append(rootPath)

from py01_data import ipSeries

hist1 = np.histogram(ipSeries, bins=10)  # 用numpy包计算直方图

print(hist1)
