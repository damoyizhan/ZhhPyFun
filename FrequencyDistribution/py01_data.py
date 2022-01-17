# coding: utf-8
"""
 目标：生成测试用的sample data，本例中随机生成1000个IP 地址
"""

from pprint import pprint
from random import randint
import pandas as pd

iplist = []

for i in range(1, 1000):
    ip = str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(randint(0, 255))
    iplist.append(ip)

ipSeries = pd.Series(iplist)

print(ipSeries)



