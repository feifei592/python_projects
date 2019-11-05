"""使用正则表达式直接爬取内容(没有用到bs4)"""
import requests
import re


def spider(url1):
    try:
        # 获取网页HTML
        r = requests.get(url1, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html1 = r.text
        return html1
    except:
        print("爬取失败")


# 使用正则表达式匹配需要的信息
url = "http://news.baidu.com"
html = spider(url)
pattern = re.compile(r'<a href="(.*?)" .*? target="_blank".*?>(.*?)</a>')
data = pattern.findall(html)
list0 = []
for v in data:
    # print(v)
    if v[0] != '' and v[1] != '':
        list1 = list()
        list1.append(v[0])
        list1.append(v[1])
        list0.append(list1)
print(list0[0:15])






