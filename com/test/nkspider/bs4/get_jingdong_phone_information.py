import requests
from bs4 import BeautifulSoup
from lxml import etree

import random
import time
import re

import os
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}


def get_information(web_url):
    web_data = requests.get(url, headers=headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        soup_document = BeautifulSoup(html_text, 'html.parser')
        phone_homepage_elements = soup_document.select("div.p-img > a")
        price_elements = soup_document.select("div.p-price > strong > i")
        for phone_homepage_element, price in zip(phone_homepage_elements, price_elements):
            phone_homepage_href = 'https:' + (phone_homepage_element.get("href").strip())
            price = price.get_text()
            get_phone_info(phone_homepage_href, price)


def get_phone_info(phone_homepage_url, price):
    web_data = requests.get(phone_homepage_url, headers=headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        # 使用 lxml 解析 html_text
        selector = etree.HTML(html_text)
        # 使用 lxml 内置的 XPath 进行定位&提取
        phone_name = selector.xpath('//*[@id="detail"]/div/div/div/ul/li[1]/text()')[3]
        phone_name = ''.join(list(phone_name))
        brand_name = selector.xpath('//*[@id="parameter-brand"]/li/a/text()')[0]
        print(phone_name, brand_name, price)


if __name__ == '__main__':
    # url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8"
    url = "https://search.jd.com/Search?keyword=%E6%B8%B8%E6%88%8F%E6%9C%AC&enc=utf-8&wq=%E6%B8%B8%E6%88%8F%E6%9C%AC&pvid=f474078f03dc4292ae8ca80674eecf8a"
    get_information(url)

