# 导入包
import urllib.request

# 0. 指定浏览器 -- 设置 user-agent=>request_headers
request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
    'Referer': 'https://movie.douban.com',
    'Connection': 'keep-alive'
}

# 1. 指定 url
url = "https://www.baidu.com"

# 2. 封装请求对象, 设置请求参数
request = urllib.request.Request(url=url, headers=request_headers)

# 3. 发送请求,获得响应
response = urllib.request.urlopen(request)

# 4.获取并解析处理响应的相关信息
# 4-0. 获取响应的状态码
status_code = response.getcode()
# 4-1. 获取响应中的请求地址
request_address = response.geturl()
# 4-2. 获取响应信息, 本质是响应头
response_info = response.info()
# 获取 html 源代码
html_text = response.read().decode('utf-8')

# 打印
print(status_code)
print(request_address)
print(response_info)
print(html_text)

# ... 借助 bs4\lxml 对 html_text 进行解析\定位\提取