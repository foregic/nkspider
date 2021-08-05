# 导入 urllib 支持
# import urllib
# from urllib.request import urlopen
# 指明导入 urllib 下 request 模块下的所有功能
import urllib.request
import os  # 获取路径|文件夹的信息

# 获取百度首页的图片并下载
# 0. 解析获取url(uri)
url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
# 1. 发送对 url(uri) 请求, 获取响应
resp = urllib.request.urlopen(url)
# 2. 获取响应内容
resp_content = resp.read()
# 3. 获取响应内容中的实际数据(img)
data = resp_content

# Python IO
file_name = "baidu.png"
# file_name = url.split("/")[-1]
# 获取当前程序文件所在的文件夹下的 data 目录
file_path = os.path.join(os.getcwd(), 'data')
# 完成文件读写
with open(file_path + os.sep + file_name, 'wb') as fp:
    fp.write(data)
    print("End...")