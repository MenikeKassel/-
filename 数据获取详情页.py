# -*- coding: utf-8 -*-
# @Time : 2021/12/25 0:16
# @Author : menike
# @File : 数据获取详情页.py
# @Software: PyCharm

import time
import csv
import requests
from lxml import etree


def get_url(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
        ,
        "Cookie": "_uab_collina=164036252715671937090469; adv=ad_logid_url%3Dhttps%253A%252F%252Ftrace.51job.com%252Ftrace.php%253Fpartner%253Dsem_pcbaidu5_128152%2526ajp%253DaHR0cHM6Ly9ta3QuNTFqb2IuY29tL3RnL3NlbS9MUF8yMDIwXzEuaHRtbD9mcm9tPWJhaWR1YWQ%253D%2526k%253Dd946ba049bfb67b64f408966cbda3ee9%2526bd_vid%253D11852377956051259878%26%7C%26; guid=b498af321245ea2b32ff19cac29c7f20; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; slife=lastvisit%3D250200%26%7C%26; search=jobarea%7E%60090300%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60090300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60090300%2C010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%CA%FD%BE%DD%B7%D6%CE%F6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60090300%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60090200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA32%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; acw_sc__v2=61c75d26c1ccfd9a1e447d466682dc3c2fa05f31; acw_tc=2f624a4c16404573601327122e40808ed9542c90b6124f9a90a7c8aa80d9cd; acw_sc__v3=61c7649920fe5556567eba112d2e03860c0ed5ab; ssxmod_itna=iqmx97DQ3QqWuDBcDeTm8KEhqCqLw+4Y5+Y4DCbUDBwRo4iNDnD8x7YDv+f5WNTi0r4W17=m2P5QQ04aKHdk9hDxFoUz34GLDmKDy774aeDxpq0rD74irDDxD3DbSdDSDWKD9D0+kSBuqtDm4GWCqGfDDoDYR=nDitD4qDBIEdDKqGgCuDKb06PMS2MUjtKFWeyD0UQxBd58Zuo1P9eSk2TPEIqD0P4bGH3bDBtKxP5YmPnDB6pxBjlUuXXUmyB/TN4NODFYi+abo45Chx3iOe=7b+3AijtR77pY7eqtADojYVYbDDAe9+a0DxD=; ssxmod_itna2=iqmx97DQ3QqWuDBcDeTm8KEhqCqLw+4Y5+Y4DCbD8kp80DGN5nxGaiY0EfwOjV=3KPkeMQjA=hSQKdrbhecrGhumAjfqd2GYoUPA6wb6hZgyjp6/uCB986zd8B29Uha5MnGcT/12wtLY5i4tD8gvvAxPhC0KqMi6Y=eP2+Eb3aqTrWwTqEBE6/guMKRG52Au=wQfaaPc35MIN1WWWL1Y+/etirPU=rMn1peciwORz2b7tEGih52U7F/EwIK5EZaEdr=B5h/ANsmhmr0fvfSTxoQ1kzbK9=/T++vTSs+/gcz7STW6NM5dnf1FbGnT5nurlkGxm4DQKPns=WCrWH5+4S0iFewerYjdweW+KRr1QaKSWGwDNoTGShEnkemD7jbxnpO4ClBrjShHlrpRiiqr/kbVDCubtNCF=oAsmIARs5Wsw+AY6v/T71xbaPCDcvDZWxnLrWpv8eLDDwpG7DGcDG7E=xWAq1Y3qDP4D==="
        ,
        "Referer": f"{url}"
        , "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive"
    }  # 头文件模仿网页对网页进行爬虫

    resp = requests.get(url, headers=headers, timeout=30)
    # print(resp.text)
    try:
        content = resp.content.decode('gbk')
    except:
        content = resp.content.decode('utf-8')
    # print(content)
    tree = etree.HTML(content)
    position_info = tree.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()")
    company_info = tree.xpath("/html/body/div[3]/div[2]/div[3]/div[3]/div/text()")
    # vc/html/body/div[3]/div[2]/div[3]/div[3]/div
    print(position_info)
    print(company_info)
    return position_info, company_info


if __name__ == '__main__':

    sheet_name = "./data/data.csv"
    urls = []
    # 数据文件有问题数据
    with open(sheet_name, encoding="utf-8", errors="ignore") as f:
        # 可通过列名读取列值，表中有空值
        data = csv.DictReader(_.replace("\x00", "") for _ in f)
        headers = next(data)
        # print(headers)
        for row in data:
            print(row["职位详情页"])
            urls.append(row["职位详情页"])

        # print(urls)

        for url in urls:
            time.sleep(10)
            try:
                print(url)
                f = open(
                    './data/详情页.csv',
                    mode='a',
                    encoding='utf-8-sig',
                    newline='')
                # 创建一个csv文件，mode=a表示对文件只能写入，encoding是内容文字，newline避免有换行字符等产生
                print("打开文件成功")
                csv__ = csv.DictWriter(
                    f,
                    fieldnames=[
                        '职位详情页', "公司信息"]
                )

                csv__.writeheader()
                print("start")
                position_info, company_info = get_url(url)
                # print(position_info)
                print("end")
                dit = {'职位详情页': position_info,
                       "公司信息": company_info}
                # 把拆分的数据整合进一个新的字典
                csv__.writerow(dit)
                print("写入文件成功")


            except Exception as m:
                pass
                print("error")
                print(m)
                time.sleep(8)
