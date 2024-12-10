import requests
from utils import oid
import xml.etree.ElementTree as ET

# 定义请求的URL
url = "https://api.bilibili.com/x/v1/dm/list.so"

oid = oid.getOid()
print(oid)
params = {
    "oid": oid
}
headers = {
    'Cookie': 'buvid4=023081809-k0zyHiuRDURA%2F%2Bu6uUGBn9ZJh%2BUZroYQRlqvXttbKIFoVgjlvvDstw%3D%3D; buvid_fp_plain=undefined; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=14211643; DedeUserID__ckMd5=896bac34e98270e4; LIVE_BUVID=AUTO7217028158647895; FEED_LIVE_VERSION=V8; buvid3=EBCD19BB-5F43-FA27-9E08-E7841D11831F72726infoc; b_nut=1723861672; _uuid=1B2A10745-10D82-3D25-B7E8-710B373AF513573813infoc; rpdid=0zbfvZWQjU|16Z4lxZ7a|2E|3w1SVjVJ; fingerprint=21dae7af1181bd34188ec789e2d7d75c; CURRENT_QUALITY=0; buvid_fp=21dae7af1181bd34188ec789e2d7d75c; PVID=3; home_feed_column=5; hit-dyn-v2=1; dy_spec_agreed=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM4ODU5MTQsImlhdCI6MTczMzYyNjY1NCwicGx0IjotMX0.-TpHS1oQ29EYzWSf_slAT-jsYaBoZB3M_637TFrFLcI; bili_ticket_expires=1733885854; SESSDATA=1034f759%2C1749178715%2Ca2aad%2Ac1CjB-1L_IiUZkYXemBlhQoVB5lrjEGQv0N_RgiZ_DLplQ4Lt9XzBhzFWep3Rk6gCqGQwSVlV0YVFPbXgzUXNhT1dldWhGRVpPMU5jaDhzTVdDQ1QyLU56NDNIcnNnUVFOQ3VTQm1Xc1I3QlZwa2hlSzBIRTJtMC1SLXZRa3JlbmxDSV9oYXJvSTRRIIEC; bili_jct=b49d9fcd88fc86b822f7c9d4125530a3; sid=4k53eg99; bp_t_offset_14211643=1008410247531855872; b_lsid=FF812264_193A475A5F8; bsource=search_bing; browser_resolution=1912-954; CURRENT_FNVAL=4048',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

try:
    # 发送GET请求，带上参数
    response = requests.get(url, params=params, headers=headers)
    # 如果请求成功（状态码为200）
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
