'''
Author: reisen
Date: 2024-12-15 14:27:47
LastEditTime: 2024-12-15 15:20:36
'''

import csv
import configs.config as config
from configs.config import BilibiliHelper
import requests

bv = BilibiliHelper.get_bv()

headers = BilibiliHelper.get_headers()

video_url = 'https://api.bilibili.com/x/web-interface/wbi/view'

csv_header = ['aid','bv号', '播放数', '弹幕数', '评论数', '收藏数', '投币数', '分享数', '当前排名','历史最高排行', '获赞数','点踩数','视频评分']
file_path_1 = ('doc/video/视频信息_' + bv + '.csv')
video_info = []
config.create_file_if_not_exists(file_path_1)

resp1 = requests.get(video_url, params={"bvid": bv}, headers=headers)
data = resp1.json()['data']
print(data['stat'])
video_data = data['stat']
video_info.append([video_data['aid'],bv,video_data['view'],video_data['danmaku'],video_data['reply'],video_data['favorite'],video_data['coin'],video_data['share'],video_data['now_rank'],video_data['his_rank'],video_data['like'],video_data['dislike'],video_data['evaluation']])

with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    writer.writerows(video_info)



