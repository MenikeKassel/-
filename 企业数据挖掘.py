# -*- coding: utf-8 -*-
# @Time : 2021/12/29 0:40
# @Author : menike
# @File : 企业数据挖掘.py
# @Software: PyCharm
import numpy
import numpy as np
import numpy as numpy
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Geo
from pyecharts.charts import HeatMap
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Scatter3D
from pyecharts.charts import Line
import random
import math
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
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


# 绘制热度图
def draw_heat(gp, v_max):
    value = [[i, j, round(gp.values[i][j])] for i in range(gp.index.shape[0]) for j in range(gp.columns.shape[0])]
    c = HeatMap()
    c.add_xaxis(list(gp.index))
    c.add_yaxis(
        "",
        list(gp.columns),
        value,
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
    )
    c.set_global_opts(
        title_opts=opts.TitleOpts(title="招聘信息数据挖掘",subtitle="企业热度图"),
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=v_max),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45))
    )
    return c


# post_time	url	company_name	company_size
# company_type	job_type	job_name
# edu	salary	people_need	walfare	city
# workingexp	company_area	work_place
# require_content


def deal(data):
    return data.to_list()


def encode(df):
    df_arr = df.apply(deal, axis=1).tolist()
    te = TransactionEncoder()
    df_tf = te.fit_transform(df_arr)
    df = pd.DataFrame(df_tf, columns=te.columns_)
    return df


def metrics(r, f):
    ans = []
    for i in range(r.shape[0]):
        item = r.iloc[i]
        ans.append(f(item))
    return ans


def allconf(item):
    return item.support / max(item['antecedent support'], item['consequent support'])


def cosine(item):
    return item.support / math.sqrt(item['antecedent support'] * item['consequent support'])


def Jaccard(item):
    return item.support / (item['antecedent support'] + item['consequent support'] - item.support)


def maxconf(item):
    return max(item.support / item['antecedent support'], item.support / item['consequent support'])


def Kulczynski(item):
    return 0.5 * (item.support / item['antecedent support'] + item.support / item['consequent support'])


def get_rules(frequent_items):
    rules = association_rules(frequent_items, metric='lift')
    rules = rules.sort_values(by=['lift'], ascending=False).reset_index(drop=True)
    rules = rules.drop(['leverage', 'conviction'], axis=1)
    rules['cosine'] = metrics(rules, cosine)
    rules['Jaccard'] = metrics(rules, Jaccard)
    rules['Allconf'] = metrics(rules, allconf)
    rules['Maxconf'] = metrics(rules, maxconf)
    rules['Kulczynski'] = metrics(rules, Kulczynski)
    return rules


def draw_scatter(rules):
    # 配置 config
    config_xAxis3D = "support"
    config_yAxis3D = "confidence"
    config_zAxis3D = "lift"
    config_color = "support"
    config_symbolSize = "lift"
    # 构造数据
    data = [
        [
            rules.loc[i][config_xAxis3D],
            rules.loc[i][config_yAxis3D],
            rules.loc[i][config_zAxis3D],
            rules.loc[i][config_color],
            rules.loc[i][config_symbolSize],
            i,
        ]
        for i in range(rules.shape[0])
    ]

    s3 = Scatter3D(init_opts=opts.InitOpts(width="700px", height="320px"))  # bg_color="black"
    s3.add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(
            name=config_xAxis3D,
            type_="value"
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name=config_yAxis3D,
            type_="value"
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name=config_zAxis3D,
            type_="value"
        ),
        grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
    )
    s3.set_global_opts(
        title_opts=opts.TitleOpts(title="\n\n\n\n\n\n\n\n\n\n招聘信息数据挖掘", subtitle="企业关联规则评价散点图"),
        visualmap_opts=[
            opts.VisualMapOpts(
                type_="color",
                is_calculable=True,
                dimension=3,
                pos_top="10",
                max_=0.5,
                range_color=[
                    "#1710c0",
                    "#0b9df0",
                    "#00fea8",
                    "#00ff0d",
                    "#f5f811",
                    "#f09a09",
                    "#fe0300",
                ],
            )
        ]
    )
    return s3


if __name__ == '__main__':
    data = pd.read_csv("./data/data.csv")
    Recruitna = delete(data)
    data = eval_salary(Recruitna)
    with open('city_to_province.json', encoding='utf-8') as f:
        d = json.load(f)
    data = data.drop(data[data.city == '其他'].index)
    pro = []
    for i in range(0, len(data)):
        pro.append(d[data.iloc[i]['city']])
    # 增加省份列
    data.loc[:, 'province'] = pro
    m = []
    # print(data['s_average'])
    for i in data['s_average']:
        # print(i)
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
    data.loc[:, 's_average1'] = m
    firm = data[['company_name', 'company_type', 'company_size', 'city']].drop_duplicates(subset=['company_name'],
                                                                                          keep='first')
    print(firm.shape[0])
    df = firm['company_type'].value_counts()
    x = list(df.index.values)
    y = [int(x) for x in df.values]
    bar = Bar()
    bar.add_xaxis(x)
    bar.add_yaxis("", y)
    bar.set_global_opts(title_opts=opts.TitleOpts(

        title='招聘信息的数据挖掘',
        subtitle='企业类型图'), xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)))
    bar.render("企业.html")

    df = firm['company_size'].value_counts()
    x = list(df.index.values)
    y = [int(x) for x in df.values]
    pie = Pie()
    pie.add("", [list(z) for z in zip(x, y)])
    pie.set_global_opts(title_opts=opts.TitleOpts(

        title=

              '\n\n招聘信息的数据挖掘',
        subtitle='企业规模图'))
    pie.render('企业规模.html')
    df = firm.city.value_counts()
    x = list(df.index.values)
    y = [int(x) for x in df.values]
    # m = Geo()
    # m.add_schema(maptype="china",
    #              itemstyle_opts=opts.ItemStyleOpts(color="#404a59", border_color="#fff11"),
    #              )
    # m.add_coordinate_json('city_location.json')
    # m.add("", [list(z) for z in zip(x, y)], symbol_size=8)
    # m.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # m.set_global_opts(
    #     visualmap_opts=opts.VisualMapOpts()
    # )
    # m.render("企业地理分布.html")
    gp = data.pivot_table('s_average', index='company_type', columns='company_size', aggfunc='mean', margins=True,
                          fill_value=0)
    order = ['少于50人', '50-150人', '150-500人', '500-1000人', '1000-5000人', '5000-10000人', '10000人以上', 'All']
    gp = gp[order]
    c = draw_heat(gp, gp.values.max())
    c.render("企业热度.html")
    print("开出最高薪资的企业如下:")
    print(data[data.s_max == data.s_max.max()].company_name)
    c_s = data[['company_type', 'company_size', 's_average1']]
    c_s = encode(c_s)
    frequent_items = apriori(c_s, min_support=0.05, use_colnames=True, max_len=4).sort_values(by='support',
                                                                                              ascending=False)
    frequent_items.head(10)
    rules = get_rules(frequent_items)
    print(rules.head(10))
    s = draw_scatter(rules)
    s.render("企业散点.html")
