import requests
import time
import json
import re
import pymysql
from bs4 import BeautifulSoup


db = pymysql.Connect('127.0.0.1', 'root', '622621', 'test')


# 使用requests获取html
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


# 数据添加到数据库
def insert_data(movie, id_data, time_data, stars_data, votes_data, comment):
     cursor = db.cursor()
     cursor.execute('SET CHARACTER SET utf8;')
     sql = 'insert into doubancomment values(%s,%s,%s,%s,%s,%s);'
     cursor.execute(sql, (movie, id_data, time_data, stars_data, votes_data, comment))
     db.commit()#确认提交
     cursor.close()
     print('执行成功')


# 获取具体信息
movielist = []
# 修改URL的起始条数相当于下一页
for i in ["0", "20", "40"]:
    url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E5%8A%A8%E6%BC%AB&start="+i
    html = spider(url)
    string = json.loads(html)
    # print(string["data"])
    # 获取电源名和ID号
    for movie in string["data"]:
        moviename = movie['title']
        movieurl = movie["url"]
        movieid = movie["id"]
        str = moviename+"-"+movieid+"-"+movieurl
        movielist.append(str)
        # 使用URL规律以及获取到的电源ID构造URL池
        for start in ["0", "20", "40"]:
            url2 = "https://movie.douban.com/subject/"+movieid+"/comments?start="+start+"&limit=20&sort=new_score&status=P"
            html = spider(url2)
            # time.sleep(1)
            soup = BeautifulSoup(html, 'lxml')
            # 筛选评论DIV
            div = soup.find_all('div', {"class": "comment-item"})
            for item in div:
                # 筛选评论内容的span
                comment = item.find_all('span', {"class": "short"})[0]
                # 筛选点赞数标签
                zan = item.find_all('span', {"class": "votes"})[0]
                # 筛选用户信息
                infos = item.find_all('span', {"class": "comment-info"})
                for info in infos:
                    flag = info.find_all('span')
                    userid = info.find_all('a')[0]
                    time = info.find_all('span', {"class": "comment-time"})[0]
                    # 使用comment-time中的span数判断用户是否对电影评级
                    if len(flag) == 3:
                        stars = info.find_all('span')[1].get("class")[0]
                        star = re.findall(r'\d+', stars)
                    else:
                        star = ["无评级"]
                userid1 = userid.text
                time1 = time.text.strip()
                # 调用数据库操作函数
                insert_data(moviename, userid1, time1, star[0], zan.text, comment.text)
                # 打印结果
                print(moviename+userid.text + "-" + time.text.strip() + "-" + comment.text + "-" + star[0] + "-" + zan.text)
    time.sleep(1)
db.close()
