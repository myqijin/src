#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import json
from selenium.common.exceptions import NoSuchElementException
import re
import pandas


class AutoSend():
    driver = None

    def __init__(self, url):
        """使用无头浏览器打开url"""
#         self.driver = webdriver.PhantomJS(
#             executable_path=r"D:\Software\phantomjs-2.1.1-windows\bin\phantomjs")
#         self.driver = webdriver.Chrome()
#         self.driver.get(url)
#         self.driver.implicitly_wait(5)
#         self.driver.delete_all_cookies()
#         cookies_dict = [{
#             'domain': '.51job.com',
#             "name": "51job",
#             "value": "cuid%3D132147020%26%7C%26cusername%3Dmyqijin%2540foxmail.com%26%7C%26cpassword%3D%26%7C%26cname%3D%25BD%25F0%25E7%25F9%26%7C%26cemail%3Dmyqijin%2540foxmail.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.03hgA0Djvg2M%26%7C%26cconfirmkey%3DmyGlr.6HhglRg%26%7C%26cresumeids%3D.0lW6tBTEey1A%257C%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DmyaliU%252FIfmIsQ%26%7C%26to%3DDzYFbQBgUWYFYF80AmcDMgU2UC0DaFR4XCtcZ1o6UzoPaVpBAzcBaAApATACNlI4Am0AL1YzADpWPQYoDzRSZw8yBW8AYVFlBWNfNQJlAzU%253D%26%7C%26",
#             'path': '/',
#         },
#             {'domain': '.51job.com',
#              'name': 'slife',
#              'path': '/',
#              'value': 'lowbrowser%3Dnot%26%7C%26lastlogindate%3D20180228%26%7C%26',
#              },
#             {
#             'domain': '.51job.com',
#             'name': 'ps',
#             'value': 'us%3DW2UFbwR4BjFTNV0xBX4BMFRkVGYBKVA8BTsFK11mVGFcZQVnBmNQb1Y%252FWjFXO1NgBTIKOAM2AClcagIFDmYFVltq%26%7C%26needv%3D0',
#             'path': '/',
#         },
#             {
#             'domain': '.51job.com',
#             'name': '_ujz',
#             'value': 'MTMyMTQ3MDIwMA%3D%3D',
#             'path': '/',
#         },
#             {'domain': '.51job.com',
#              'name': 'guid',
#              'path': '/',
#              'value': '15197987898303950043'}
#         ]
#         for cookie_dict in cookies_dict:
#             self.driver.add_cookie(cookie_dict)
#         self.driver.refresh()
#         self.driver.implicitly_wait(5)
#         self.driver.get_screenshot_as_file("test.png")

    def search(self, keyw):
        self.name = self.driver.find_element_by_id("kwdselectid")
        self.name.clear()
        self.name.send_keys(keyw)
        self.driver.find_element_by_id("work_position_input").submit()
        self.driver.find_element_by_id(
            "work_position_click_center_right_list_category_000000_020000").submit()
        self.driver.find_element_by_link_text("确定").click()
        self.driver.find_element_by_xpath(
            "/html[1]/body[1]/div[2]/form[1]/div[1]/div[1]/button[1]").submit()
        self.driver.implicitly_wait(10)
        self.driver.get_screenshot_as_file("search.png")

    def get_info(self, csv_file):
        try:
            datas = pandas.read_csv(csv_file, header=0, encoding='gbk')
            return datas
        except FileNotFoundError:
            print("Sorry, file cannot be found!")
        except PermissionError:
            print("File access denied!")

    def condition(self, datas):
        eligibles = datas[datas["minsalary"] >= 10000.0][0:100]
        return eligibles

    def apply(self, data):
        #                 self.driver.get(data[5])
        try:
            print(data)
#                     self.driver.find_element_by_link_text("申请职位").click()
        except NoSuchElementException:
            print("The position has been applied!")

    def next_page(self):
        pages = self.driver.find_elements_by_class_name("bk")
        try:
            pages[1].click()
        except NoSuchElementException:
            print("It's the last page!")
            flag = False
            return flag

    def closeJS(self):
        self.driver.close()
#         self.driver.quit()


if __name__ == '__main__':
    """主函数"""
    url = r"http://search.51job.com"
    keyw = u"机械工程师"
    autosend = AutoSend(url)
    datas = autosend.get_info("51job_test.csv")
    eligibles = autosend.condition(datas)
#     print(eligibles)
    eligibles["hyperlink"].apply(autosend.apply)
#     autosend.search(keyw)
#     autosend.closeJS()
    print("Mission Completed!")
