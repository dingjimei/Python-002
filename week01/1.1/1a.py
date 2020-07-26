# 使用requests库获取猫眼
import requests
import re
import json
from multiprocessing import Pool

def parse_one_page(html):         # 提取出，‘序列号’，‘电影标题’，‘上映时间’，‘评分’
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?'
                         +'<p.*?releasetime">(.*?)</p>.*?<i.*?integer">(.*?)</i>'
                         +'.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index':item[0],
            'title':item[1],
            'releasetime':item[2].strip()[5:], # str.strip()就是把这个字符串头和尾的空格，以及位于头尾的\n \t之类给删掉
            'score':item[3]+item[4]
        }

def write_to_file(content):       # 把提取出来的信息写到文件夹
    with open('result.csv','a',encoding='utf8')as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def get_one_page(url):           # 获取网页的 URL
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    header = {'user-agent':user_agent}
    url = 'https://maoyan.com/board/4?offset=0'
    response = requests.get(url,headers=header)
    return response.text

def main(offset):
    url = 'https://maoyan.com/board/4?offset=0' # 共提取10个网页内容
    html = get_one_page(url)     # 每个网页对应的信息代码
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(1)])
