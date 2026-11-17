import requests
from proto import dm_pb2 as Danmaku
from configs import config

url = 'https://api.bilibili.com/x/v2/dm/web/seg.so'
oid = config.BilibiliHelper.get_oid
params = {
    'type': 1,         # 弹幕类型
    'oid': oid,    # cid
    'segment_index': 1 # 弹幕分段
}
headers = {
    'Cookie': '',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
resp = requests.get(url, params,headers=headers)
data = resp.content

danmaku_seg = Danmaku.DmSegMobileReply() # type: ignore
print(danmaku_seg)

danmaku_seg.ParseFromString(data)

print(danmaku_seg)
# print(text_format.MessageToString(danmaku_seg.elems[0], as_utf8=True))