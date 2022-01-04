# -*- coding: utf-8 -*-
# @Time : 2021/12/30 0:12
# @Author : menike
# @File : K.py
# @Software: PyCharm
#KNNf分类
import matplotlib.pyplot as plt
import pandas as pd
import json
import pandas as pd
import numpy as np
import graphviz
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import re
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from mlxtend.preprocessing import TransactionEncoder
from pyecharts import options as opts
from pyecharts.charts import Bar
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
def deal(data):
    return data.to_list()
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
def city_eval(city):
    data1 = [['一线城市', '北京'],
             ['一线城市', '上海'],
             ['一线城市', '广州'],
             ['一线城市', '深圳'],
             ['新一线城市', '成都'],
             ['新一线城市', '重庆'],
             ['新一线城市', '杭州'],
             ['新一线城市', '武汉'],
             ['新一线城市', '西安'],
             ['新一线城市', '天津'],
             ['新一线城市', '苏州'],
             ['新一线城市', '南京'],
             ['新一线城市', '郑州'],
             ['新一线城市', '长沙'],
             ['新一线城市', '东莞'],
             ['新一线城市', '沈阳'],
             ['新一线城市', '青岛'],
             ['新一线城市', '合肥'],
             ['新一线城市', '佛山'],
             ['二线城市', '无锡市'],
             ['二线城市', '佛山市'],
             ['二线城市', '合肥市'],
             ['二线城市', '大连市'],
             ['二线城市', '福州市'],
             ['二线城市', '厦门市'],
             ['二线城市', '哈尔滨市'],
             ['二线城市', '济南市'],
             ['二线城市', '温州市'],
             ['二线城市', '南宁市'],
             ['二线城市', '长春市'],
             ['二线城市', '泉州市'],
             ['二线城市', '石家庄市'],
             ['二线城市', '贵阳市'],
             ['二线城市', '南昌市'],
             ['二线城市', '金华市'],
             ['二线城市', '常州市'],
             ['二线城市', '南通市'],
             ['二线城市', '嘉兴市'],
             ['二线城市', '太原市'],
             ['二线城市', '徐州市'],
             ['二线城市', '惠州市'],
             ['二线城市', '珠海市'],
             ['二线城市', '中山市'],
             ['二线城市', '台州市'],
             ['二线城市', '烟台市'],
             ['二线城市', '兰州市'],
             ['二线城市', '绍兴市'],
             ['二线城市', '海口市'],
             ['二线城市', '扬州市'],
             ['三线城市', '汕头市'],
             ['三线城市', '揭阳市'],
             ['三线城市', '江门市'],
             ['三线城市', '湛江市'],
             ['三线城市', '潮州市'],
             ['三线城市', '肇庆市'],
             ['三线城市', '清远市'],
             ['三线城市', '梅州市'],
             ['三线城市', '湖州市'],
             ['三线城市', '舟山市'],
             ['三线城市', '丽水市'],
             ['三线城市', '镇江市'],
             ['三线城市', '盐城市'],
             ['三线城市', '泰州市'],
             ['三线城市', '淮安市'],
             ['三线城市', '连云港市'],
             ['三线城市', '宿迁市'],
             ['三线城市', '潍坊市'],
             ['三线城市', '临沂市'],
             ['三线城市', '济宁市'],
             ['三线城市', '淄博市'],
             ['三线城市', '威海市'],
             ['三线城市', '泰安市'],
             ['三线城市', '保定市'],
             ['三线城市', '唐山市'],
             ['三线城市', '廊坊市'],
             ['三线城市', '邯郸市'],
             ['三线城市', '沧州市'],
             ['三线城市', '秦皇岛市'],
             ['三线城市', '洛阳市'],
             ['三线城市', '商丘市'],
             ['三线城市', '南阳市'],
             ['三线城市', '新乡市'],
             ['三线城市', '乌鲁木齐市'],
             ['三线城市', '漳州市'],
             ['三线城市', '莆田市'],
             ['三线城市', '宁德市'],
             ['三线城市', '龙岩市'],
             ['三线城市', '三明市'],
             ['三线城市', '南平市'],
             ['三线城市', '九江市'],
             ['三线城市', '赣州市'],
             ['三线城市', '上饶市'],
             ['三线城市', '呼和浩特市'],
             ['三线城市', '包头市'],
             ['三线城市', '芜湖市'],
             ['三线城市', '蚌埠市'],
             ['三线城市', '阜阳市'],
             ['三线城市', '马鞍山市'],
             ['三线城市', '滁州市'],
             ['三线城市', '安庆市'],
             ['三线城市', '桂林市'],
             ['三线城市', '柳州市'],
             ['三线城市', '银川市'],
             ['三线城市', '三亚市'],
             ['三线城市', '遵义市'],
             ['三线城市', '绵阳市'],
             ['三线城市', '南充市'],
             ['三线城市', '宜昌市'],
             ['三线城市', '襄阳市'],
             ['三线城市', '荆州市'],
             ['三线城市', '黄冈市'],
             ['三线城市', '咸阳市'],
             ['三线城市', '衡阳市'],
             ['三线城市', '株洲市'],
             ['三线城市', '湘潭市'],
             ['三线城市', '岳阳市'],
             ['三线城市', '郴州市'],
             ['三线城市', '大庆市'],
             ['三线城市', '鞍山市'],
             ['三线城市', '吉林市'],
             ['四线城市', '韶关市'],
             ['四线城市', '常德市'],
             ['四线城市', '六安市'],
             ['四线城市', '汕尾市'],
             ['四线城市', '西宁市'],
             ['四线城市', '茂名市'],
             ['四线城市', '驻马店市'],
             ['四线城市', '邢台市'],
             ['四线城市', '南充市'],
             ['四线城市', '宜春市'],
             ['四线城市', '大理市'],
             ['四线城市', '丽江市'],
             ['四线城市', '延边朝鲜族自治州'],
             ['四线城市', '衢州市'],
             ['四线城市', '黔东南苗族侗族自治州'],
             ['四线城市', '景德镇市'],
             ['四线城市', '开封市'],
             ['四线城市', '红河哈尼族彝族自治州'],
             ['四线城市', '北海市'],
             ['四线城市', '黄冈市'],
             ['四线城市', '东营市'],
             ['四线城市', '怀化市'],
             ['四线城市', '阳江市'],
             ['四线城市', '菏泽市'],
             ['四线城市', '黔南布依族苗族自治州'],
             ['四线城市', '宿州市'],
             ['四线城市', '日照市'],
             ['四线城市', '黄石市'],
             ['四线城市', '周口市'],
             ['四线城市', '晋中市'],
             ['四线城市', '许昌市'],
             ['四线城市', '拉萨市'],
             ['四线城市', '锦州市'],
             ['四线城市', '佳木斯市'],
             ['四线城市', '淮南市'],
             ['四线城市', '抚州市'],
             ['四线城市', '营口市'],
             ['四线城市', '曲靖市'],
             ['四线城市', '齐齐哈尔市'],
             ['四线城市', '牡丹江市'],
             ['四线城市', '河源市'],
             ['四线城市', '德阳市'],
             ['四线城市', '邵阳市'],
             ['四线城市', '孝感市'],
             ['四线城市', '焦作市'],
             ['四线城市', '益阳市'],
             ['四线城市', '张家口市'],
             ['四线城市', '运城市'],
             ['四线城市', '大同市'],
             ['四线城市', '德州市'],
             ['四线城市', '玉林市'],
             ['四线城市', '榆林市'],
             ['四线城市', '平顶山市'],
             ['四线城市', '盘锦市'],
             ['四线城市', '渭南市'],
             ['四线城市', '安阳市'],
             ['四线城市', '铜仁市'],
             ['四线城市', '宣城市'],
             ['四线城市', '永州市'],
             ['四线城市', '黄山市'],
             ['四线城市', '西双版纳傣族自治州'],
             ['四线城市', '十堰市'],
             ['四线城市', '宜宾市'],
             ['四线城市', '丹东市'],
             ['四线城市', '乐山市'],
             ['四线城市', '吉安市'],
             ['四线城市', '宝鸡市'],
             ['四线城市', '鄂尔多斯市'],
             ['四线城市', '铜陵市'],
             ['四线城市', '娄底市'],
             ['四线城市', '六盘水市'],
             ['四线城市', '承德市'],
             ['四线城市', '保山市'],
             ['四线城市', '毕节市'],
             ['四线城市', '泸州市'],
             ['四线城市', '恩施土家族苗族自治州'],
             ['四线城市', '安顺市'],
             ['四线城市', '枣庄市'],
             ['四线城市', '聊城市'],
             ['四线城市', '百色市'],
             ['四线城市', '临汾市'],
             ['四线城市', '梧州市'],
             ['四线城市', '亳州市'],
             ['四线城市', '德宏傣族景颇族自治州'],
             ['四线城市', '鹰潭市'],
             ['四线城市', '滨州市'],
             ['四线城市', '绥化市'],
             ['四线城市', '眉山市'],
             ['四线城市', '赤峰市'],
             ['四线城市', '咸宁市'],
             ['五线城市', '防城港市'],
             ['五线城市', '玉溪市'],
             ['五线城市', '呼伦贝尔市'],
             ['五线城市', '普洱市'],
             ['五线城市', '葫芦岛市'],
             ['五线城市', '楚雄彝族自治州'],
             ['五线城市', '衡水市'],
             ['五线城市', '抚顺市'],
             ['五线城市', '钦州市'],
             ['五线城市', '四平市'],
             ['五线城市', '汉中市'],
             ['五线城市', '黔西南布依族苗族自治州'],
             ['五线城市', '内江市'],
             ['五线城市', '湘西土家族苗族自治州'],
             ['五线城市', '漯河市'],
             ['五线城市', '新余市'],
             ['五线城市', '延安市'],
             ['五线城市', '长治市'],
             ['五线城市', '文山壮族苗族自治州'],
             ['五线城市', '云浮市'],
             ['五线城市', '贵港市'],
             ['五线城市', '昭通市'],
             ['五线城市', '河池市'],
             ['五线城市', '达州市'],
             ['五线城市', '宣城市'],
             ['五线城市', '濮阳市'],
             ['五线城市', '通化市'],
             ['五线城市', '松原市'],
             ['五线城市', '通辽市'],
             ['五线城市', '广元市'],
             ['五线城市', '鄂州市'],
             ['五线城市', '凉山彝族自治州'],
             ['五线城市', '张家界市'],
             ['五线城市', '荆门市'],
             ['五线城市', '来宾市'],
             ['五线城市', '忻州市'],
             ['五线城市', '克拉玛依市'],
             ['五线城市', '遂宁市'],
             ['五线城市', '朝阳市'],
             ['五线城市', '崇左市'],
             ['五线城市', '辽阳市'],
             ['五线城市', '广安市'],
             ['五线城市', '萍乡市'],
             ['五线城市', '阜新市'],
             ['五线城市', '吕梁市'],
             ['五线城市', '池州市'],
             ['五线城市', '贺州市'],
             ['五线城市', '本溪市'],
             ['五线城市', '铁岭市'],
             ['五线城市', '自贡市'],
             ['五线城市', '锡林郭勒盟'],
             ['五线城市', '白城市'],
             ['五线城市', '白山市'],
             ['五线城市', '雅安市'],
             ['五线城市', '酒泉市'],
             ['五线城市', '天水市'],
             ['五线城市', '晋城市'],
             ['五线城市', '巴彦淖尔市'],
             ['五线城市', '随州市'],
             ['五线城市', '兴安盟'],
             ['五线城市', '临沧市'],
             ['五线城市', '鸡西市'],
             ['五线城市', '迪庆藏族自治州'],
             ['五线城市', '攀枝花'],
             ['五线城市', '鹤壁市'],
             ['五线城市', '黑河市'],
             ['五线城市', '双鸭山市'],
             ['五线城市', '三门峡市'],
             ['五线城市', '安康市'],
             ['五线城市', '乌兰察布市'],
             ['五线城市', '庆阳市'],
             ['五线城市', '伊犁哈萨克自治州'],
             ['五线城市', '儋州市'],
             ['五线城市', '哈密市'],
             ['五线城市', '海西蒙古族藏族自治州'],
             ['五线城市', '甘孜藏族自治州'],
             ['五线城市', '伊春市'],
             ['五线城市', '陇南市'],
             ['五线城市', '乌海市'],
             ['五线城市', '林芝市'],
             ['五线城市', '怒江傈僳族自治州'],
             ['五线城市', '朔州市'],
             ['五线城市', '阳泉市'],
             ['五线城市', '嘉峪关市'],
             ['五线城市', '鹤岗市'],
             ['五线城市', '张掖市'],
             ['五线城市', '辽源市'],
             ['五线城市', '吴忠市'],
             ['五线城市', '昌吉回族自治州'],
             ['五线城市', '大兴安岭地区'],
             ['五线城市', '巴音郭楞蒙古自治州'],
             ['五线城市', '阿坝藏族羌族自治州'],
             ['五线城市', '日喀则市'],
             ['五线城市', '阿拉善盟'],
             ['五线城市', '巴中市'],
             ['五线城市', '平凉市'],
             ['五线城市', '阿克苏地区'],
             ['五线城市', '定西市'],
             ['五线城市', '商洛市'],
             ['五线城市', '金昌市'],
             ['五线城市', '七台河市'],
             ['五线城市', '石嘴山市'],
             ['五线城市', '白银市'],
             ['五线城市', '铜川市'],
             ['五线城市', '武威市'],
             ['五线城市', '吐鲁番市'],
             ['五线城市', '固原市'],
             ['五线城市', '山南市'],
             ['五线城市', '临夏回族自治州'],
             ['五线城市', '海东市'],
             ['五线城市', '喀什地区'],
             ['五线城市', '甘南藏族自治州'],
             ['五线城市', '昌都市'],
             ['五线城市', '中卫市'],
             ['五线城市', '资阳市'],
             ['五线城市', '阿勒泰地区'],
             ['五线城市', '塔城地区'],
             ['五线城市', '博尔塔拉蒙古自治州'],
             ['五线城市', '海南藏族自治州'],
             ['五线城市', '克孜勒苏柯尔克孜自治州'],
             ['五线城市', '阿里地区'],
             ['五线城市', '和田地区'],
             ['五线城市', '玉树藏族自治州'],
             ['五线城市', '那曲市'],
             ['五线城市', '黄南藏族自治州'],
             ['五线城市', '海北藏族自治州'],
             ['五线城市', '果洛藏族自治州'],
             ['五线城市', '三沙市']]
    c = {}
    city1 = []
    city2 = []
    city3 = []
    city4 = []
    city5 = []
    city6 = []
    for i in data1:
        if i[0] == "一线城市":
            city1.append(i[1])
        elif i[0] == "新一线城市":
            city2.append(i[1])
        elif i[0] == "二线城市":
            city3.append(i[1])
        elif i[0] == "三线城市":
            city4.append(i[1])
        elif i[0] == "四线城市":
            city5.append(i[1])
        elif i[0] == "五线城市":
            city6.append(i[1])

    # print(city1)
    # print(city2)
    # print(city5)

    i =city
    if i in city1 or (i + "市") in city1:
        return 1
    elif i in city2 or (i + "市") in city2 or (i + "州") in city2:
        return 2
    elif i in city3 or (i + "市") in city3 or (i + "州") in city3:
        return 3
    elif i in city4 or (i + "市") in city4 or (i + "州") in city4:
        return 4
    elif i in city5 or (i + "市") in city5 or (i + "州") in city5:
        return 5
    elif i in city6 or (i + "市") in city6 or (i + "州") in city6:
        return 6
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

def encode(df):
    df_arr = df.apply(deal, axis=1).tolist()
    te = TransactionEncoder()
    df_tf = te.fit_transform(df_arr)
    df = pd.DataFrame(df_tf, columns=te.columns_)
    return df

if __name__ == '__main__':
    data = pd.read_csv("./data/data.csv")
    data = delete(data)
    data = eval_salary(data)
    data = city_sum(data)
    data = salary_sum(data)
    print(data.info())

    people = []
    for i in data['people_need']:
        people_sum = i[1:-1]
        if people_sum!='若干':
            people.append(float(people_sum))
        else:
            people.append(np.NAN)#如果招聘人数为若干，将值替换为空值
    data['people_need'] = people

    exp_sum=[]
    for j in data['workingexp']:
        if j =='无工作经验':
            exp_sum.append(0)
        elif j =='10年以上经验':
            exp_sum.append(10)
        else:
            e = j.split("-")
            if len(e)==1:
                exp_sum.append(float(e[0][0]))
            else:
                exp_sum.append(  (float(e[1][0])-float(e[0])/2))
    #print(exp_sum)
    data['workingexp1'] = exp_sum
    edu_sum = []
    for i in data['edu']:
        if i=="初中及以下":
            edu_sum.append(1)
        elif i=="中技":
            edu_sum.append(2)
        elif i=="中专":
            edu_sum.append(3)
        elif i=="高中":
            edu_sum.append(4)
        elif i=="大专":
            edu_sum.append(5)
        elif i=="本科":
            edu_sum.append(6)
        elif i=="硕士":
            edu_sum.append(7)
        elif i=="博士":
            edu_sum.append(8)
    data['edu_sum'] = edu_sum

    city_sum = []
    for i in data['city']:
        city_sum.append(city_eval(i))
        # print(i)
    # print(city_sum)
    data["city2"] = city_sum
    data = data.dropna()
    print(data)
    y = []
    for i in data['s_average_sum']:
        if i == 'A1':
            i = "0"
            y.append(i)
        elif i == 'B1':
            i = "0"
            y.append(i)
        elif i == 'C1':
            i = "1"
            y.append(i)
        elif i == 'D1':
            i = "2"
            y.append(i)
    data['s_average_sum'] = y
    y = data['s_average_sum']
    x = data[['edu_sum', 'people_need', 'workingexp1', 'city2']]

    '''
    特征转换:
    DictVectorizer的功能： DictVectorizer对非数字化的处理方式是: 借助原特征的名称，组合成新的特征，
    并采用0 / 1的方式进行量化，而数值型的特征转化比较方便，一般情况维持原值即可
    '''
    from sklearn.feature_extraction import DictVectorizer
    #sparse=False表示的是非稀疏矩阵
    vec = DictVectorizer(sparse=False)
    #先进行拟合然后对字典列表进行转换，转换成特征矩阵
    x = vec.fit_transform(x.to_dict(orient='record'))
    print(vec.feature_names_)
    # 数据集中抽取30%作为训练集，需要导入sklearn.model_selection中的train_test_split
    from sklearn.model_selection import train_test_split

      # 导入决策树模型并对测试特征数据进行预测
    # 使用默认配置初始化决策树分类器
    # 如果设置criterion="entropy"则是C4.5算法，参数缺省则是gini系数，是CART算法。
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    dtc = DecisionTreeClassifier(criterion="gini",max_depth=4)
    # 训练数据进行模型学习
    dtc.fit(x_train, y_train)
    # 可视化决策树
    from sklearn.tree import export_graphviz

    # with open(r"F:/tree.dot", "w",encoding='utf-8') as file:
    #     export_graphviz(dtc, feature_names=vec.get_feature_names_out(), class_names=y,out_file=file,fontname="FangSong")
    # 对测试数据的类别作预测
    result = dtc.predict(x_test)
    print(result)
    # # 打印测试数据的准确度
    # x= [1,2,3]
    # accuracy_score_result = [0.794,0.43, 0.60]
    # recall_score_result = [ 0.92,0.26,0.33]
    # f1_score_result = [0.855,0.32, 0.43]
    #
    # Bar = (
    #     Bar()
    #         .add_xaxis(x)
    #         .add_yaxis("accuracy", y_axis=accuracy_score_result)
    #         .add_yaxis("recall", recall_score_result)
    #         .add_yaxis("f1_score", f1_score_result)
    #         .set_global_opts(title_opts=opts.TitleOpts(title="招聘信息的决策树建模", subtitle="指标比较"))
    # )
    #
    # Bar.render(f'人体预测.html')
    from sklearn import tree
    from sklearn import metrics
    print("准确度:", dtc.score(x_test, y_test))
    pre = dtc.predict(x_test)
    cn = metrics.confusion_matrix(y_test,pre)
    print(cn)
    print(classification_report(y_test, dtc.predict(x_test)))
    import seaborn as sns

    sns.heatmap(cn, cmap=sns.color_palette("Blues"), annot=True,square=True)
    plt.show()



    from graphviz import Source
    from sklearn.tree import export_graphviz
    import os

    image_path = "./images"
    os.makedirs(image_path, exist_ok=True)

    export_graphviz(dtc,
                    out_file=os.path.join(image_path, "tree.dot"),
                    feature_names=vec.get_feature_names_out(), class_names=y,  fontname="FangSong",filled=True)
    s = Source.from_file(os.path.join(image_path, "tree.dot"))
    s.view()

    require = data['require_content']
    #print(require)
#dot -Tpdf tree.dot -o tree.pdf
#dot -Tpng tree.dot -o tree.png

#。早期有些国外学者运用文本挖掘方法研究人才市场需求。1995年的时候，Todd等人在报纸上收集了美国和加拿大的有关信息系统岗位的信息，进行关键词提取并进行频数分析；2006年时Lee对一些信息技术管理岗位信息进行分析构建了技能分类目录，产生了词典的雏形;2010年时 MS Sodhi和B-GSon在以上研究的基础上，从招聘网站采集了关于运筹学专业相关的就业信息，构建了技能词典和关键词词典，在进行频数分析的基础上又进一步做了交叉分析和相关性分析，研究了运筹类专业技能在不同行业需求的差异，分析的相对深入；
#我国关于数据挖掘的研究晚于国外，尚未形成整体的框架和格局，学者主要研究的方向大多是关于数据挖掘算法的理论基础、应用场景和一些简单的优化修正。比如中科院数学研究所、中国科技大学针对关联规则进行了诸多研究和改进，中国人民大学统计学系数据挖掘中心讨论了诸多关于决策树算法的应用，复旦大学、浙江大学等高校联合研究了关于非结构化数据的网络数据挖掘。国内研究的重点大都在计算机上，针对某方面的文本信息的挖掘并不多。随着时代的发展，关于文本信息的挖掘和分析显得越来越重要，也有越来越多的研究者开始研究这一方向。
