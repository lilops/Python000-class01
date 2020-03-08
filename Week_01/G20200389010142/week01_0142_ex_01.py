# =======================作业============================
# 安装并使用 requests、bs4 库，爬取豆瓣电影 Top250 的电影名称、评分、短评数量 和前 5 条热门短评
# 并以 UTF-8 字符集保存到 csv 格式的文件中。
#=========================================================

import requests
from bs4 import BeautifulSoup as bs
import re, csv

def writeCsv(file, line,write_type):
    out = open(file, write_type, encoding = 'utf-8')
    csv_write = csv.writer(out, dialect = 'excel')
    csv_write.writerow(line)

def get_url_name(myurl):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    header = {}  # 定义一个字典
    header['user-agent'] = user_agent

    response = requests.get(myurl,headers=header)
    bs_info = bs(response.text, 'html.parser')
    ### 第一次竟然输成 response.txt 搞了半天才发现问题

    # 找到放置单个电影信息的地方
    for tags in bs_info.find_all('div', attrs={'class': 'info'}):
            # 获取电影链接
            movie_url = tags.find('a',).get('href')  #  print(movie_url)

            # 获取电影名称
            movie_name = tags.find('a',).find('span', attrs={'class': 'title'}).text

            # 获取电影得分        
            movie_score = tags.find('span', attrs={'class':'rating_num','property':'v:average'}).text   # 不加.text的话 输出的是这一行全部内容<span class="rating_num" property="v:average">9.7</span> 
            
            # 获取有多少人进行了评分  
            # 找到 star 类下第四个标签,取出里面的数字部分,此时num类型的列表，且数字类型为字符串
            # re.findall('\d+',a)取出a中数字部分  map(int,a) 把a中的字符型数字转成整形
            # list(map)是把map转换成列表    list[0] 取出列表元素，因为就一个所以用0就可以
            movie_score_num = list(map(int, re.findall('\d+',
                                   tags.find('div', attrs={'class': 'star'}).
                                   find_all('span')[3].text))
                                   )[0]
            
            # 进入单个电影链接重新分析新的页面
            response_movie_url = requests.get(movie_url, headers=header)
            bs_info_movie_url = bs(response_movie_url.text, 'html.parser')
           
            # 取出热评数量
            commeents_num = list(map(int, re.findall('\d+', # 匹配标签里面内容的数字部分
                                 bs_info_movie_url.find('div', attrs={'class': 'mod-hd'}).  #找到热评数量的父模块
                                 find('span', attrs={'class':'pl'}).text))   #取出标签里面的内容 (全部 344472 条)
                                 )[0]

            # 找到热门短评的标签，注意此时需要用find
            hot_commeents = bs_info_movie_url.find('div', attrs={'id':'hot-comments','class':'tab'})

            # 获取热评5个，新建一个列表
            movie_commeents = []
            # print(type(movie_commeents))
            for hot_commeents_item in hot_commeents.find_all('span', attrs={'class':'short'}):
                movie_commeents.append(hot_commeents_item.text)

            movie_info = [movie_name,movie_score,commeents_num, movie_commeents[0],movie_commeents[1],movie_commeents[2],movie_commeents[3],movie_commeents[4]]
            writeCsv(csv_file, movie_info,'a')
            

csv_file= '豆瓣电影.csv'
csv_header = ['电影名称','电影得分','短评数量','热评1', '热评2', '热评3', '热评4', '热评5']
writeCsv(csv_file, csv_header, 'w')

# urls = tuple(f'https://movie.douban.com/top250?start={page * 25}&filter=' for page in range(2))
urls = tuple(f'https://movie.douban.com/top250?start={page * 25}&filter=' for page in range(10))
# urls = tuple(f'https://movie.douban.com/top250?start={page * 25}&filter=' for page in range(10))
# # f-string是格式化字符串的新语法。f-string用大括号 {} 表示被替换字段，其中直接填入替换内容


from time import sleep
if __name__ == '__main__':
    for page in urls:
        get_url_name(page)
        print(page)
        sleep(5)


#  File "c:/Users/seabrezer/OneDrive/Python/Code/GeekbangPython+/course_0229/MyWork2.py", line 63, in get_url_name
#     movie_info = [movie_name,movie_score,commeents_num, movie_commeents[0],movie_commeents[1],movie_commeents[2],movie_commeents[3],movie_commeents[4]]
# IndexError: list index out of range