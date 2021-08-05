# 给项目添加 urllib3 能力: pip install urllib3
# 导入 : 给当前程序添加 urllib3 能力
import urllib3

# 0. 获取 url
url_str = "https://www.baidu.com/index.html"

# 1. 设置 user-agent
request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
}

# 2. 借助连接管理器池创建一个 http 连接, 并设置连接的超时时间
http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1.0, read=5.0))
# http = urllib3.PoolManager(timeout = 5.0)

# 3. 发送请求,获取响应
resp = http.request(method='GET', url=url_str, headers=request_headers)

# 4. 处理响应
status_code = resp.status
resp_headers = resp.headers
# resp_encode = resp.encode
html_text = resp.data.decode('utf-8')

print(html_text)