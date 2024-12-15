'''
Author: reisen
Date: 2024-12-14 23:29:53
LastEditTime: 2024-12-15 16:31:45
'''
import os,sys
import csv
import datetime
import json
from multiprocessing.pool import ThreadPool
import random
import sys
import time
import requests
import configs.biliwbi as wbi
import configs.config as config
from fake_useragent import UserAgent
import os
import re
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from configs.config import BilibiliHelper
ua = UserAgent()

img_key, sub_key = wbi.getWbiKeys()

signed_params = wbi.encWbi(
    params={
        'foo': '114',
        'bar': '514',
        'baz': 1919810
    },
    img_key=img_key,
    sub_key=sub_key
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
file_path_1 = ('doc/user/用户_'+bv+'.csv')

config.create_file_if_not_exists(file_path_1)

def get_user_data(driver, user_id):
    user_url = f"https://space.bilibili.com/{user_id}/video"
    driver.get(user_url)

    wait = WebDriverWait(driver, 3)

    def get_attribute_value1(text):
        try:
            xpath = f"//*[contains(text(), '{text}')]/parent::div"
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            match = re.search(r'\d+(?:,\d+)*', element.get_attribute('title'))
            return match.group()
        except TimeoutException:
            return '-1'

    def get_attribute_value(selector, attribute):
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return element.get_attribute(attribute)
        except TimeoutException:
            return '-1'

    nickname = get_attribute_value("span#h-name", "innerText")
    description = get_attribute_value("h4.h-sign", "title")
    following = get_attribute_value(".n-data.n-gz", "title")
    fans = get_attribute_value(".n-data.n-fs", "title")
    likes = get_attribute_value1("获赞数")
    views = get_attribute_value1("播放数")
    videos = get_attribute_value("li.contribution-item.cur span.num", "innerText")
    read_count = get_attribute_value1("阅读数")

    return {
        'nickname': nickname,
        'description': description,
        'following': int(str(following).replace(",", "")),
        'fans': int(str(fans).replace(",", "")),
        'likes': int(str(likes).replace(",", "")),
        'views': int(str(views).replace(",", "")),
        'read_count':int(str(read_count).replace(",", "")),
        'videos': int(str(videos).replace(",", "")),
    }

def main():
    num_count = 0
    # 从 txt 文件读取用户ID
    with open('doc/user/user_ids.txt', 'r') as f:
        user_ids = [line.strip() for line in f.readlines()]

    # 检查 output.xlsx 是否存在，创建或加载工作表
    with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', '昵称', '个人简介', '关注数', '粉丝数', '获赞数', '播放数', '阅读数', '视频投稿数'])

    # 启动浏览器
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = "https://space.bilibili.com"
    
    driver.get(url)
    time.sleep(20)
    # 遍历用户ID并获取数据
    for user_id in user_ids[num_count:]:
        user_data = get_user_data(driver, user_id)
        row_data = [user_id] + list(user_data.values())
        num_count = num_count + 1
        print(f"第{num_count}个用户已完成爬取，UID为{user_id}")

        # 保存数据到 Excel 文件
        with open(file_path_1, mode='a', newline='', encoding='utf-8-sig') as file:
           writer = csv.writer(file)
           writer.writerow(row_data)

        # 添加随机延时
        sleep_time = random.uniform(3, 5)  # 随机生成5到10秒之间的延时
        time.sleep(sleep_time)  # 暂停执行指定的秒数

    # 关闭浏览器
    driver.quit()

    print("爬取完成。说明：输出结果中-1代表缺省，如果表格里看到了-1，即为该单元格的值没爬成功，这可能由于访问过于频繁造成，可以调大93行延时时间重试")

if __name__ == '__main__':
    main()