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


def get_name(url):
    start_pos = url.index('c/p')
    return url[start_pos + 3:]


def get_article(url):
    re = requests.get(url=url, headers=get_headers())
    sc = resp.status_code
    if sc == 200:
        ht = re.text
    s = BeautifulSoup(ht, 'lxml')
    p_contents = s.select('div.review-content > p')
    result = ""
    for p in p_contents:
        result += get_text(p) + '\n'
    # print(result)

    return result


if __name__ == "__main__":
    l = []
    list = ['电影名字',
            '电影url',
            '电影图片',
            '作者名字',
            '作者头像',
            '文章标题',
            '文章url',
            '时间信息',
            '星级信息',
            '文章详情']

    for i in range(0, 0):
        # 1. 指定 url
        url_str = "https://movie.douban.com/review/best/?start={}".format(str(i * 10))

        # 2. 发送请求,获取响应
        resp = requests.get(url=url_str, headers=get_headers())

        # 3. 获取页面状态码
        stauts_code = resp.status_code
        if stauts_code == 200:
            html_text = resp.text

        # 4. 解析 html_text, 放入 bs 对象中 (生成|获取 soup 文档)
        soup = BeautifulSoup(html_text, 'lxml')  # 使用 lxml-html 解析器, 需要提前安装 lxml

        # 所有电影
        movie_info_elements = soup.select('a.subject-img')
        # 所有电影图片链接
        movie_icons = soup.select('a.subject-img>img')
        # 所有作者
        author_info_elements = soup.select('header > a.name')
        # print(author_info_elements)
        # 所有作者头像链接
        author_icons = soup.select('header > a.avator > img')
        # 所有文章链接
        article_urls = soup.select('div.main-bd > h2 > a')
        # 所有时间
        time_urls = soup.select(' header > span.main-meta')
        # 所有星级
        stars_urls = soup.select('header > span.main-title-rating')

        for information in zip(movie_info_elements, movie_icons, author_info_elements, author_icons, article_urls,
                               time_urls, stars_urls):
            info = {
                '电影名字': get_title(information[1]),
                '电影url': get_href(information[0]),
                '电影图片': get_src(information[1]),
                '作者名字': get_text(information[2]),
                '作者头像': get_src(information[3]),
                '文章标题': get_text(information[4]),
                '文章url': get_href(information[4]),
                '时间信息': get_text(information[5]),
                '星级信息': get_title(information[6]),
                '文章详情': get_article(get_href(information[4]))

            }
            l.append(info)
    # path = '电影图片'
    # path = path.strip()
    # isExists = os.path.exists(path)
    # if not isExists:
    #     os.makedirs(path)
    # else:
    #     print('目录已存在')

    # os.chdir('电影图片')
    # for info in l:
    #     img = requests.get(info['电影图片'], headers=get_headers())
    #
    #     f = open(get_name(info['电影图片']), 'ab')
    #     f.write(img.content)
    #     f.close()

    # with open("output.txt", 'w', newline='', encoding='utf-8') as f:
    #     # f.write("{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<10s}\n{:<20s}\n\n".format(
    #     #     list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9]))
    #     for info in l:
    #         f.write(
    #             "电影名字:{:<10s}\n"
    #             "电影url:{:<10s}\n"
    #             "电影图片:{:<10s}\n"
    #             "作者名字:{:<10s}\n"
    #             "作者头像:{:<10s}\n"
    #             "文章标题:{:<10s}\n"
    #             "文章url:{:<10s}\n"
    #             "时间信息:{:<10s}\n"
    #             "星级信息:{:<10s}\n"
    #             "文章详情:\n{:<20s}\n"
    #             "\n\n".format(
    #                 info['电影名字'], info['电影url'], info['电影图片'], info['作者名字'], info['作者头像'], info['文章标题'], info['文章url'],
    #                 info['时间信息'], info['星级信息'], info['文章详情']))
