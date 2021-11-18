import math

from variance import get_variance


# 标准差

def get_standard_deviation(records):
    variance = get_variance(records)
    return math.sqrt(variance)


print('标准差：' + get_standard_deviation([1, 2, 2, 3, 4, 5, 6, 7, 800000000000000]).__str__())
