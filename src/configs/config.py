import os
import re
import time
import requests
from datetime import datetime
from fake_useragent import UserAgent


class BilibiliHelper:
    # 类属性，相当于静态变量
    _cookie = "buvid4=4F41C8A4-A89C-5E80-B2AB-8C222E6A8C0160292-023081809-k0zyHiuRDURA%2F%2Bu6uUGBn9ZJh%2BUZroYQRlqvXttbKIFoVgjlvvDstw%3D%3D; buvid_fp_plain=undefined; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=14211643; DedeUserID__ckMd5=896bac34e98270e4; LIVE_BUVID=AUTO7217028158647895; FEED_LIVE_VERSION=V8; buvid3=EBCD19BB-5F43-FA27-9E08-E7841D11831F72726infoc; b_nut=1723861672; _uuid=1B2A10745-10D82-3D25-B7E8-710B373AF513573813infoc; rpdid=0zbfvZWQjU|16Z4lxZ7a|2E|3w1SVjVJ; CURRENT_QUALITY=0; hit-dyn-v2=1; dy_spec_agreed=1; PVID=1; home_feed_column=5; browser_resolution=1528-738; SESSDATA=7cf0a90d%2C1749738645%2C22e42%2Ac1CjCB9RJzkAh9y62VJOA5hlPUbd3i4NL0whgZhSfccV8a-XPH0eGK-wXHgh0XKNV-C-ISVmhhQTBjSmxFVzc5ay0tajNwRE5CblItNFExUVpnRmpkRXo5dnZPbUxaU2xBYmlEVkk2ZlY4M0xTd0k0dFQyb25qcy0wbnRwd09tWU5nRnhPODQ2Wmt3IIEC; bili_jct=8319bc03969a1f1bb0dace6ba2824845; fingerprint=ab608923ba12e0161c35f30096c6d1c1; buvid_fp=ab608923ba12e0161c35f30096c6d1c1; bp_t_offset_14211643=1011045506320695296; b_lsid=A24210B27_193D4C3D156; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ3MDA2MjQsImlhdCI6MTczNDQ0MTM2NCwicGx0IjotMX0.yXq7edwOq7Bewt2R2BAxu_8rUKDGZIOkx0uBMXxPpNE; bili_ticket_expires=1734700564; CURRENT_FNVAL=2000; sid=gjnii2pd"
    _bv = "BV13wzVYtEet"

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
        resp = requests.get(
            f"https://www.bilibili.com/video/{BilibiliHelper._bv}",
            headers=cls.get_headers(),
        )
        obj = re.compile(r'"aid":(?P<id>\d+),"bvid":"{}"'.format(BilibiliHelper._bv))
        print(cls.get_headers())
        match = obj.search(resp.text)
        if match:
            oid = match.group("id")
            return oid
        else:
            raise ValueError("Could not find OID")

    @classmethod
    def get_cid(cls) -> str:
        cid_url = (
            f"https://api.bilibili.com/x/player/pagelist?bvid={BilibiliHelper._bv}"
        )
        resp2 = requests.get(cid_url, headers=cls.get_headers())
        data = resp2.json().get("data", [])
        if data:
            cid = data[0].get("cid")
            return cid
        else:
            raise ValueError("Could not find CID")

    @classmethod
    def get_headers(cls):
        cookie_pairs = [
            pair.split("=")
            for pair in BilibiliHelper._cookie.split("; ")
            if "=" in pair
        ]
        cookies_dict = {name.strip(): value.strip() for name, value in cookie_pairs}
        bili_jct = cookies_dict.get("bili_jct", "")
        sessdata = cookies_dict.get("SESSDATA", "")

        headers = {
            "Cookie": BilibiliHelper._cookie,
            "User-Agent": UserAgent().random,
            "SESSDATA": sessdata,
            "csrf": bili_jct,
        }
        return headers


# 设置初始值（可以放在其他地方，比如配置文件加载后）


def create_file_if_not_exists(file_path):
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(file_path, "w", encoding="utf-8") as f:
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
        month_str = current.strftime("%Y-%m")
        if not months or months[-1] != month_str:  # 避免添加重复的月份
            months.append(month_str)
        # 增加到下一个月
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)

    # 如果开始和结束时间在同一月份，确保这个月份被包含
    if start_time.strftime("%Y-%m") == end_time.strftime("%Y-%m") and not months:
        months.append(start_time.strftime("%Y-%m"))

    return months


def datetime_to_timestamp_in_milliseconds(cls):
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    helper = BilibiliHelper()
    print(helper)
