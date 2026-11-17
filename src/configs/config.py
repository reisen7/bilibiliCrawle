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
    _cookie = ""
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
