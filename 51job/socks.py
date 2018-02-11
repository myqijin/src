#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pip._vendor import requests
import random
from urllib import request
import re


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[5].text.lower() + "://" +
                       tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_ip = random.choice(ip_list)
    proxies = {'http': proxy_ip}
    return proxies


def test_ip(ip, time_out, test_url='http://icanhazip'):
    proxies = {'http': ip[0]}
    try_ip = ip[0]
    print(proxies)
    try:
        r = requests.get(test_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36', },
                         proxies=proxies, timeout=time_out)
        if r.status_code == 200:
            print('测试通过')
            return True
        else:
            print('请求码不是200')
            return False
    except:
        print('请求过程错误')
        return False


if __name__ == '__main__':
    """主函数"""
    ip_url = "http://www.xicidaili.com/nn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    }
    ip_list = get_ip_list(ip_url, headers)
    url = "http://icanhazip.com"
    timeout = random.choice(range(80, 180))
    flag = True
    for ip in ip_list:
        print(ip)
        if test_ip(ip, url, timeout):
            flag = False
            proxy_support = request.ProxyHandler(ip)
            opener = request.build_opener(proxy_support)
            request.install_opener(opener)
            req = request.Request(url, headers=headers)
            response = request.urlopen(req, timeout=timeout)
            html = response.read()
            print(html)
        else:
            print("False: " + ip+"\n")
