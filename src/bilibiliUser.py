"""
Author: reisen
Date: 2024-12-14 23:29:53
LastEditTime: 2024-12-16 19:58:56
"""

import gzip
import io
import os, sys
import csv
import datetime
import json
from multiprocessing.pool import ThreadPool
import random
import sys
import time
from exceptiongroup import catch
import requests
import configs.biliwbi as wbi
import configs.config as config
from fake_useragent import UserAgent
import os
import re
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook, load_workbook
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from configs.config import BilibiliHelper

ua = UserAgent()

img_key, sub_key = wbi.getWbiKeys()

signed_params = wbi.encWbi(
    params={"foo": "114", "bar": "514", "baz": 1919810},
    img_key=img_key,
    sub_key=sub_key,
)


# w_rid = signed_params['w_rid']
# wts = signed_params['wts']
# print(w_rid)
# print(wts)
# user_url = 'https://api.bilibili.com/x/space/wbi/acc/info'

# params = {
#    'mid': '2',
#    'wts': wts,
#    'w_rid': w_rid
# }

# cookie = config.getCookie()
# headers = {
#     'Cookie': cookie
# }


# try:
#     # 发送GET请求
#     response = requests.get(user_url, params=params, headers=headers)
#     # 如果响应状态码为200，则表示请求成功
#     if response.status_code == 200:
#         print(response.json())
#     else:
#         print(f"请求失败，状态码: {response.status_code}")
# except requests.RequestException as e:
#     print(f"请求出错: {e}")


# 将用户ID保存到名为user_ids.txt的文件中，每行一个。
# 运行此脚本后，您将在名为output.xlsx的Excel文件中看到提取的数据。

bv = BilibiliHelper.get_bv()


file_path_1 = "doc/user/用户_" + bv + ".csv"

config.create_file_if_not_exists(file_path_1)


def get_user_data(driver, user_id):
    user_url = f"https://space.bilibili.com/{user_id}"
    driver.get(user_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    last_request = ""
    response = ""
    json_data = {}
    for request in driver.requests:
        if "info?mid=" in request.url and request.response:
            # 更新last_request为当前请求
            last_request = request
            Content_Encoding = request.response.headers["Content-Encoding"]
            if Content_Encoding == "gzip":
                body = gzip.decompress(request.response.body)
                json_data = json.loads(body.decode("utf - 8"))
    card_url = f"https://api.bilibili.com/x/web-interface/card?mid={user_id}"
    resp_card = requests.get(
        card_url,
        headers=BilibiliHelper.get_headers(),
    )
    print("获取用户数据成功")
    data = json_data["data"]
    nickname = data["name"]
    sex = data["sex"]
    sign = data["sign"]
    level = data["level"]
    medal_level = ""
    medal_name = ""
    if data["fans_medal"]["medal"] == "true":
        medal_level = data["fans_medal"]["medal"]["level"]
        medal_name = data["fans_medal"]["medal"]["medal_name"]
    nameplate_name = data["nameplate"]["name"]
    nameplate_level = data["nameplate"]["level"]
    school = ""
    if data["school"]:
        school = data["school"]["name"]

    is_senior_member = data["is_senior_member"]
    vipStatus = data["vip"]["status"]
    vip = ""
    if vipStatus == "0":
        vip = ""
    else:
        vip = data["vip"]["label"]["text"]
    # print(resp_card.text)
    data1 = resp_card.json()
    # print(data1)
    like = data1["data"]["like_num"]
    data1 = data1["data"]["card"]
    # print(data1)
    fans = data1["fans"]
    attention = data1["attention"]

    Official_type = ""
    if data1["Official"]["type"] == "-1":
        Official_type = ""
    if data1["Official"]["type"] == "0":
        Official_type = "个人认证"
    if data1["Official"]["type"] == "1":
        Official_type = "机构认证"
    Official_desc = data1["Official"]["desc"]

    return {
        "nickname": nickname,
        "sex": sex,
        "sign": sign,
        "level": level,
        "medal_name": medal_name,
        "medal_level": medal_level,
        "nameplate_name": nameplate_name,
        "nameplate_level": nameplate_level,
        "school": school,
        "is_senior_member": is_senior_member,
        "vip": vip,
        "fans": fans,
        "attention": attention,
        "like": like,
        "Official_type": Official_type,
        "Official_desc": Official_desc,
    }


def main():
    num_count = 0
    # 从 txt 文件读取用户ID
    with open(
        "doc/user/user_ids.txt", "r", encoding="utf-8-sig", errors="replace"
    ) as f:
        user_ids = [line.strip() for line in f.readlines()]

    # print(user_ids)

    # 检查 output.xlsx 是否存在，创建或加载工作表
    with open(file_path_1, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ID",
                "昵称",
                "性别",
                "个人简介",
                "等级",
                "粉丝牌名称",
                "粉丝牌等级",
                "勋章名称",
                "勋章等级",
                "学校",
                "是否为硬核大会员",
                "会员",
                "粉丝数",
                "关注数",
                "点赞数",
                "认证信息",
                "认证信息详情",
            ]
        )

    # 启动浏览器
    options = {
        "ignore_http_methods": [
            "GET",
            "POST",
        ],  # 提取XHR请求，通常为GET或POST。如果你不希望忽略任何方法，可以忽略此选项或设置为空数组
        "custom_headers": {"X-Requested-With": "XMLHttpRequest"},  # 筛选XHR请求
    }
    chrome_options = Options()
    chrome_service = Service("../chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    url = "https://space.bilibili.com"

    driver.get(url)
    time.sleep(15)
    # 遍历用户ID并获取数据
    for user_id in user_ids[num_count:]:
        user_data = get_user_data(driver, user_id)
        row_data = [user_id] + list(user_data.values())
        num_count = num_count + 1
        print(f"第{num_count}个用户已完成爬取，UID为{user_id}")

        # 保存数据到 Excel 文件
        with open(file_path_1, mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

        # 添加随机延时
        sleep_time = random.uniform(3, 5)  # 随机生成5到10秒之间的延时
        time.sleep(sleep_time)  # 暂停执行指定的秒数

    # 关闭浏览器
    driver.quit()

    print(
        "爬取完成。说明：输出结果中-1代表缺省，如果表格里看到了-1，即为该单元格的值没爬成功，这可能由于访问过于频繁造成，可以调大93行延时时间重试"
    )


if __name__ == "__main__":
    main()
