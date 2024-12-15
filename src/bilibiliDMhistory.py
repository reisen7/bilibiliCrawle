'''
Author: reisen
Date: 2024-12-08 15:51:33
LastEditTime: 2024-12-15 16:14:23
'''
import csv
import json
import time
import requests
import datetime
import configs.config as config
import google.protobuf.text_format as text_format
from proto import dm_pb2 as Danmaku
from configs.config import BilibiliHelper


bv = BilibiliHelper.get_bv()

headers = BilibiliHelper.get_headers()

# 从URL中提取oid
oid = config.BilibiliHelper.get_oid()
type = 1
print("OID:", oid)
print("type:", type)





# 查询稿件发布时间
video_url = 'https://api.bilibili.com/x/web-interface/wbi/view'

resp1 = requests.get(video_url, params={"bvid": bv}, headers=headers)
data = resp1.json()['data']

# 当前时间戳
current_timestamp = int(time.time())
months_between = config.get_months_between(data['pubdate'], current_timestamp)
print(months_between)

cid = config.BilibiliHelper.get_cid()

monthDays = []

for months in months_between:
    params = {
        "type": 1,
        "oid": cid,
        "month": months
    }
    history_date_url = 'https://api.bilibili.com/x/v2/dm/history/index'
    resp = requests.get(history_date_url, params, headers=headers)
    print(resp.text)
    data = json.loads(resp.text)
    monthDays += data['data']

# print(monthDays)

dms = []

csv_header = ['id', '弹幕发送时间（ms）', '弹幕类型', '弹幕字号', '弹幕颜色', '发送者mid', '弹幕内容', '发送时间',
              '弹幕 dmid', '弹幕属性位']
file_path_1 = ('doc/dm/历史弹幕_' + bv + '.csv')

config.create_file_if_not_exists(file_path_1)

for monthDay in monthDays:
    history_dm_url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so'
    params = {
        'type': 1  # 弹幕类型
        , 'oid': cid  # cid
        , 'date': monthDay  # 弹幕日期
        , 'segment_index': 2
    }
    resp = requests.get(history_dm_url, params, headers=BilibiliHelper.get_headers())
    data = resp.content

    danmaku_seg = Danmaku.DmSegMobileReply() # type: ignore
    danmaku_seg.ParseFromString(data)
    # print(text_format.MessageToString(danmaku_seg.elems[0], as_utf8=True))
    print(len(danmaku_seg.elems))
    for elems in danmaku_seg.elems:
        dm = text_format.MessageToString(elems, as_utf8=True).replace("\"", "").split("\n")

        json_obj = {}
        for dm_value in dm:
            name = dm_value.split(":")[0] if len(dm_value.split(":")) > 1 else ""
            value = dm_value.split(":")[1].strip() if len(dm_value.split(":")) > 1 else ""
            json_obj[name] = value
            # print(json_obj)

        dt_object = datetime.datetime.fromtimestamp(int(json_obj['ctime']), datetime.timezone.utc)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        id = json_obj['id']
        progress = json_obj.get('progress', None)
        mode = json_obj['mode']
        fontsize = json_obj['fontsize']
        color = json_obj['color']
        midHash = json_obj['midHash']
        content = json_obj['content']
        ctime = formatted_time
        idStr = json_obj['idStr']
        attr = json_obj['attr']
        print(json_obj)
        dms.append(
            [id,progress,mode,fontsize,color,midHash,content,ctime,idStr,attr]
        )
        # print(int(dma_lie[7]))
        # print(dma_lie)
        # dt_object = datetime.datetime.fromtimestamp(int(dma_lie[7]), datetime.timezone.utc)
        # formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        # dma_lie[7] = formatted_time
        # dms.append(dma_lie)
        # print(dma_lie)



with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    writer.writerows(dms)


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
