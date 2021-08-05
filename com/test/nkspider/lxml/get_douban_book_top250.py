# 导包
import requests
from bs4 import BeautifulSoup
from lxml import etree

import random
import time
import re

import os
import csv

# 模拟多个 user-agent
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

# 随机获取 user-agent, 实现 反 反爬 操作
request_headers = {
    'User-Agent': random.choice(user_agents)
}


# 获取当前 url 页面中每一本图书的主页 url === bs4
def get_per_page_25_book_links(url):
    web_data = requests.get(url, headers=request_headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        soup_document = BeautifulSoup(html_text, 'html.parser')
        book_homepage_elements = soup_document.select("div.pl2 > a")
        # 遍历获取每一本图书的主页url
        for book_homepage_element in book_homepage_elements:
            # 获取 href 属性值 == 图书主页 url
            book_homepage_href = book_homepage_element.get("href").strip()
            time.sleep(1)
            # 爬取每一本图书主页中的所需的信息
            get_book_info(book_homepage_href)


# 在图书主页(详情页)中完成基于 XPath 解析\定位\提取
def get_book_info(book_homepage_url):
    web_data = requests.get(book_homepage_url, headers=request_headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        # 使用 lxml 解析 html_text
        selector = etree.HTML(html_text)
        # 使用 lxml 内置的 XPath 进行定位&提取
        author_name = selector.xpath('//*[@id="info"]//a/text()')[0]
        # 使用正则表达式完成作者名字的提取, 去除额外的空格|换行
        # 1- 声明空白符 匹配
        p = re.compile('\s+')
        # 2- 删除所有的空白符, 替换空白符为空字符
        author_name = re.sub(p, '', author_name)
        publisher_name = selector.xpath('//span[contains(text(), "出版社")]')[0].tail
        publisher_date = selector.xpath('//span[contains(text(), "出版年")]')[0].tail
        book_price_element = selector.xpath('//span[text()="定价:"]')
        # 判断是否有 定价 标签
        book_price = book_price_element[0].tail if book_price_element != [] else 0.0
        book_rate = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0].strip()
        person_count = selector.xpath(' //*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()')[0].strip()
        book_isbn = selector.xpath('//span[contains(text(), "ISBN") or contains(text(), "统一书号")]')[0].tail
        print(author_name, publisher_name, publisher_date, book_price, book_rate, person_count, book_isbn)


# 设置程序入口, 声明主方法
if __name__ == '__main__':
    # 声明|创建 top250 所有的页面
    urls = ['https://book.douban.com/top250?start={}'.format(str(no)) for no in range(0, 250, 25)]
    # 遍历 top250 每一页(包含25本书概要信息<均包含25本书的每一本书详情页url>)
    for url in urls:
        # 解析定位提取该 url(概要信息页面) 中 25 本书的图书主页url
        get_per_page_25_book_links(url)
    print("End....")