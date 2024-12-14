import requests
from src.configs import config
import xml.etree.ElementTree as ET

# 定义请求的URL
url = "https://api.bilibili.com/x/v1/dm/list.so"

url = "https://api.bilibili.com/x/v2/dm/wbi/web/seg.so"


oid = config.getOid()

cookie = config.getCookie()

print(oid)

params = {
    "oid": oid,
    "type": "1"
}
headers = {
    'Cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

try:
    # 发送GET请求，带上参数
    response = requests.get(url, params=params, headers=headers)
    # 如果请求成功（状态码为200）
    print(response)
    if response.status_code == 200:
        # 将响应内容以二进制形式写入到danmaku.xml文件中
        with open("danmaku.xml", "wb") as file:
            file.write(response.content)
        print("成功获取并保存弹幕数据到danmaku.xml文件")
    else:
        print(f"请求失败，状态码: {response.status_code}")
except requests.RequestException as e:
    print(f"请求出现异常: {e}")

# 从xml里面获取弹幕信息
with open('danmaku.xml', 'r', encoding='utf-8') as file:
    xml_data = file.read()

# 解析XML数据
root = ET.fromstring(xml_data)

# 初始化一个空列表用于存储结果
data_list = []

# 遍历所有<d>元素并提取p属性的值
for d in root.findall('d'):
    p_value = d.get('p')
    text_value = d.text
    # 将p属性的值和文本内容作为元组添加到列表中
    data_list.append((p_value, text_value))

# 转换为字典，以p的值为键，文本内容为值
data_dict = {item[0]: item[1] for item in data_list}

# 打印字典以验证结果
for key, value in data_dict.items():
    print(f'"{key}" : "{value}"')
