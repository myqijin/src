#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import job_hunter_test
import urllib
import re
from time import sleep
import random


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


def findelement(html):
    """obtain html elements of kanzhun"""

    # get company name
    pattern_comment = re.compile(
        r'<a .*?-title" href="(.*?)" target="_blank">(.*?)</a>', re.S)

    # get company rank
    pattern_rank = re.compile(
        r'<span class="grade_star ps_start mr10">.*?</span>(.*?)</dd>', re.S)
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
            pattern_name = re.compile(r'\(|（|）|\)')
            comp = re.sub(pattern_name, "", comp)
            complists[i] = re.sub(pattern_name, "", complists[i])
            if comp == complists[i]:
                return i
            else:
                return None
    except:
        return None


def getrank(url, comp):
    """obtain corresponding information"""

    webrequest = job_hunter_test.get_content(url)
    comments, ranks, links, flag = findelement(webrequest)
    nextpages = findnextpage(webrequest)
    i = matchcomp(comp, comments)
    if i != None:
        return ranks[i], links[i], True
    else:
        if nextpages:
            for nextpage in nextpages:
                webrequest = job_hunter_test.get_content(nextpage)
                comments, ranks = findelement(webrequest)
                i = matchcomp(comp, comments)
                if i:
                    return ranks[i], links[i], flag
        return None, None, flag


if __name__ == '__main__':
    """main function"""

    # open file
    csv_file = "ME_20180329.csv"
    datas = opencsv(csv_file)
    ranks = []
    remaining = []
    for data in datas[1:]:
        # combine company with url
        compurl = urllib.parse.urlencode({'q': data[1]})
        url = (r"http://www.kanzhun.com/companyl/search/?stype=&" + compurl)
        print(data[1], getrank(url, data[1]))
        rank, link, flag = getrank(url, data[1])

        # add rank to table
        data.append(rank)

        # complete hyberlink
        try:
            data.append("www.kanzhun.com" + link)
        except:
            data.append(url)
        print(data)
        # write to file
        if not flag:
            remaining.append(data)
        else:
            job_hunter_test.w2csv("ME_20180329 with KanZhun.csv", data, 'a')

        # sleep
        sleeptime = random.choice(range(15, 30))
        print("Wait %d s..." % sleeptime)
        sleep(sleeptime)

    # write uncompleted company to file
    job_hunter_test.ws2csv("ME_20180328_remaining.csv", remaining, 'w')
#     print(datas)

    print("Mission Complete!")
