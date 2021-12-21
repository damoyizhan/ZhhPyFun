import math


def Z_Score(data):
    lenth = len(data)
    total = sum(data)
    ave = float(total) / lenth
    tempsum = sum([pow(data[i] - ave, 2) for i in range(lenth)])
    tempsum = pow(float(tempsum) / lenth, 0.5)
    for i in range(lenth):
        data[i] = (data[i] - ave) / tempsum
    return data



print('Z均值：'+Z_Score([1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1, 999999999999999999999999999999999999999999999999999999999999999999, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1,1,1,1,1, 999999999999999999999999999999999999999999999999999999999999999999]).__str__())
print('Z均值：'+Z_Score([1,1,1,1,1,1,1,1,1,1,1, -999999999999999999999999999999999999999999999999999999999999999999]).__str__())