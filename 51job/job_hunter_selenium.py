#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import time


class Login():
    driver = None

    def __init__(self, url):
        self.driver = webdriver.PhantomJS(
            executable_path=r"D:\Software\phantomjs-2.1.1-windows\bin\phantomjs")
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def login(self, username, password):
        self.name = self.driver.find_element_by_id("loginname")
        self.name.clear()
        self.name.send_keys(username)
        self.pw = self.driver.find_element_by_id("password")
        self.pw.clear()
        self.pw.send_keys(password)
        self.driver.find_element_by_id("login_btn").submit()
        self.driver.implicitly_wait(10)

    def run(self):
        self.driver.get_screenshot_as_file("2.png")
        self.driver.close()


if __name__ == '__main__':
    """主函数"""
    username = "myqijin@foxmail.com"
    password = "Ntkicw_51"
    url = r"https://login.51job.com"
    login = Login(url)
    login.login(username, password)
    login.run()
    print("Mission Completed!")
