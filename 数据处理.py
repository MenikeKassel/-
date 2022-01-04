# -*- coding: utf-8 -*-
# @Time : 2021/12/29 17:32
# @Author : menike
# @File : 数据处理.py
# @Software: PyCharm
import pandas as pd
import json
def delete(data):
    # print(data.info())
    dropNadata = data.dropna()
    # print(dropNadata)
    Recruitna = dropNadata.drop_duplicates()
    # print(Recruitna)
    return Recruitna  #


# 计算薪资平均值
def eval_salary(Recruitna):
    '''
    :param Recruitna: data
    :return: 算出薪资均值
    '''
    Split = Recruitna['salary'].str.split('-', 1, True)
    Split = Split.replace('万/月', '', regex=True)
    Split = Split.replace('千/月', '', regex=True)
    Split = Split.replace('元/天', '', regex=True)
    Split = Split.replace('千以下/月', '', regex=True)
    Split = Split.replace('万以下/年', '', regex=True)
    Split = Split.replace('元/小时', '', regex=True)
    Split = Split.replace('万/年', '', regex=True)
    Split.columns = ['s_min', 's_max']

    # 将拆分出的薪资上下限与原表格联结
    Recruitna = pd.merge(Recruitna, Split, left_on=Recruitna.index, right_on=Split.index).drop(['key_0'], axis=1)

    # 将薪资上下限字段中的字符类型转为数值类型
    Recruitna[['s_min', 's_max']] = Recruitna[['s_min', 's_max']].astype(float)

    # 统一薪资上下限单位为千/月
    Recruitna.loc[Recruitna['salary'].str.contains('万/月'), 's_min'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '万/月'), 's_min'] * 10
    Recruitna.loc[Recruitna['salary'].str.contains('万/月'), 's_max'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '万/月'), 's_max'] * 10
    Recruitna.loc[Recruitna['salary'].str.contains('元/天'), 's_min'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '元/天'), 's_min'] * 21 / 1000
    Recruitna.loc[Recruitna['salary'].str.contains('元/天'), 's_max'] = Recruitna.loc[
        Recruitna['salary'].str.contains('元/天'), 's_min']
    Recruitna.loc[Recruitna['salary'].str.contains('元/小时'), 's_min'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '元/小时'), 's_min'] * 8 * 21 / 1000
    Recruitna.loc[Recruitna['salary'].str.contains('元/小时'), 's_max'] = Recruitna.loc[
        Recruitna['salary'].str.contains('元/小时'), 's_min']
    Recruitna.loc[Recruitna['salary'].str.contains('万/年'), 's_min'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '万/年'), 's_min'] / 12
    Recruitna.loc[Recruitna['salary'].str.contains('万/年'), 's_max'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '万/年'), 's_max'] / 12
    Recruitna.loc[Recruitna['salary'].str.contains('千以下/月'), 's_max'] = Recruitna.loc[
        Recruitna['salary'].str.contains('千以下/月'), 's_min']
    Recruitna.loc[Recruitna['salary'].str.contains('万以下/年'), 's_min'] = Recruitna.loc[Recruitna['salary'].str.contains(
        '万以下/年'), 's_min'] / 12
    Recruitna.loc[Recruitna['salary'].str.contains('万以下/年'), 's_max'] = Recruitna.loc[
        Recruitna['salary'].str.contains('万以下/年'), 's_min']

    # 求出薪资上下限均值
    Recruitna['s_average'] = (Recruitna['s_min'] + Recruitna['s_max']) / 2
    return Recruitna
#对薪资进行概念分层，增加薪资分层
def salary_sum(data):
    m = []
    for i in data['s_average']:
        if i < 6:
            i = "A1"
            m.append(i)
        elif 6 < i <= 10:
            i = "B1"
            m.append(i)
        elif 10 < i <= 16:
            i = "C1"
            m.append(i)
        elif 16 < i:
            i = "D1"
            m.append(i)
        else:
            i = "A1"
            m.append(i)
    data.loc[:, 's_average_sum'] = m
    return data
#增加省份列
def city_sum(data):
    with open('city_to_province.json', encoding='utf-8') as f:
        d = json.load(f)
    data = data.drop(data[data.city == '其他'].index)
    pro = []
    for i in range(0, len(data)):
        pro.append(d[data.iloc[i]['city']])
    # 增加省份列
    data.loc[:, 'province'] = pro
    return data
if __name__ == '__main__':
    #pd.set_option('display.max_columns', None)
    #显示所有列，显示所有rows行
    data = pd.read_csv("C:\\Users\\12973\\Desktop\\51job.csv")
    print(data)
    print(data.info())
    data = delete(data)
    data.dropna()
    print(data)
    print(data.info())
    print(data.describe())

