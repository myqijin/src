#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import job_hunter_test
import urllib
import re
from time import sleep
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


def opencsv(filename):
    """read csv file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            datas = [data for data in reader]
            return datas
    except FileNotFoundError:
        print("Sorry, file cannot be found!")
    except PermissionError:
        print("File access denied!")


def getdrive(url):
    """使用浏览器打开url"""
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(15)
    WebDriverWait(driver, 5, 1).until(
        expected_conditions.element_to_be_clickable((By.CLASS_NAME, "btn_o_l")))
    return driver


def gethtml(url, data):
    """obtain html of kanzhun"""

    driver = getdrive(url)

    # input company name to search bar
    try:
        enterblank = driver.find_element_by_id("BSSFloor")
        enterblank.clear()
        enterblank.send_keys(data)
        driver.find_element_by_class_name("btn_o_l").submit()
    except NoSuchElementException:
        print("search failure")
        html = None
    else:
        driver.implicitly_wait(15)
    # judge whether there existed verification code

        try:
            driver.find_element_by_tag_name("impression")
        except:
            if driver.find_element_by_tag_name("img"):
                sleep(10)
                input("Is verification code here?")
                enterblank.send_keys(data)
                driver.find_element_by_class_name("btn_o_l").submit()
                driver.implicitly_wait(10)
        html = driver.page_source
        c_url = driver.current_url

    # close driver
    driver.close()
    return html, c_url


def findelement(html):
    """obtain html elements of kanzhun"""

    # get company name
    pattern_comment = re.compile(
        r'<a .*?-title" href="(.*?)" target="_blank">(.*?)</a>', re.S)

    # get company rank
    pattern_rank = re.compile(
        r'<span class="grade_star ps_start mr10">.*?</span>(.*?)</dd>', re.S)

    # save the campany names, company links & company ranks to lists
    try:
        comments = re.findall(pattern_comment, html)
        compnames = [comment[1] for comment in comments]
        links = [comment[0] for comment in comments]
        ranks = re.findall(pattern_rank, html)
    except:
        print("No company found")
        return None, None, None, False
    return compnames, ranks, links, True


def findnextpage(html):
    """determine if there have next pages"""

    pattern_page = re.compile(
        r'<a ka="paging\d" herf="(.*?)">\d</a>', re.S)
    try:
        nextpages = re.findall(pattern_page, html)
        return nextpages
    except:
        return None


def matchcomp(comp, complists):
    """match company name in table with in web"""

    try:
        for i in range(0, len(complists)):

            # remove brackets
            pattern_name = re.compile(r'\(|（|）|\)')
            comp = re.sub(pattern_name, "", comp)
            complists[i] = re.sub(pattern_name, "", complists[i])

            # determine if company name is in the list
            if comp == complists[i] or complists[i] in comp:
                return i
            else:
                return None
    except:
        return None


def getrank(url, comp):
    """obtain corresponding information"""

    webrequest, c_url = gethtml(url, comp)
    comments, ranks, links, flag = findelement(webrequest)
    i = matchcomp(comp, comments)
    if i != None:
        return ranks[i], links[i], c_url, flag
    else:
        return None, None, c_url, flag


if __name__ == '__main__':
    """main function"""

    # open file
    csv_file = "ME_20180329.csv"
    datas = opencsv(csv_file)
    ranks = []
    remaining = []
    for data in datas[334:]:
        # combine company with url
        url = (r"http://www.kanzhun.com")
        rank, link, c_url, flag = getrank(url, data[1])
        # add rank to table
        data.append(rank)

        # complete hyberlink
        try:
            data.append("www.kanzhun.com" + link)
        except:
            data.append(c_url)
        print(data)
        # write to file
        if not flag:
            remaining.append(data)
        else:
            job_hunter_test.w2csv("ME_20180329 with KanZhun.csv", data, 'a')

        # sleep
        sleeptime = random.choice(range(10, 25))
        print("Wait %d s..." % sleeptime)
        sleep(sleeptime)
        job_hunter_test.ws2csv("ME_20180328_remaining.csv", remaining, 'a')

    # write uncompleted company to file

    print("Mission Complete!")
