# 0. 导入内置 json
import json
# 0. 导入 requests
import requests

# 1-1. 直接赋值 json string
json_str = '{"name": "zhangsan", ' \
           '"age": 20, ' \
           '"like": ["sing", "dance", "swim"],  ' \
           '"scores": {"chinese": 80, "math": 60, "english": 99} }'
print("JSON Str : {0}".format(json_str))

# 1-2. 调用 json.loads 执行反序列化
json_str_data = json.loads(json_str)
print("JSON Data(var) : %s" % json_str_data)

# 1-3. 获取 json string 中的数据(value)值
print(json_str_data["name"], json_str_data["like"][2], json_str_data["scores"]["chinese"])
# 遍历 json_data
for key, value in json_str_data.items():
    print("key: ", key, " ==> value: ", value)
    if type(value) == list:
        print("\tAll ", key, " is ", end=": ")
        for item in value:
            print(item, end=", ")
        print()
    if type(value) == dict:
        print("\tAll ", key, " is: ")
        for k in value.keys():
            print("\t\t%s : %d" % (k, value[k]))

# 2-1 设置请求头参数
request_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71 "
}
# 2-2 设置 url
url_str = "https://club.jd.com/comment/productPageComments.action?productId=100011203359&score=0&sortType=5&page=1&pageSize=10"

# 2-3 发送请求,获取响应
resp = requests.get(url_str, headers=request_headers)
if resp.status_code != 200:
    print("response is fail.")
    pass

# 2-4 获取响应内容, 并解析为字符串
resp_json_str = resp.content.decode("gb18030")
print(resp_json_str)

# 2-5 反序列化操作
resp_json_data = json.loads(resp_json_str)

# 2-6 获取 json data 中的数据(value)值
sku_id = resp_json_data["productCommentSummary"]["skuId"]
print(sku_id)
comments = resp_json_data["comments"]
for comment in comments:
    content = comment["content"]
    print(content)
# 遍历 resp_json_data
for key, value in resp_json_data.items():
    print("key: ", key, " ==> value: ", value)
    if type(value) == list:
        print("\tAll ", key, " is ", end=": ")
        for item in value:
            print(item, end=", ")
        print()
    if type(value) == dict:
        print("\tAll ", key, " is: ")
        for k in value.keys():
            print("\t\t{0} : {1}".format(k, value[k]))

# 2-0. 声明变量
name = "hanmeimei"
age = 22
like = ("reading", "somking", "sleeping")
chinee_score = 10
math_score = 20
english_score = 30
scores = {"chinese": chinee_score, "math": math_score, "english": english_score}
student = {"name": name, "age": age, "like": like, "scores": scores}
# 2-1. 序列化为 string
student_json_str = json.dumps(student)
print(student_json_str)

# 2-2. 序列化为 file
with open('student.json', 'wt') as fp:
    json.dump(student, fp)

with open('student.json', 'rt') as fp:
    student_var = json.load(fp)
student_var["name"] = "lilei"
print(student_var)