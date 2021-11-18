# 均值

def get_average(records):
    return sum(records) / len(records)


print('平均值：' + get_average([1, 2, 2, 3, 4, 5, 6, 7, 800000000000000]).__str__())
