# -*- coding: utf-8 -*-
# @Time : 2021/12/24 23:43
# @Author : menike
# @File : 数据获取.py
# @Software: PyCharm

import csv
import time

from lxml import etree
import requests
import re
import json
import random

# '070500', '010000', '020000', '030200', '040000', '180200', '200200', '080200', '070200',
# 获取IP伪装
# def get_fake_IP():
#     ip_page = requests.get(  # 获取200条IP
#         'http://www.89ip.cn/tqdl.html?num=60&address=&kill_address=&port=&kill_port=&isp=')
#     proxies_list = re.findall(
#         r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)(:-?[1-9]\d*)',
#         ip_page.text)
#
#     # 转换proxies_list的元素为list,最初为'tuple'元组格式
#     proxies_list = list(map(list, proxies_list))
#
#     # 格式化ip  ('112', '111', '217', '188', ':9999')  --->  112.111.217.188:9999
#     for u in range(0, len(proxies_list)):
#         # 通过小数点来连接为字符
#         proxies_list[u] = '.'.join(proxies_list[u])
#         # 用rindex()查找最后一个小数点的位置，
#         index = proxies_list[u].rindex('.')
#         # 将元素转换为list格式
#         proxies_list[u] = list(proxies_list[u])
#         # 修改位置为index的字符为空白（去除最后一个小数点）
#         proxies_list[u][index] = ''
#         # 重新通过空白符连接为字符
#         proxies_list[u] = ''.join(proxies_list[u])
#
#     # proxies = {'协议':'协议://IP:端口号'}
#     # 'https':'https://59.172.27.6:38380'
#
#     return "'" + random.choice(proxies_list) + "'"
#
#
# proxies = {'http': get_fake_IP()}
# '070500', '010000', '020000', '030200', '040000', '180200', '200200', '080200', '070200', '090200', '060000',
# '030800', '230300', '230200', '070300', '250200', '190200', '150200', '080300', '170200', '050000', '120300',
# '120200', '220200', '240200', '110200', '091700', '250500', '220500', '210400', '221400', '230800', '072100',
# '251600', '090600', '121300', '172000', '252000', '101100', '271100', '100900', '121000', '100800', '280800',
# '181000', '181800', '140800', '030600', '230600', '131100', '231500', '150700', '271500', '092100', '130800',
# '290600', '091300', '091600', '140300', '141000', '260200', '320800', '310700', '320500', '320300', '100200',
values = ['030300', '030000', '080400', '01']

f = open(
    './data/招聘信息.csv',
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
error_city = []
for value in values:
    try:
        time.sleep(3)
        for page in range(1, 20):
            url = f'https://search.51job.com/list/{value},000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25B7%25A5%25E7%25A8%258B,2,' \
                  f'{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
                ,
                "Cookie": "_uab_collina=164035915534466794789822; adv=ad_logid_url%3Dhttps%253A%252F%252Ftrace.51job.com%252Ftrace.php%253Fpartner%253Dsem_pcbaidu5_128152%2526ajp%253DaHR0cHM6Ly9ta3QuNTFqb2IuY29tL3RnL3NlbS9MUF8yMDIwXzEuaHRtbD9mcm9tPWJhaWR1YWQ%253D%2526k%253Dd946ba049bfb67b64f408966cbda3ee9%2526bd_vid%253D11852377956051259878%26%7C%26; guid=b498af321245ea2b32ff19cac29c7f20; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lastvisit%3D250200%26%7C%26; acw_tc=781bad2d16404486633453636e7f84020ccc7814c2b0868692272f9b002ee4; acw_sc__v2=61c742d46e09eececedf41fd605b99fb46fe468a; search=jobarea%7E%60090300%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60090300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60090300%2C010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60090300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60090200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; ssxmod_itna=eqUxcDRD0WDtD=3GHXhCDjo/z=4RA2DT4OD7IdD/KQmDnqD=GFDK40oEgUEPiPNfQAYaLT7Wciqdq5aZxh3Pbdox0aDbqGkviYEheDx1q0rD74irDDxD3DbbdDSDWKD9D0+8BnLuKGWDm+8DWPDYxDrfrKDRxi7DDHQ7x07DQv87C+4f1YFdtym21RhqQG8D7HpDlpxfUgwL9f4g1BAptq47DGddAMD3AGUeDit+DA3mx0koq0Oc=vz8=EU66v1DFRqfG0qbnq7K0Roqn00rCWyaG44eAx0Hm007mMqCshyyLDDiZLPmC+DD; ssxmod_itna2=eqUxcDRD0WDtD=3GHXhCDjo/z=4RA2DT4OD7KG9bdzDBwBeq7PGCitvTQWCx8O0QsNIpg54hedldvN8d53jrr45PbGSXG/Qmc5bvP2AafH07h9CDbw/8+UfMRiyfClHh1EdQy/AKaGXj4eXpYQYDP3YzCgik87hTChYG7L335Yiw8SEfDTEf8bXfYjX2CChzWqtHISL/ffKh0oLUfWQHBQd0G62O2PAlQdoX8RnsAnbL4U=0WzLG07Q35cPOx42fKDSfuirOH+9XIRYeU9l8ySenKMe0KASTtjHyaenC24Y0kXoeUyVOEo616xjNHG4PEQfhLGYiRGYKaYuiD3ZDmjGKYEhB38e5tCp+nqUlUD1vrm0OnGse4PPA8jbttwB7DkreatmmpRwYLD1TeGmzfP+eWGBAk+P+tP+U6OiWzfTGiemCTeKefIqmlbjaeO/qO=csGKAtn29WA9P+/tA46c8FsSFRjWPcF+fIRKjk8yk+Fk0msg2scGWDG2/ExzOII2o8iGi05IhhrCiFCwsl8Q0xqmxzDFCQFerN7SIMQxiuDWO+EYr00oDHeK0xq+fvxLpcYD08Dijz0DPjgkC08iDxD==="
                ,
                "Referer": f"https://search.51job.com/list/{value},000000,0000,32,9,99,%2B,2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
                , "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive"
            }  # 头文件模仿网页对网页进行爬虫

            response = requests.get(
                url=url,
                headers=headers,
                timeout=30,

            )
            # 获取资源路径下的网页文件
            # print(response.text)
            html_data = re.findall(
                'window.__SEARCH_RESULT__ =(.*?)</script>',
                response.text)[0]
            # 运用正则表达式findall找到需要的资源，[0]表示爬取出来的是字符串
            json_data = json.loads(html_data)
            # 用json.loads对获取到的字符串进行解码返回python字段
            # pprint.pprint(json)

            engine = json_data['engine_jds']
            # 找到这个字段的内容
            # pprint.pprint(engine)
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
            print(f"{value}地区第{page}页获取完毕")
    except Exception as m:
        print("Error")
        error_city.append(value)
        print(m)
        pass
print(error_city)
