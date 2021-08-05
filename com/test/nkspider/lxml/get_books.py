# 导包
import requests
from bs4 import BeautifulSoup
import lxml
import csv
import random
import os

# 0. 设置请求头,给出 user-agent, 模拟浏览器
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def get_headers():
    request_headers = {
        'User-Agent': random.choice(user_agents)
    }
    return


def get_href(tag):
    return tag.get('href')


def get_src(tag):
    return tag.get('src')


def get_title(tag):
    return tag.get('title')


def get_text(tag):
    return tag.text


def get_alt(tag):
    return tag.get('alt')


path = 'books'
path = path.strip()
isExists = os.path.exists(path)
if not isExists:
    os.makedirs(path)
else:
    print(path)

os.chdir(path)

illgle = ['\\', '|', '>', '<', '/', '?', '*', ':', '"']

start_s = ""
start = start_s.split(" ")

for s_s in start:
    s_path = s_s
    s_path = s_path.strip()
    Exists = os.path.exists(s_path)

    if not Exists:
        os.makedirs(s_path)
    else:
        print(s_path)

    os.chdir(s_path)
    for i in range(1, 104):
        # 1. 指定 url
        url_str = "https://www.f0ed3acd7d4d.com/xiaoshuo/list-{}-{}.html".format(s_s, str(i))
        print(url_str)
        resp = requests.get(url=url_str, headers=get_headers())
        stauts_code = resp.status_code
        if stauts_code == 200:
            html_text = resp.text

        # 4. 解析 html_text, 放入 bs 对象中 (生成|获取 soup 文档)
        soup = BeautifulSoup(html_text, 'lxml')  # 使用 lxml-html 解析器, 需要提前安装 lxml

        books = (soup.select(" div > ul > li> a"))
        print(books)
        books = books[56:]
        print(books)

        for book in books:
            book_name = (get_title(book) + ".txt")
            for ill in illgle:
                book_name = book_name.replace(ill, '')
            if os.path.exists(book_name):
                print(book_name)
                continue

            book_url = "https://www.f0ed3acd7d4d.com" + get_href(book)
            print(book_url)
            r = requests.get(url=book_url, headers=get_headers())
            if r.status_code == 200:
                h_t = r.text

            s = BeautifulSoup(h_t, "lxml")
            c = s.select("div.content > p")
            l = []
            for t in c:
                l.append(get_text(t))
            l.insert(0, book_url)
            print(l)



            with open(book_name, "w", newline="\n", encoding="utf-8") as f:
                f.write("\n".join(l))
                f.close()
    os.chdir("../")
