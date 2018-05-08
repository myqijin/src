#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import re
import time
from datetime import date, datetime
from urllib import request, error

import chardet
import xlrd as xlrd
from bs4 import BeautifulSoup


class Fund():

    def __init__(self):
        pass

    def get_random_header(self):
        """request header"""
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

    def get_content(self, url):
        """获取网页中的html代码"""

        header = self.get_random_header()

        # 随机超时时间
        timeout = random.choice(range(80, 180))
        html = None
        while True:
            try:
                print("\n")
                print(url)
                req = request.Request(url, headers=header)
                response = request.urlopen(req, timeout=timeout)
                html = response.read()
                print("Status: ", response.status)
            # 超时异常
            except error.HTTPError as e:
                print('HTTPError: NoResouse', e.reason)
            except error.URLError as e:
                print('URLError: NoSiteExcit', e.reason)
            try:
                c = chardet.detect(html)
                html = html.decode(c["encoding"], 'ignore')
            except UnicodeError as e:
                print(e)
                html = None
            finally:
                break
        return html

    def build_bsobj(self, html):
        """通过html获取bs4对象"""
        try:
            bsobj = BeautifulSoup(html, "lxml")
        except AttributeError as e:
            return None
        return bsobj

    def get_data(self, url):
        """obtain fund info"""

        sleep_time = random.choice(range(2, 7))
        print("\nOn hold: %d s..." % sleep_time)
        time.sleep(sleep_time)

        # get html
        html = self.get_content(url)
        # 创建bs4实例
        bsobj = self.build_bsobj(html)
        # 找到标签
        try:
            info = bsobj.find("div", class_='bs_gl')
            tds = info.find_all("label")

            # get name
            name = bsobj.find("h4", class_="title").a.get_text()

            # search scale tag
            scale = tds[4].span.get_text()

            # search founded date
            founded = tds[0].span.get_text()

            # search purchase fee
            purchase_fee = bsobj.find("b", class_="sourcerate").next_sibling.next_element.get_text()

            # find operating fee
            tds = bsobj.find_all("div", class_="box")[3].find_all("td", class_="w135")
            management_fee = tds[0].get_text()
            trustee_fee = tds[1].get_text()
            sales_charge = tds[2].get_text()

        except AttributeError as e:
            print(e)
            return None

        else:
            # extract
            name = re.search(r"(\S*)\s", name).group(0)
            scale = re.search(r"\d{1,2}\.\d{1,2}", scale).group()
            purchase_fee = float(re.search(r"\d{1,2}\.\d{1,2}", purchase_fee).group()) / 100.0
            founded = datetime.strptime(founded, '%Y-%m-%d').strftime('%Y%m%d')

            # founded = re.search(r"\d{4}(\-|\/|.)\d{1,2}\1\d{1,2}", founded).group()
            management_fee = float(re.search(r"\d{1,2}\.\d{1,2}", management_fee).group()) / 100
            trustee_fee = float(re.search(r"\d{1,2}\.\d{1,2}", trustee_fee).group()) / 100

            # judge sales_charge == 0 ?
            if re.search(r"\d{1,2}\.\d{1,2}", sales_charge):
                sales_charge = float(re.search(r"\d{1,2}\.\d{1,2}", sales_charge).group()) / 100
            else:
                sales_charge = 0
            updated = date.today().strftime('%Y%m%d')
            print(name, scale, founded, updated, purchase_fee, management_fee, trustee_fee, sales_charge)
            return name, scale, founded, updated, str(purchase_fee), str(management_fee), str(trustee_fee), str(
                sales_charge)

    def readxls(self, file):
        """read column from excel"""
        try:
            workbook = xlrd.open_workbook(file)
            sheet = workbook.sheet_by_name('Sheet1')
        except FileNotFoundError as e:
            print(e)
        else:
            data = sheet.col_values(0)
        return data
