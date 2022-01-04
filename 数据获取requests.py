# -*- coding: utf-8 -*-
# @Time : 2021/12/23 22:36
# @Author : menike
# @File : 数据获取requests.py
# @Software: PyCharm
import codecs
import csv

import requests
import re
import json
import pprint

f = open(
    './data/前程无忧.csv',
    mode='a',
    encoding='utf-8-sig',
    newline='')
# 创建一个csv文件，mode=a表示对文件只能写入，encoding是内容文字，newline避免有换行字符等产生
csv__ = csv.DictWriter(
    f,
    fieldnames=[
        '职位名称',
        '基本信息',
        '公司名字',
        '工作地点',
        '公司类型',
        '公司规模',
        '公司性质',
        '福利',
        '工资',
        '信息发布时间',
        '职位详情页']
)
# f是创建的csv文件，fieldnames表示列名
csv__.writeheader()
print("输入你的城市:")
citydict = {'成都': '090200', '北京': '010000', }
str = input()
# https://search.51job.com/list/090200%252c010000%252c020000%252c030200,000000,0000,32,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
if str == '成都':
    url = \
        'https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=' \
        '99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '北京':
    url = \
        'https://search.51job.com/list/010000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == \
        '上海':
    url = \
        'https://search.51job.com/list/020000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '广州':
    url = \
        'https://search.51job.com/list/030200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '深圳':
    url = \
        'https://search.51job.com/list/040000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '武汉':
    url = \
        'https://search.51job.com/list/180200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '西安':
    url = \
        'https://search.51job.com/list/200200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '杭州':
    url = \
        'https://search.51job.com/list/080200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '南京':
    url = \
        'https://search.51job.com/list/070200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '重庆':
    url = \
        'https://search.51job.com/list/060000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '东莞':
    url = \
        'https://search.51job.com/list/030800,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '大连':
    url = \
        'https://search.51job.com/list/230300,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '沈阳':
    url = \
        'https://search.51job.com/list/230200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
elif str == '苏州':
    url = \
        'https://search.51job.com/list/070300,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B' \
        ',2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm' \
        '=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
# 不固定url资源路径,通过if和elif对城市进行判断然后选择url
# url='https://search.51job.com/list/090200,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    ,
    "Cookie": "uab_collina=164035915534466794789822; adv=ad_logid_url%3Dhttps%253A%252F%252Ftrace.51job.com%252Ftrace.php%253Fpartner%253Dsem_pcbaidu5_128152%2526ajp%253DaHR0cHM6Ly9ta3QuNTFqb2IuY29tL3RnL3NlbS9MUF8yMDIwXzEuaHRtbD9mcm9tPWJhaWR1YWQ%253D%2526k%253Dd946ba049bfb67b64f408966cbda3ee9%2526bd_vid%253D11852377956051259878%26%7C%26; guid=b498af321245ea2b32ff19cac29c7f20; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; acw_tc=76b20ff116403611810961002e4ba816f7338684ec7d5635aab40b1c08f738; acw_sc__v2=61c5ed3b1974b502e502e0e875bd7f7f469f0e1b; acw_sc__v2=61c5ed3ca88bb479682c57e5b68c006cee80d76a; search=jobarea%7E%60090200%2C010000%2C020000%2C030200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60090200%2C010000%2C020000%2C030200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60070300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C8%ED%BC%FE%B9%A4%B3%CC%27+%2F+%27%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60030200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FACVTE%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; ssxmod_itna=GqAOiIqRxIxxXYG7zbG=eDQQLlDU2bmb3kGeGNoG8zDnqD=GFDK40E5OwjvwjwaI/G3Yw3LBG8DKaY6GST4WOIFgxGLDmKDy7CB2G5D4RKGwD0eG+DD4DWDmnFDnxAQDjxGpc2LkX=DEDYpcDA3Di4D+FLQDmqG0DDt7R4G2D7UcjGhQFq2j7mt3pwxepi+cD0tdxBLaFpTYOccQnqrb=aIqjDDHlOybR7yNW7Ga4epRDB6mxBQMAkX6ACHyBMUDMhDWtGG5BgG0FrPKm7DPnGwUvi4X4rqz7OxdnpDU6+eXxDfbYh4KeD==; ssxmod_itna2=GqAOiIqRxIxxXYG7zbG=eDQQLlDU2bmb3ki4A=WLNG8DBwrgq7pqI8+90hjHGFmidq6xuzoW7ddYEom2hI4XcmA+HevbDL6+b1RQEyjtho/SXqt66px6nza5m9vfnU3mBG7LLdzVssxBitgw7H0picrI5bm7ONU5rei5iNgcCUa4HfayC6GEiW3o=U67Ey2Ppvbgam1fkUbufXAKAHgKAMpLHUO86A+dfv3ez1gy8F740Oav8S2v8MrEnXDSAFNkfHTqTFCHhXiEe33UT23PAYs27paEI3eU85YmytPVz2sDnp7T2YpmxWE/ghWo0/avXhXjawEc6Wroc2vk2vsren1Exa6EQ0UiffEKnPbYtQGgIZQb=K5N4QhjL/W262biZL8Cbuhtf6R=4ulBPs8hFG4DQ95RGe0wA3GVneqYDqiRm7ibWiY6ibvcWXv8Y5GIWKInbc0roi7eP7vcbp059bVKLT/GDNGKCegIP8HMxs8WdcQjxtjrCyDDMk=Ur=YHWSH5CqK+5q7idfkZmiwoilmDxtDDFqD+gwQlnR94PVhNYD=="
    ,
    "Referer": "https://search.51job.com/list/010000,000000,0000,32,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=",
    "X-Requested-With": "XMLHttpRequest"
}  # 头文件模仿网页对网页进行爬虫

response = requests.get(
    url=url,
    headers=headers
)
# 获取资源路径下的网页文件
print(response.text)
html_data = re.findall(
    'window.__SEARCH_RESULT__ =(.*?)</script>',
    response.text)[0]
# 运用正则表达式findall找到需要的资源，[0]表示爬取出来的是字符串
json_data = json.loads(html_data)
# 用json.loads对获取到的字符串进行解码返回python字段
# pprint.pprint(json)

engine = json_data['engine_jds']
# 找到这个字段的内容
pprint.pprint(engine)
for i in engine:
    # pprint.pprint(i)
    title = i['job_name']
    attribute_text = i['attribute_text']
    jjj = ' '.join(attribute_text)
    company_name = i['company_name']
    companyind_text = i['companyind_text']
    companysize_text = i['companysize_text']
    companytype_text = i['companytype_text']
    jobwelf = i['jobwelf']
    providesalary_text = i['providesalary_text']
    updatedate = i['updatedate']
    job_href = i['job_href']
    workarea_text = i['workarea_text']
    # 对找到的列表拆分为多个字典内容

    dit = {
        '职位名称': title,
        '基本信息': jjj,
        '公司名字': company_name,
        '工作地点': workarea_text,
        '公司类型': companyind_text,
        '公司规模': companysize_text,
        '公司性质': companytype_text,
        '福利': jobwelf,
        '工资': providesalary_text,
        '信息发布时间': updatedate,
        '职位详情页': job_href

    }
    # 把拆分的数据整合进一个新的字典
    csv__.writerow(dit)
    # 把dit字典内容写进csv文件
# https://search.51job.com/list/070300,000000,0000,32,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,2.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
# https://search.51job.com/list/070300,000000,0000,32,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,3.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
