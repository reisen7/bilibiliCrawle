import os
import re
import time
import requests
from datetime import datetime
from fake_useragent import UserAgent


class BilibiliHelper:
    # 类属性，相当于静态变量
    _cookie = "buvid3=EF7B0AC3-332C-FF18-55C9-89606E9189CD71380infoc; b_nut=1713965271; _uuid=AFD8E9AE-5CE4-1C98-C3E4-CA6926AA3A2F72077infoc; buvid4=22B70373-63D3-AF59-ACAB-F677312FCF5072187-024042413-Jp6mowiK7grcjxRq0m0a7w%3D%3D; rpdid=|(YYJ~~kk)|0J'u~ulluJ~um; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=329083930; DedeUserID__ckMd5=4908218e56e1c21a; buvid_fp_plain=undefined; bp_video_offset_329083930=1008953127103102976; bp_t_offset_329083930=1009368175562719232; home_feed_column=4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ0NTE5NzIsImlhdCI6MTczNDE5MjcxMiwicGx0IjotMX0.OtG6-2AKZ2_SDooyCfcaDB2wnC-S7Tl6fkqCUPU3igc; bili_ticket_expires=1734451912; SESSDATA=5fc3b4af%2C1749744775%2Cc6f6d%2Ac1CjAJTxffEWwk92RfECk13cyhfezMNXO1KQ94wTdT7mR0zxb5DgsW7bG7ykUoQrLNPAYSVk9aMV81eUoxQjRHTndaTVg2R0NpRF9uVTR2alZJS2oxdGhuZXRaclpBeWk5UTBFVlBaamJFWk9ORjhRZkxYc2FUTk9vbk9lVkNiT3RrSU9Tck41WWNnIIEC; bili_jct=8d502cc1d1390c1c156a318da89eb496; sid=89f9jd5o; CURRENT_FNVAL=2000; fingerprint=624438a134d3901426bdf1326fa87817; b_lsid=FFCE8B1010_193C91E47EF; bsource=search_bing; browser_resolution=1190-666; buvid_fp=624438a134d3901426bdf1326fa87817"
    _bv = "BV1jNmtYcEbY"

    @classmethod
    def get_cookie(cls) -> str:
        return cls._cookie

    @classmethod
    def set_cookie(cls, value):
        cls._cookie = value

    @classmethod
    def get_bv(cls) -> str:
        return cls._bv

    @classmethod
    def set_bv(cls, value):
        cls._bv = value

    def __init__(self):
        self.ua = UserAgent()

    @classmethod
    def get_oid(cls) -> str:
        resp = requests.get(f"https://www.bilibili.com/video/{BilibiliHelper._bv}", headers=cls.get_headers())
        obj = re.compile(r'"aid":(?P<id>\d+),"bvid":"{}"'.format(BilibiliHelper._bv))
        print(cls.get_headers())
        match = obj.search(resp.text)
        if match:
            oid = match.group('id')
            return oid
        else:
            raise ValueError("Could not find OID")
        
    @classmethod
    def get_cid(cls) -> str:
        cid_url = f'https://api.bilibili.com/x/player/pagelist?bvid={BilibiliHelper._bv}'
        resp2 = requests.get(cid_url, headers=cls.get_headers())
        data = resp2.json().get('data', [])
        if data:
            cid = data[0].get('cid')
            return cid
        else:
            raise ValueError("Could not find CID")
        
    @classmethod
    def get_headers(cls):
        cookie_pairs = [pair.split('=') for pair in BilibiliHelper._cookie.split('; ') if '=' in pair]
        cookies_dict = {name.strip(): value.strip() for name, value in cookie_pairs}
        bili_jct = cookies_dict.get('bili_jct', '')
        sessdata = cookies_dict.get('SESSDATA', '')

        headers = {
            'Cookie': BilibiliHelper._cookie,
            'User-Agent': UserAgent().random,
            'SESSDATA': sessdata,
            'csrf': bili_jct,
        }
        return headers


# 设置初始值（可以放在其他地方，比如配置文件加载后）


def create_file_if_not_exists(file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(file_path, 'w', encoding='utf-8') as f:
        if os.path.exists(file_path):
            f.truncate(0)  # 清空文件内容
        else:
            pass  # 创建空文件



def get_months_between(start_timestamp, end_timestamp=None):
    # 如果未提供结束时间戳，则使用当前时间
    if end_timestamp is None:
        end_time = datetime.now()
    else:
        end_time = datetime.fromtimestamp(end_timestamp)

    start_time = datetime.fromtimestamp(start_timestamp)

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


def datetime_to_timestamp_in_milliseconds(cls):
    return int(round(time.time() * 1000))



if __name__ == '__main__':
    helper = BilibiliHelper()
    print(helper)