#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import json


class AutoSend():
    driver = None

    def __init__(self, url, file):
        """使用无头浏览器打开url"""
        self.driver = webdriver.PhantomJS(
            executable_path=r"D:\Software\phantomjs-2.1.1-windows\bin\phantomjs")
        try:
            with open(file, 'r') as f:
                cookie_dict = json.loads(f)
        except FileNotFoundError:
            print("File no excited.")
        except PermissionError:
            print("File access denied!")
        self.driver.add_cookie(cookie_dict)
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def search(self, keyw, loc):
        self.name = self.driver.find_element_by_id("kedselectid")
        self.name.clear()
        self.name.send_keys(keyw)
        self.pw = self.driver.find_element_by_id("work_position_input")
        self.pw.clear()
        self.pw.send_keys(loc)
        self.driver.find_element_by_xpath(
            "/html[1]/body[1]/div[2]/form[1]/div[1]/div[1]/button[1]").submit()
        self.driver.implicitly_wait(10)
        self.driver.get_screenshot_as_file("search.png")

    def get_info(self):
        jobs = self.driver.find_elements_by_class_name("el")
        for job in jobs:
            title = job.find_element_by_class_name("t1 ").text
            print(title)

    def run(self):
        self.driver.close()


if __name__ == '__main__':
    """主函数"""
    url = r"https://search.51job.com"
    keyw = u"机械工程师"
    loc = u"上海"
    file = "51job.json"
    autosend = AutoSend(url, file)
    autosend.search(keyw, loc)
    print("Mission Completed!")
