# 方差
from average import get_average


def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)


print('方 差：' + get_variance([1, 2, 2, 3, 4, 5, 6, 7, 800000000000000]).__str__())
