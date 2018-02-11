#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time
from urllib import error, request
from pip._vendor.requests.packages import chardet
from bs4 import BeautifulSoup
import csv
from datetime import timedelta, datetime


def get_content(url, data=None):
    """获取网页中的html代码"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    }

    # 随机超时时间
    timeout = random.choice(range(80, 180))
    while True:
        try:
            req = request.Request(url, headers=header)
            response = request.urlopen(req, timeout=timeout)
            html = response.read()
            c = chardet.detect(html)
#             print(c)
            print(response.status)
            html = html.decode(c["encoding"])
            break
        # 超时异常
        except error.HTTPError as e:
            print('HTTPError: NoResouse', e)
            time.sleep(random.choice(range(10, 30)))
        except error.URLError as e:
            print('URLError: NoSiteExcit', e)
            time.sleep(random.choice(range(10, 30)))

    return html


def get_content_ip(url,  proxy, data=None):
    """使用代理IP获取网页中的html代码"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    }

    # 创建ProxyHandler
    proxy_support = request.ProxyHandler(proxy)
    # 创建opener
    opener = request.build_opener(proxy_support)
    # 安装opener
    request.install_opener(opener)
    # 随机超时时间
    timeout = random.choice(range(80, 180))
    while True:
        try:
            response = request.urlopen(url, timeout=timeout)
            html = response.read()
            c = chardet.detect(html)
#             print(c)
            print(response.status)
#             html = html.decode(c["encoding"])
            break
        # 超时异常
        except error.HTTPError as e:
            print('HTTPError: NoResouse', e)
            time.sleep(random.choice(range(10, 30)))
        except error.URLError as e:
            print('URLError: NoSiteExcit', e)
            time.sleep(random.choice(range(10, 30)))

    return html


def get_data(html_text):
    """获得天气信息具体内容"""
    final_info = []

    # 创建bs4实例
    try:
        bsobj = BeautifulSoup(html_text, "html.parser")
    except AttributeError as e:
        return None

    # 获取body部分
    body = bsobj.body

    # 获取更新日期
    tdate = datetime.strptime(body.find("input", {'id': 'fc_24h_internal_update_time'})[
        'value'][:8], '%Y%m%d')
    # 找到ul标签
    ul = body.find("ul", {'class': 't clearfix'})

    # 找到li标签
    lis = ul.findAll("li")

    day = 0
    for li in lis:
        day_info = []
        # 获取日期
        date = tdate + timedelta(days=day)
        day_info.append(date)

        # 获取天气
        wea = li.find("p", {"class": "wea"}).string
        day_info.append(wea)

        # 获取气温
        temp_h = li.find('span').get_text().replace("℃", "")
        temp_l = li.find('i').get_text().replace("℃", "")
        day_info.append(temp_h)
        day_info.append(temp_l)
        final_info.append(day_info)
        day += 1
    return final_info


def write_2_csv(data, file_name):
    """将数据写入csv文件"""
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


if __name__ == '__main__':
    """主函数"""
    url = "http://www.whatismyip.com.tw/"
    html = get_content(url)
    info = get_data(html)
    print(html)
    write_2_csv(info, "weather_SH.csv")
    print("Mission Complete")
