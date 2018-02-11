#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import json
import requests
import urllib
import random
import time


def get_random_header():
    list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    headers = {
        'User-Agent': random.choice(list),
    }
    return headers


def opencsv(filename):
    try:
        with open(csv_file, 'r+', encoding='utf-8') as f:
            reader = csv.reader(f)
            datas = [data for data in reader]
            return datas
    except FileNotFoundError:
        print("Sorry, file cannot be found!")
    except PermissionError:
        print("File access denied!")


def get_coordinate(url, param):
    headers = get_random_header()
    timeout = random.choice(range(80, 180))
    webrequest = requests.get(url, headers=headers,
                              params=param, timeout=timeout)
    print(webrequest.status_code)
    get_json = webrequest.json()
    try:
        lng = float(get_json["result"]["location"]["lng"])
        lat = float(get_json["result"]["location"]["lat"])
    except:
        return None, None
    else:
        return lng, lat


def rew2csv(file_name, datas):
    """将数据写入csv文件"""
    with open(file_name, 'w', newline='', encoding='utf-8_sig') as csv_f:
        writer = csv.writer(csv_f)
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    """主函数"""

    # 读取csv文件
    csv_file = "51job_test.csv"
    datas = opencsv(csv_file)
    locs = [column[8] for column in datas]
    # 我的key
    my_token = "zYSpyRGfEbDkqV1RiK12tY7HjQltDELj"
    for i in range(0, len(locs)):
        param = {'address': locs[i], 'output': 'json', 'ak': my_token}
        url = "http://api.map.baidu.com/geocoder/v2/"
        lng, lat = get_coordinate(url, param)
        datas[i].append(lng)
        datas[i].append(lat)
        if i % 100 == 0:
            time.sleep(3)
    rew2csv('51job_test.csv', datas)
    print("Mission Complete!")
