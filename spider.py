"""
    猫眼TOP100榜单排名
    2019-10-09
    邱深知
"""

from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import re

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.content.decode()
        return None
    except RequestException:
        return None

def parse_one_page(html):
   soup = BeautifulSoup(html,'lxml')
   title = re.compile('title="(.*?)"')
   imgst = re.compile('data-src="(.*?)"')
   shangyin = re.compile('<p class="releasetime">(.*?)</p>')
   zhuyans = re.compile('<p class="star">\S*\s*(.*?)\s*\S*</p>')
   pingfen1 = re.compile('<p class="score"><i class="integer">(.*?)</i>')
   pingfen2 = re.compile('</i><i class="fraction">(.*?)</i></p>')


   #标题
   page = soup.select('div > div > div.movie-item-info > p.name > a')
   ps = re.findall(title,str(page))
   # 图片
   imgs = soup.select('a > img.board-img')
   imgss = re.findall(imgst, str(imgs))
   #主演
   zhuyan = soup.select('div > div > div.movie-item-info > p.star')
   zhuyanss = re.findall(zhuyans,str(zhuyan))
   #上映时间
   shangying = soup.select('div > div > div.movie-item-info > p.releasetime')
   shanyings = re.findall(shangyin,str(shangying))
   #评分
   pingfens = soup.select('div > div > div.movie-item-number.score-num > p')
   pinfen1 = re.findall(pingfen1,str(pingfens))
   pinfen2 = re.findall(pingfen2,str(pingfens))


   for title,imgss,zhuya,shanyin,pinfen1,pinfen2 in zip(ps,imgss,zhuyanss,shanyings,pinfen1,pinfen2):
       # print("标题："+title)
       # print("图片："+imgss)
       # print(zhuya)
       # print(shanyin)
       # print("评分："+pinfen1+pinfen2)
       text = "标题："+title+"\n"+"图片："+imgss+"\n"+zhuya+"\n"+shanyin+"\n"+"评分："+pinfen1+pinfen2+"\n"
       with open('TOP100排名.txt', 'a', encoding='utf-8')as f:
           f.write(text)
           f.close()


def main():
    pages = 0
    # try:
    while True:
        if pages >=101 :
            print("已经爬取10页！")
            break
        else:
            url = "https://maoyan.com/board/4?offset={}".format(pages)
            html = get_one_page(url)
            parse_one_page(html)
            pages += 10
            print(url)
    # except:
    #     print("爬取%d"%pages+"成功！")

if __name__ == '__main__':
    main()


