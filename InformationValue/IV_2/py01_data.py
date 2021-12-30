# coding: utf-8
"""
 目标：生成测试用的sample data
 hello world 格式：
 row = {'y': '0', 'xv': 'a', 'xi': '32','xf':'10.89'}
 xv = 格式为varchar 的x值
 xi = 格式为int     的x值
 xf = 格式为float   的x值
"""
from pprint import pprint
from random import randint
import pandas as pd


def Num2Char(number):
    """
    把数字转换成相应的字符,1-->'A' 27-->'AA'
    """
    numbers = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h'
    }

    return numbers[number]


data_list = []

for i in range(1, 100):
    y = randint(0, 1)
    xv_pre = randint(0, 7)
    xv = Num2Char(xv_pre)
    xi = randint(0, 100)
    xf = randint(1000000, 9000000) / 10000

    row = {'y': y, 'xv': xv, 'xi': xi, 'xf': xf}

    data_list.append(row)

# pprint(data_list)

data_list = [{'xf': 265.2829, 'xi': 60, 'xv': 'h', 'y': 1},
             {'xf': 746.6886, 'xi': 27, 'xv': 'd', 'y': 0},
             {'xf': 570.2055, 'xi': 57, 'xv': 'f', 'y': 1},
             {'xf': 569.4865, 'xi': 53, 'xv': 'g', 'y': 1},
             {'xf': 296.9362, 'xi': 95, 'xv': 'f', 'y': 1},
             {'xf': 447.6251, 'xi': 25, 'xv': 'f', 'y': 0},
             {'xf': 427.1694, 'xi': 71, 'xv': 'e', 'y': 1},
             {'xf': 782.461, 'xi': 44, 'xv': 'g', 'y': 0},
             {'xf': 718.7098, 'xi': 85, 'xv': 'e', 'y': 1},
             {'xf': 838.2993, 'xi': 44, 'xv': 'a', 'y': 0},
             {'xf': 438.7048, 'xi': 72, 'xv': 'b', 'y': 0},
             {'xf': 513.585, 'xi': 51, 'xv': 'a', 'y': 1},
             {'xf': 898.4296, 'xi': 3, 'xv': 'g', 'y': 0},
             {'xf': 645.2199, 'xi': 56, 'xv': 'f', 'y': 0},
             {'xf': 494.8897, 'xi': 31, 'xv': 'e', 'y': 1},
             {'xf': 272.2454, 'xi': 17, 'xv': 'd', 'y': 1},
             {'xf': 196.2053, 'xi': 35, 'xv': 'g', 'y': 1},
             {'xf': 419.8198, 'xi': 45, 'xv': 'b', 'y': 1},
             {'xf': 577.8692, 'xi': 7, 'xv': 'b', 'y': 1},
             {'xf': 697.466, 'xi': 13, 'xv': 'e', 'y': 0},
             {'xf': 274.9494, 'xi': 93, 'xv': 'a', 'y': 0},
             {'xf': 759.6351, 'xi': 23, 'xv': 'c', 'y': 1},
             {'xf': 875.0141, 'xi': 49, 'xv': 'e', 'y': 0},
             {'xf': 731.0994, 'xi': 90, 'xv': 'e', 'y': 0},
             {'xf': 881.9657, 'xi': 83, 'xv': 'd', 'y': 0},
             {'xf': 583.9123, 'xi': 80, 'xv': 'c', 'y': 0},
             {'xf': 837.8005, 'xi': 50, 'xv': 'g', 'y': 0},
             {'xf': 155.9217, 'xi': 18, 'xv': 'f', 'y': 0},
             {'xf': 668.8822, 'xi': 83, 'xv': 'f', 'y': 1},
             {'xf': 601.0198, 'xi': 67, 'xv': 'f', 'y': 1},
             {'xf': 754.9427, 'xi': 27, 'xv': 'e', 'y': 1},
             {'xf': 846.9763, 'xi': 22, 'xv': 'c', 'y': 1},
             {'xf': 845.4367, 'xi': 50, 'xv': 'c', 'y': 1},
             {'xf': 323.6858, 'xi': 13, 'xv': 'h', 'y': 1},
             {'xf': 607.3708, 'xi': 8, 'xv': 'e', 'y': 1},
             {'xf': 579.3382, 'xi': 30, 'xv': 'g', 'y': 0},
             {'xf': 199.5296, 'xi': 20, 'xv': 'e', 'y': 1},
             {'xf': 733.055, 'xi': 60, 'xv': 'g', 'y': 0},
             {'xf': 241.4455, 'xi': 20, 'xv': 'f', 'y': 1},
             {'xf': 689.8463, 'xi': 22, 'xv': 'e', 'y': 1},
             {'xf': 365.9267, 'xi': 49, 'xv': 'g', 'y': 0},
             {'xf': 132.7664, 'xi': 41, 'xv': 'e', 'y': 1},
             {'xf': 237.873, 'xi': 49, 'xv': 'a', 'y': 1},
             {'xf': 133.8152, 'xi': 40, 'xv': 'c', 'y': 1},
             {'xf': 758.2697, 'xi': 91, 'xv': 'c', 'y': 1},
             {'xf': 233.5459, 'xi': 47, 'xv': 'a', 'y': 1},
             {'xf': 122.2476, 'xi': 0, 'xv': 'd', 'y': 1},
             {'xf': 436.8142, 'xi': 20, 'xv': 'd', 'y': 1},
             {'xf': 636.5765, 'xi': 87, 'xv': 'a', 'y': 0},
             {'xf': 200.4963, 'xi': 37, 'xv': 'd', 'y': 0},
             {'xf': 700.792, 'xi': 23, 'xv': 'e', 'y': 1},
             {'xf': 837.3379, 'xi': 29, 'xv': 'c', 'y': 1},
             {'xf': 674.9005, 'xi': 20, 'xv': 'a', 'y': 1},
             {'xf': 434.856, 'xi': 25, 'xv': 'a', 'y': 0},
             {'xf': 537.4608, 'xi': 57, 'xv': 'h', 'y': 1},
             {'xf': 416.4948, 'xi': 48, 'xv': 'd', 'y': 1},
             {'xf': 831.855, 'xi': 15, 'xv': 'g', 'y': 1},
             {'xf': 722.3499, 'xi': 81, 'xv': 'b', 'y': 0},
             {'xf': 623.8292, 'xi': 47, 'xv': 'f', 'y': 0},
             {'xf': 741.6126, 'xi': 67, 'xv': 'b', 'y': 0},
             {'xf': 720.4991, 'xi': 93, 'xv': 'd', 'y': 1},
             {'xf': 695.564, 'xi': 76, 'xv': 'c', 'y': 1},
             {'xf': 792.0112, 'xi': 44, 'xv': 'b', 'y': 0},
             {'xf': 109.4065, 'xi': 54, 'xv': 'g', 'y': 0},
             {'xf': 356.5922, 'xi': 97, 'xv': 'f', 'y': 1},
             {'xf': 488.0274, 'xi': 86, 'xv': 'e', 'y': 1},
             {'xf': 844.1596, 'xi': 31, 'xv': 'e', 'y': 0},
             {'xf': 154.3468, 'xi': 43, 'xv': 'b', 'y': 1},
             {'xf': 815.9717, 'xi': 0, 'xv': 'a', 'y': 1},
             {'xf': 249.4674, 'xi': 69, 'xv': 'h', 'y': 1},
             {'xf': 357.1742, 'xi': 90, 'xv': 'h', 'y': 0},
             {'xf': 415.0546, 'xi': 21, 'xv': 'f', 'y': 1},
             {'xf': 848.5257, 'xi': 85, 'xv': 'e', 'y': 0},
             {'xf': 738.6664, 'xi': 93, 'xv': 'h', 'y': 1},
             {'xf': 522.4688, 'xi': 78, 'xv': 'b', 'y': 0},
             {'xf': 813.3649, 'xi': 76, 'xv': 'f', 'y': 0},
             {'xf': 745.8486, 'xi': 12, 'xv': 'a', 'y': 0},
             {'xf': 118.9123, 'xi': 57, 'xv': 'b', 'y': 0},
             {'xf': 414.9976, 'xi': 22, 'xv': 'b', 'y': 0},
             {'xf': 251.2055, 'xi': 63, 'xv': 'a', 'y': 1},
             {'xf': 448.0614, 'xi': 3, 'xv': 'g', 'y': 1},
             {'xf': 853.6853, 'xi': 39, 'xv': 'b', 'y': 0},
             {'xf': 812.6781, 'xi': 37, 'xv': 'a', 'y': 1},
             {'xf': 544.8363, 'xi': 88, 'xv': 'e', 'y': 1},
             {'xf': 784.2802, 'xi': 50, 'xv': 'b', 'y': 1},
             {'xf': 692.0399, 'xi': 43, 'xv': 'b', 'y': 1},
             {'xf': 730.1466, 'xi': 52, 'xv': 'f', 'y': 1},
             {'xf': 760.9144, 'xi': 25, 'xv': 'a', 'y': 0},
             {'xf': 646.9331, 'xi': 15, 'xv': 'f', 'y': 1},
             {'xf': 194.8551, 'xi': 55, 'xv': 'c', 'y': 0},
             {'xf': 861.2496, 'xi': 90, 'xv': 'c', 'y': 0},
             {'xf': 474.9135, 'xi': 33, 'xv': 'e', 'y': 0},
             {'xf': 842.4038, 'xi': 4, 'xv': 'c', 'y': 0},
             {'xf': 391.6881, 'xi': 55, 'xv': 'f', 'y': 0},
             {'xf': 393.5516, 'xi': 50, 'xv': 'a', 'y': 0},
             {'xf': 528.9012, 'xi': 70, 'xv': 'b', 'y': 0},
             {'xf': 313.4359, 'xi': 28, 'xv': 'c', 'y': 0},
             {'xf': 646.4035, 'xi': 55, 'xv': 'a', 'y': 1},
             {'xf': 706.2255, 'xi': 6, 'xv': 'a', 'y': 0}]

# data_list 转换为 DataFrame

df = pd.DataFrame(data_list)

# print(df)