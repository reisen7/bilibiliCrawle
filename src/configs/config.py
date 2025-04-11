"""
Author: reisen7 (reisen7@foxmail.com)
-----
Date: Friday, 11th April 2025 6:00:52 pm
-------------------------------------

-------------------------------------
HISTORY:
Date      	By  	Comments
----------	------	------------------
"""

import os
import re
import time
import requests
from datetime import datetime
from fake_useragent import UserAgent


class BilibiliHelper:
    # 类属性，相当于静态变量
    _cookie = "buvid3=832DE693-6441-9543-41D5-5C547CE4658A76524infoc; b_nut=1735380076; _uuid=B9D103A310-6E101-CD10D-710DF-11C515393321076733infoc; buvid4=AAE105CB-5004-71D6-FF14-F5D5B3CEFF9078077-024122810-YVZn5QqHbRxEGySS90mT5v6Tjq3eg4V3wnWUwF%2FVVrHYq3XkAbxELigtG9KHcPZl; rpdid=0zbfVGNbwB|EEC5QZYy|4jA|3w1TrtDh; SESSDATA=04d9afb8%2C1750932136%2C611c5%2Ac1CjAurrPGcB8uPrgVdty5IxphrLLL7Ae5c0bJ5eozwrXDbyLx4nsSQWKrAuFZtP4ehjoSVmZQNm92TWhpdDlpQmJiUnRuY1Z3MHNMVkpWcHBVLTh2TlJmN1ZwRWFJTXI0SGtaOXl6djRrUlp5Tmx2U0w2eUtjR0J5bjVBcl8yb0lTOG01VlIzb01RIIEC; bili_jct=993587aff370170f983cca88069b7939; DedeUserID=14211643; DedeUserID__ckMd5=896bac34e98270e4; header_theme_version=CLOSE; enable_web_push=DISABLE; hit-dyn-v2=1; dy_spec_agreed=1; buvid_fp_plain=undefined; LIVE_BUVID=AUTO7517365933379533; PVID=1; blackside_state=0; CURRENT_BLACKGAP=0; CURRENT_QUALITY=80; enable_feed_channel=ENABLE; home_feed_column=4; bp_t_offset_14211643=1052083420617768960; browser_resolution=1009-715; fingerprint=250a979f707317e90d29b641fcd5a41d; buvid_fp=1b2028bbe56ceee11069e19d9286b576; __at_once=12805230630066019579; __at_sign=e5f6f2706257a7d2aa6284c7b8f40f07; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDQ2MjEwMzIsImlhdCI6MTc0NDM2MTc3MiwicGx0IjotMX0.Iy2llKcQM1e1SOnGi2RlNeBaxex8zMEEmH_E27cr_ro; bili_ticket_expires=1744620972; b_lsid=722210AC4_1962411434D; CURRENT_FNVAL=4048; sid=8scsf889"
    _bv = "BV1MJ4m1u7RH"

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
        # print(resp.text)
        obj = re.compile(r'<div id="(?P<id>\d+)" bvid="{}"'.format(BilibiliHelper._bv))
        obj1 = re.compile(r'"aid":(?P<id>\d+),"bvid":"{}"'.format(BilibiliHelper._bv))
        # print(cls.get_headers())
        match = obj.search(resp.text)
        if not match:
            match = obj1.search(resp.text)
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
    print(helper.get_oid())
