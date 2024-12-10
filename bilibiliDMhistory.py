import re
import time
from urllib.parse import urlparse
from urllib.parse import urlparse, parse_qs
import requests
import google.protobuf.text_format as text_format
import dm_pb2 as Danmaku
import datetime
import oid

bv = oid.getBv()

headers = oid.getHeaders()

# 从URL中提取oid
oid = oid.getOid(bv)
type = 1
print("OID:", oid)
print("type:", type)


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

# 查询稿件发布时间
video_url = 'https://api.bilibili.com/x/web-interface/wbi/view'

resp1 = requests.get(video_url,params={"bvid": bv},headers=headers)
data = resp1.json()['data']

# 当前时间戳
current_timestamp = int(time.time())
months_between = get_months_between(data['pubdate'], current_timestamp)
print(months_between)

cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv
resp2 = requests.get(cid_url,headers=headers)
print(resp2.json()['data'][0]['cid'])
cid = resp2.json()['data'][0]['cid']


for months in months_between:
    params = {
        "type": 1,
        "oid": cid,
        "month": months
    }
    history_date_url = 'https://api.bilibili.com/x/v2/dm/history/index'
    resp = requests.get(history_date_url, params, headers=headers)
    data = resp.content
    print(f"请求状态码: {resp.status_code}")
    print(f"响应内容: {resp.text}")


# 存在历史弹幕的日期

# params = {
#     "type": 1,
#     "oid": 113593563548072,
#     "month": "2020-01"
# }




# history_date_url = 'https://api.bilibili.com/x/v2/dm/history/index'
#
# params = {
#     "type": type,
#     "oid": oid,
#     "month": "2024-12"
# }
#
# resp = requests.get(history_date_url, params,headers=headers)
# data = resp.content
# print(f"请求状态码: {resp.status_code}")
# print(f"响应内容: {resp.text}")
