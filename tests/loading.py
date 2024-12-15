'''
Author: reisen
Date: 2024-12-15 18:41:00
LastEditTime: 2024-12-15 18:42:37
'''
import time
num = 50         #设置倒计时时间
timeflush = 0.5   #设置屏幕刷新的间隔时间
for i in range(0, int(num/timeflush)+1):
    print("\r正在加载:" + "|" + "-" * i + " "*(int(num/timeflush)+1-i)+"|" + str(i)+"%", end="")
    time.sleep(timeflush)
print("\r加载完成！")

