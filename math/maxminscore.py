# 最大值\最小值
def get_maxmin(records):
    min_value = None
    max_value = None
    for i in records:
        if min_value is None or min_value > i:
            min_value = i
        if max_value is None or max_value < i:
            max_value = i
    return max_value, min_value


# 最大最小规范化
def maxmin_score(records):
    max_value, min_value = get_maxmin(records)
    scores = [(i - min_value) / (max_value - min_value) for i in records]
    return scores


print(maxmin_score([2, 2, 3, 4, 5, 6, 7, 8]))
print(maxmin_score([10, 20, 30, 40, 50, 60, 70, 80]))
print(maxmin_score([20, 20, 30, 40, 50, 60, 70, 80]))