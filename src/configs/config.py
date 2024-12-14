import datetime
import os

import requests
import re
from fake_useragent import UserAgent

ua = UserAgent()  # 创立随机请求头

av = ''
bv = 'BV1jNmtYcEbY'

cookie = "buvid3=EF7B0AC3-332C-FF18-55C9-89606E9189CD71380infoc; b_nut=1713965271; _uuid=AFD8E9AE-5CE4-1C98-C3E4-CA6926AA3A2F72077infoc; buvid4=22B70373-63D3-AF59-ACAB-F677312FCF5072187-024042413-Jp6mowiK7grcjxRq0m0a7w%3D%3D; rpdid=|(YYJ~~kk)|0J'u~ulluJ~um; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=329083930; DedeUserID__ckMd5=4908218e56e1c21a; fingerprint=e55873cc520dafcba59c9c190d6f2aa0; buvid_fp_plain=undefined; buvid_fp=e55873cc520dafcba59c9c190d6f2aa0; bp_video_offset_329083930=1008953127103102976; bp_t_offset_329083930=1009368175562719232; b_lsid=A25457DF_193B5C4F69F; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQxODA2MDUsImlhdCI6MTczMzkyMTM0NSwicGx0IjotMX0.WQjzuuokem-zL9t0N76x648Eh4AafqdX6TuX8_JTd_o; bili_ticket_expires=1734180545; SESSDATA=47c41f0e%2C1749473405%2C4192a%2Ac1CjBNcFwXKZQ-7bcaIFJQUgEceY_i9N3AQRCbdApRahurkQB3l1dC064fHbECVJT9RfkSVmJqWjlGcndCUmVTeS1EQ01NN1lRVlZuaG1kV3pEdXBNcUlIOHhfWU5qODFlQy1UTGlLblppeXVxUU1JT3VVbUpwdTNURUlmS3E0eHpESWVUWExnMklnIIEC; bili_jct=1fa19b284ae7e005fefee16945ee5f16; sid=52swl5k9; CURRENT_FNVAL=2000; home_feed_column=4; browser_resolution=1180-658"

headers = {

    'Cookie': cookie,
    'User-Agent': ua.random
    #随机请求头，b站爸爸别杀我，赛博佛祖保佑
}

def create_file_if_not_exists(file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.truncate(0)  # 使用truncate方法将文件内容清空，使其变为空文件
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            pass  # 这里只是创建空文件，若需要写入初始内容可在这里添加对应代码

def getOid():
    resp = requests.get("https://www.bilibili.com/video/"+bv,headers=headers)
    obj = re.compile(f'"aid":(?P<id>.*?),"bvid":"{bv}"')  # 在网页源代码里可以找到id，用正则获取到
    oid = obj.search(resp.text).group('id')
    # print('oid是' + oid)  # 在程序运行时告诉我们已经获取到了参数oid
    return oid

def getCid():
    cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv
    resp2 = requests.get(cid_url, headers=headers)
    # print(resp2.json()['data'][0]['cid'])
    cid = resp2.json()['data'][0]['cid']
    return cid
def getHeaders():
    return headers


def getCookie():
    return cookie

def getBv():
    return bv


def get_months_between(start_timestamp, end_timestamp=None):
    # 如果未提供结束时间戳，则使用当前时间
    if end_timestamp is None:
        end_time = datetime.datetime.now()
    else:
        end_time = datetime.datetime.fromtimestamp(end_timestamp)

    start_time = datetime.datetime.fromtimestamp(start_timestamp)

    # 确保开始时间不大于结束时间
    if start_time > end_time:
        return []

    months = []
    current = start_time

    while current <= end_time:
        month_str = current.strftime('%Y-%m')
        if not months or months[-1] != month_str:  # 避免添加重复的月份
            months.append(month_str)
        # 增加到下一个月
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)

    # 如果开始和结束时间在同一月份，确保这个月份被包含
    if start_time.strftime('%Y-%m') == end_time.strftime('%Y-%m') and not months:
        months.append(start_time.strftime('%Y-%m'))

    return months


if __name__ == '__main__':
    print(getOid('BV176i2YfE9L'))
