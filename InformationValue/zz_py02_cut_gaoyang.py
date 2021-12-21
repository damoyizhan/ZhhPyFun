#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# calc_float_value_bins               输入pandas.Series对象，输出bins                    即分箱
# calc_float_bins_info_by_base_bins   输入pandas.Series对象+bins， 输出各个bins的统计信息  即分箱统计

import pandas as pd

import numpy as np
import json
from utils import filter_na, is_series_data_type_numeric


def calc_float_value_bins(filter_na_value_data, feature_name=None):
    # 分箱数
    discrete_threashold = 8
    # 分箱结果
    feature_value_bins_list = []
    # x值的取值清单
    total_value_cnt = int(filter_na_value_data.value_counts().count())

    # 只有一个取值的时候，分箱;
    if total_value_cnt == 1:
        feature_value_bins_list.append('(, %s]' % filter_na_value_data.values[0])
        feature_value_bins_list.append('(%s, ]' % filter_na_value_data.values[0])

    # 取值个数小于等于8的特征分箱
    elif total_value_cnt < discrete_threashold or (feature_name is not None and feature_name.endswith('level')):
        # 取值个数小于阈值，或特征名为xxx_level，则当成离散型，每个取值是一个分箱
        value_list = list(filter_na_value_data.value_counts().index)
        value_list.sort()

        for idx, value in enumerate(value_list):
            if idx == 0:
                feature_value_bins_list.append('(, %s]' % value)
            elif idx == len(value_list) - 1:
                feature_value_bins_list.append('(%s, ]' % value_list[idx - 1])
            else:
                feature_value_bins_list.append('(%s, %s]' % (value_list[idx - 1], value))
    # 取值个数 大于8 的特殊模型结果分箱；
    elif feature_name == 'model_result':
        value_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        for idx, value in enumerate(value_list):
            if idx == 0:
                feature_value_bins_list.append('[0, %s]' % value)
            elif idx == len(value_list) - 1:
                feature_value_bins_list.append('(%s, ]' % value_list[idx - 1])
            else:
                feature_value_bins_list.append('(%s, %s]' % (value_list[idx - 1], value))

    # 取值个数大于8 的普通特征分箱；
    else:
        # 按取值占比从大到小，遍历各个取值，超过10%则新建一个分箱
        value_cnt_ratio_series = filter_na_value_data.value_counts(normalize=True).sort_index()
        new_bins_threshold = 0.1

        tmp_total_ratio = 0
        last_bins_right_boundary = ''
        for _k, _ratio in value_cnt_ratio_series.iteritems():
            tmp_total_ratio += _ratio
            if tmp_total_ratio >= new_bins_threshold:
                feature_value_bins_list.append('(%s, %s]' % (last_bins_right_boundary, _k))
                last_bins_right_boundary = _k
                tmp_total_ratio = 0

        feature_value_bins_list.append('(%s, ]' % last_bins_right_boundary)

    return feature_value_bins_list


def calc_float_bins_info_by_base_bins(data_series_filter_na, base_bins_info):
    """
    根据已有分箱信息进行分箱
    """
    try:
        if isinstance(base_bins_info, str):
            base_bins_info = json.loads(base_bins_info)

        total_cnt = data_series_filter_na.count()

        result = []
        for value_bins_raw in base_bins_info:

            value_bins = value_bins_raw.replace(' ', '')

            left_oper = None
            right_oper = None
            if value_bins[0] == '[':
                left_oper = 'ge'
            elif value_bins[0] == '(':
                left_oper = 'gt'

            if value_bins[-1] == ']':
                right_oper = 'le'
            elif value_bins[-1] == ')':
                right_oper = 'lt'

            min_value_str, max_value_str = value_bins.replace('[', '') \
                .replace(']', '') \
                .replace('(', '') \
                .replace(')', '') \
                .split(',')

            min_value = None
            max_value = None
            if min_value_str:
                min_value = round(float(min_value_str), 8)
            if max_value_str:
                max_value = round(float(max_value_str), 8)

            left_data = None
            right_data = None
            if min_value is not None:
                if left_oper == 'ge':
                    left_data = data_series_filter_na >= min_value
                elif left_oper == 'gt':
                    left_data = data_series_filter_na > min_value

            if max_value is not None:
                if right_oper == 'le':
                    right_data = data_series_filter_na <= max_value
                elif right_oper == 'lt':
                    right_data = data_series_filter_na < max_value

            if (left_data is not None) and (right_data is not None):
                group_sample_cnt = int(data_series_filter_na[left_data & right_data].count())
            elif left_data is not None:
                group_sample_cnt = int(data_series_filter_na[left_data].count())
            elif right_data is not None:
                group_sample_cnt = int(data_series_filter_na[right_data].count())
            else:
                logging.error('left_data and right_data is all None')
                continue

            result.append((value_bins_raw, round(float(group_sample_cnt / total_cnt), 8), group_sample_cnt))

        return result
    except Exception as e:
        print(base_bins_info)
        print(data_series_filter_na)
        raise e


def calc_psi(base_bins_info, current_base_info):
    _base = np.array([0.00000001 if x[1] == 0 else x[1] for x in base_bins_info])
    _cur = np.array([0.00000001 if x[1] == 0 else x[1] for x in current_base_info])

    ret = ((_cur - _base) * np.log(_cur / _base)).sum()
    return round(float(ret), 8)


def gen_custom_bins(cut_list):
    bins_list = []
    for idx, cut_value in enumerate(cut_list):
        if idx == 0:
            bins_list.append('(%s,%s]' % ('', cut_value))
        elif idx == len(cut_list) - 1:
            bins_list.append('(%s,%s]' % (cut_list[idx - 1], cut_value))
            bins_list.append('(%s,%s]' % (cut_value, ''))
        else:
            bins_list.append('(%s,%s]' % (cut_list[idx - 1], cut_value))

    return bins_list


def convert_bins(bins):
    """
    格式1： 1,2,3+
    格式2： default
    格式3： custom,function_name
    """
    bins = bins.replace(' ', '')
    if bins == 'default':
        return bins

    parts = bins.split(',')
    if parts[0] == 'custom':
        return bins

    if '+' in parts[-1]:
        parts[-1] = parts[-1][0:-1]

        if int(parts[0]) == 0:
            parts = parts[1:]

        new_bins = []

        bins_str = '(,0]'
        new_bins.append(bins_str)

        for idx, _p in enumerate(parts):
            if idx == 0:
                bins_str = '(0,%s)' % _p
                new_bins.append(bins_str)
            elif idx == len(parts) - 1:
                bins_str = '[%s,%s)' % (parts[idx - 1], _p)
                new_bins.append(bins_str)

                bins_str = '[%s,)' % (parts[idx])
                new_bins.append(bins_str)
            else:
                bins_str = '[%s,%s)' % (parts[idx - 1], _p)
                new_bins.append(bins_str)

        return new_bins

    return None


def calc_psi_two_series_new(old_series, new_series, feature_name, bins_info):
    """
    格式1： 1,2,3+
    格式2： default
    格式3： custom,function_name
    """
    custom_bins = convert_bins(bins_info)

    ret = None
    if isinstance(custom_bins, list):
        ret = calc_psi_two_series(old_series, new_series, feature_name, custom_bins_list=custom_bins)
    elif custom_bins == 'default':
        ret = calc_psi_two_series(old_series, new_series, feature_name)
    else:
        _parts = custom_bins.split(',')
        if _parts[0] == 'custom':
            if _parts[1] == 'hsdep_user_first_register_to_active_duration':
                old_series, new_series, custom_bins = hsdep_user_first_register_to_active_duration(old_series, new_series)
                ret = calc_psi_two_series(old_series, new_series, feature_name, custom_bins_list=custom_bins)

    return ret


def calc_psi_two_series(old_series, new_series, feature_name, custom_bins=None, custom_bins_list=None):
    old_series = old_series[old_series != 'feature no key']
    new_series = new_series[new_series != 'feature no key']

    old_series_filter_na = filter_na(old_series)
    new_series_filter_na = filter_na(new_series)

    if old_series_filter_na.shape[0] == 0 or new_series_filter_na.shape[0] == 0:
        print("data is empty, cannot calc psi")
        return None

    if not (is_series_data_type_numeric(old_series_filter_na) and is_series_data_type_numeric(new_series_filter_na)):
        print("data is not numeric, cannot calc psi")
        return None

    old_series_filter_na = old_series_filter_na.astype(float).round(8)
    new_series_filter_na = new_series_filter_na.astype(float).round(8)

    if custom_bins is None and custom_bins_list is None:
        bins = calc_float_value_bins(old_series_filter_na, feature_name)
    elif custom_bins is not None:
        bins = gen_custom_bins(custom_bins)
    elif custom_bins_list is not None:
        bins = custom_bins_list

    old_bins_data = calc_float_bins_info_by_base_bins(old_series_filter_na, bins)
    new_bins_data = calc_float_bins_info_by_base_bins(new_series_filter_na, bins)

    psi = calc_psi(old_bins_data, new_bins_data)

    ret = {
        'psi': psi,
        'old_bins_data': old_bins_data,
        'new_bins_data': new_bins_data,
        'old_data_cnt': old_series_filter_na.shape[0],
        'new_data_cnt': new_series_filter_na.shape[0],

    }

    ret['desc'] = fmt_bins_data(ret)

    return ret


def fmt_bins_data(data):
    ret = ""
    ret += '样本量：旧系统：[%s] 新系统：[%s]\n' % (data['old_data_cnt'], data['new_data_cnt'])
    ret += 'psi: %s\n' % data['psi']

    ret += "\n"

    old_bins_data = data['old_bins_data']
    new_bins_data = data['new_bins_data']

    bins_data1 = np.array([[x[0], x[1], int(x[2])] for x in old_bins_data])
    bins_data2 = np.array([[x[0], x[1], int(x[2])] for x in new_bins_data])

    s3 = '-----旧系统----'
    s4 = str(bins_data1)
    s5 = '-----新系统----'
    s6 = str(bins_data2)

    s7 = '-----绝对差异-----'
    absolute_diff = []
    relatively_diff = []
    for i in range(len(bins_data1)):
        diff = float(bins_data2[i][1]) - float(bins_data1[i][1])
        absolute_diff.append('%s%%' % round(diff * 100, 2))

        if float(bins_data1[i][1]) >= 0.00001:
            rel_diff = (float(bins_data2[i][1]) - float(bins_data1[i][1])) / float(bins_data1[i][1])
            relatively_diff.append('%s%%' % round(rel_diff * 100, 2))
        else:
            relatively_diff.append('0%')

    #     diff = []
    #     for i in range(len(bins_data1)):
    #         diff.append(round(float(bins_data2[i][1])-float(bins_data1[i][1]),4))

    s8 = str(absolute_diff) + '\n\n-----相对差异-----\n' + str(relatively_diff)

    ret = '%s\n%s\n%s\n%s\n%s\n%s\n%s' % (ret, s3, s4, s5, s6, s7, s8)

    return ret


def hsdep_user_first_register_to_active_duration(old_series, new_series):
    old_series = old_series / 3600000
    new_series = new_series / 3600000

    return old_series, new_series, convert_bins('0,1,3,4,12,24,48,72+')
