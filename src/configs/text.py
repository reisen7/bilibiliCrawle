"""
Author: Reisen7
Date: 2024-12-18 02:28:54
LastEditTime: 2024-12-19 21:26:10
"""

import requests
from fake_useragent import UserAgent
import requests
import google.protobuf.text_format as text_format
from proto import dm_pb2 as Danmaku
from configs.config import BilibiliHelper

headers = {
    "Cookie": BilibiliHelper.get_cookie(),
    "User-Agent": UserAgent().random,
}


url = "https://api.bilibili.com/x/v2/dm/web/history/seg.so"
params = {
    "type": 1,  # 弹幕类型
    "oid": 144541892,  # cid
    "date": "2024-12-11",  # 弹幕日期
}
resp = requests.get(url, params, headers=headers)
data = resp.content
danmaku_seg = Danmaku.DmSegMobileReply()
danmaku_seg.ParseFromString(data)
print(len(danmaku_seg.elems))
print(
    text_format.MessageToString(
        danmaku_seg.elems[len(danmaku_seg.elems) - 1], as_utf8=True
    )
)
