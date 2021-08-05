# 导包
import requests
from bs4 import BeautifulSoup
import time

# 0. 设置请求头,给出 user-agent, 模拟浏览器
request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
    'Referer': 'https://movie.douban.com',
    'Connection': 'keep-alive'
}


# 实现具体某个页面(url)数据爬取
def get_info(page_url):
    # 发送请求获取响应
    resp = requests.get(url=page_url, headers=request_headers)
    html_text = resp.text
    # 1. 转换为 bs4 的 soup 文档
    soup_document = BeautifulSoup(html_text, 'lxml')
    # 2. 基于 soup 文档的定位&提取
    # 定位
    ranks = soup_document.select('span.pc_temp_num')  # 所有的序号
    titles = soup_document.select('div.pc_temp_songlist > ul > li > a')  # 所有的歌手&歌名
    times = soup_document.select('div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')  # 所有时长
    # 遍历 - 提取
    for rank, title, time in zip(ranks, titles, times):
        if "-" in title.get_text():
            data = {
                'rank': rank.get_text().strip(),
                'singer': title.get_text().split('-')[0].strip(),
                'song': title.get_text().split('-')[1].strip(),
                'time': time.get_text().strip()
            }
            print(data)


# 声明 main 方法
if __name__ == "__main__":
    # 生成所有的待爬取的 urls
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html'.format(str(i)) for i in range(1, 24)]
    # 遍历每一个 url, 完成数据爬取
    for url in urls:
        # 调用方法完成某个页面(url)爬取
        get_info(url)
        # time.sleep(1)  # 暂停1秒, 模拟人的手工操作, 建议使用随机数
    print("End...")