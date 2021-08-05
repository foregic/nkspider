# 导包给程序添加 requests 支持
import requests

# 设置请求头,给出 user-agent, 模拟浏览器
request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67',
    'Referer': 'https://movie.douban.com',
    'Connection': 'keep-alive'
}

# 给出 url_str, 是一个 uri 的资源描述符
url_str = "https://www.baidu.com"

# 借助 requests 发送请求,获取响应
resp = requests.get(url=url_str, headers=request_headers)

# 处理响应
status_code = resp.status_code
if status_code == 200:
    print("Get Page success....")
    try:
        html_text = resp.text  # 获取页面的源代码
        print(html_text)
    except ConnectionError:
        print("Connect Error....")
else:
    print("error...")