#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
from urllib import error, request
from pip._vendor.requests.packages import chardet
from bs4 import BeautifulSoup
from datetime import datetime


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
}

url = "http://www.weather.com.cn/weather/101020100.shtml"
# 随机超时时间
timeout = random.choice(range(80, 180))
while True:
    try:
        req = request.Request(url, headers=header)
        response = request.urlopen(req, timeout=timeout)
        html = response.read()
        c = chardet.detect(html)
#             print(c)
        print("Status:", response.status)
        html = html.decode(c["encoding"])
        break
    # 超时异常
    except error.HTTPError as e:
        print('HTTPError: NoResouse', e)
        time.sleep(random.choice(range(10, 30)))
    except error.URLError as e:
        print('URLError: NoSiteExcit', e)
        time.sleep(random.choice(range(10, 30)))


final_info = []

# 创建bs4实例
bsobj = BeautifulSoup(html, "html.parser")

# 获取body部分
body = bsobj.body

# 找到li标签
t = body.find("input", {'id': 'fc_24h_internal_update_time'})['value'][:6]
ul = body.find("ul", {'class': 't clearfix'})

# 找到li标签
lis = ul.findAll("li")

for li in lis:
    day_info = []
    # 获取日期
    date = li.find("h1").string
    
print(t+date)
