# 导包
import requests
from bs4 import BeautifulSoup
import lxml

# 0. 设置请求头,给出 user-agent, 模拟浏览器
request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
    'Referer': 'https://movie.douban.com',
    'Connection': 'keep-alive'
}

# 1. 指定 url
url_str = "https://movie.douban.com/review/best/?start=0"

# 2. 发送请求,获取响应
resp = requests.get(url=url_str, headers=request_headers)

# 3. 获取页面源代码
stauts_code = resp.status_code
if stauts_code == 200:
    html_text = resp.text

# 4. 解析 html_text, 放入 bs 对象中 (生成|获取 soup 文档)
# soup = BeautifulSoup(html_text, 'html.parser')  # 使用内置解析器
soup = BeautifulSoup(html_text, 'lxml')  # 使用 lxml-html 解析器, 需要提前安装 lxml

# 5. 定位 : 借助 css selector
# 5-1. 根据标签名和属性定位
# author_name_element = soup.find(name='a', href="https://www.douban.com/people/184234641/")
# author_name_element = soup.find(name='a', class_='name')
# author_info_elements = soup.find_all(name='header', class_='main_hd')
# 5-2. 根据 css 类选择器 定位
# author_info_element=soup.select_one('a.name')
# author_info_element=soup.select_one('header.main_hd')
# 所有作者
author_info_elements = soup.select('a.name')
# 所有电影
movie_info_elements = soup.select('a.subject-img')

# 6. 提取: 作者名字\作者主页\电影图片地址\电影名称
# 遍历 - python
# for author_info_element in author_info_elements:
#     # 提取标签元素的文本
#     author_name = author_info_element.get_text().strip()    # 截断前后的多余空格
#     # 提取标签属性的值
#     author_homepage = author_info_element.get('href')       # 获取指定属性名的属性值
#     print(author_name, author_homepage)

if __name__=="__main__":

    # 遍历并一次性提取: 作者名字\作者主页, 电影的名字\电影主页\电影封面图片的源地址|文件
    for author_info_element, movie_info_element in zip(author_info_elements, movie_info_elements):
        # 定位电影图片标签元素
        movie_info_img_element = movie_info_element.find(name='img')
        # 依次提取
        author_name = author_info_element.get_text().strip()
        author_homepage = author_info_element.get('href')
        movie_name = movie_info_img_element.get("title")
        movie_homepage = movie_info_element.get('href')
        movie_cover_img = movie_info_img_element.get("src")
        # 生成字典对象,整体提取的信息
        movie_review_info = {
            'author_name': author_name,
            'author_homepage': author_homepage,
            'movie_name': movie_name,
            'movie_homepage': movie_homepage,
            'movie_cover_img': movie_cover_img
        }
        print(movie_review_info)