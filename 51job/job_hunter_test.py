#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import chardet
from urllib import request, error
import urllib
from bs4 import BeautifulSoup
import re
import xlwt
import csv
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


def get_content(url, data=None):
    """获取网页中的html代码"""
    header = get_random_header()

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
            html = html.decode(c["encoding"], 'ignore').encode('utf-8')
        except UnicodeError as e:
            print(e)
            html = None
        finally:
            break
    return html


def get_page_num(html):
    """获得总页数"""

    # 创建bs4实例
    page_obj = build_bsobj(html)
    # 找到标签
    try:
        page_num = page_obj.find("span", class_="td").get_text()
        page_num = int(re.sub("\D", "", page_num))
        return page_num
    except:
        print("No element found!")
        return -1


def get_salary_range(salary):
    try:
        s_min, s_max = salary.split("-")
    except ValueError as e:
        print(e)
        return None, None
    else:
        if "年" in salary:
            if "万" in salary:
                s_max = round(
                    float(re.match(r"^\d+(\.\d+)?", s_max).group()) / 12 * 10000, 2)
                s_min = round(float(s_min) / 12 * 10000, 2)
                return s_max, s_min
            else:
                return None, None

        elif "月" in salary:
            if "万" in salary:
                s_max = round(
                    float(re.match(r"^\d+(\.\d+)?", s_max).group()) * 10000, 2)
                s_min = round(float(s_min) * 10000, 2)
                return s_max, s_min
            if "千" in salary:
                s_max = round(
                    float(re.match(r"^\d+(\.\d+)?", s_max).group()) * 1000, 2)
                s_min = round(float(s_min) * 1000, 2)
                return s_max, s_min
            else:
                return None, None
        else:
            return None, None


def build_bsobj(html):
    """通过html获取bs4对象"""
    try:
        bsobj = BeautifulSoup(html, "xml")
    except AttributeError as e:
        return None
    return bsobj


def get_data(html, total_info):
    """获得职位具体内容"""

    # 创建bs4实例
    bsobj = build_bsobj(html)
    # 找到标签
    try:
        dw = bsobj.find("div", class_='dw_table')
        job_num = dw.find("div", class_="rt").get_text()
        job_num = int(re.sub("\D", "", job_num))
        els = dw.findAll("div", class_='el')
    except AttributeError as e:
        print(e)
        return None
    for el in els:
        if el.span.a:

            # 获取title
            try:
                title = el.span.a.get("title")
            except AttributeError as e:
                print(e)
                title = None
            # 获取链接
            try:
                link = el.span.a.get("href")
            except AttributeError as e:
                print(e)
                link = None
            # 获取company
            try:
                comp = el.find(class_="t2").a.get("title")
            except AttributeError as e:
                print(e)
                comp = None

            # 获取地点
            try:
                area = el.find(class_="t3").get_text()
            except AttributeError as e:
                print(e)
                area = None

            # 获取薪资
            try:
                salary = el.find(class_="t4").get_text()
            except AttributeError as e:
                print(e)
                salary = None
            else:
                max_salary, min_salary = get_salary_range(salary)

            # 获取职位详细描述
            welfare, details, loc = get_job_details(link)

            job_des_i = {
                "TITLE": title,
                "COMPANY": comp,
                "AREA": area,
                "MinSALARY": min_salary,
                "MaxSALARY": max_salary,
                "HYPERLINK": link,
                "WELFARE": welfare,
                "JOB_DETAILS": details,
                "LOCATION": loc,
            }
            total_info.append(job_des_i)
            print(job_des_i.values())
            sleep_time = random.choice(range(2, 7))
            print("On hold: %d s..." % sleep_time)
            time.sleep(sleep_time)
        else:
            continue

    return total_info


def get_job_details(url):
    """获得职位的详细内容"""
    details_html = get_content(url)
    if details_html:
        # 创建bs4实例
        details_bsobj = build_bsobj(details_html)
    else:
        return None, None, None
    # 找到福利标签
    t2 = details_bsobj.find("p", {"class": "t2"})
    if t2:
        welfare = t2.text.strip()
    else:
        welfare = None

    # 找到详细职责标签
    try:
        de_describtion = details_bsobj.find(
            "div", {"class": "bmsg job_msg inbox"}).text.strip()
        de_describtion = de_describtion[:de_describtion.find(
            "职能类别")].rstrip()
    except:
        de_describtion = None

    # 找到详细地址标签
    try:
        loc = details_bsobj.find(
            "div", {"class": "bmsg inbox"}).span.next_sibling
        loc = loc.strip('\t')
    except:
        loc = None

    return welfare, de_describtion, loc


def w2xls(file_name, datas):
    """将数据写入xls文件"""
    xls_file = xlwt.Workbook(encoding='utf-8')
    ws = xls_file.add_sheet("ME")
    # 写入title
    for r in range(1, len(datas) + 1):
        for c in range(0, len(datas[r - 1])):
            ws.write(r, c, datas[r - 1][c])
    try:
        xls_file.save(file_name)
    except FileSaveError as e:
        print("Denied to save!")


def w2csv(file_name, datas):
    """将数据写入csv文件"""
    with open(file_name, 'a', newline='', encoding='utf-8_sig') as csv_f:
        writer = csv.writer(csv_f)
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    """主函数"""

    # 关键词
    keyword = urllib.parse.urlencode({"keyword": "数据分析师"})
    # 地区
    area = "020000"
    # 获取最大页数
    page_url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=" + area + "%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&" + \
        keyword + "&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
    page_html = get_content(page_url)
    max_page = get_page_num(page_html)
    # 需要爬的页数
    page = int(input("How many pages will be caught? Maxpage is %d.\n" % max_page))
    # 循环爬取数据
    for p in range(1, page + 1):
        total_info = []
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=" + area + "%2C00&district=000000&funtype=0000&industrytype=00&issuedate=9&providesalary=99&" + \
            keyword + "&keywordtype=2&curr_page=" + str(p) + \
            "&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9"
        html = get_content(url)
        if html:
            info = get_data(html, total_info)
        else:
            continue
        print("第" + str(p) + "页爬完！")
        # 写入数据
        contents = []
        try:
            contents.append(total_info[0].keys())
            for i in range(0, len(total_info)):
                temp = []
                for content in total_info[i].values():
                    temp.append(content)
                contents.append(temp)
        #         w2xls("51job.xls", contents)
            w2csv("DA_20180307.csv", contents)
        except:
            print("Save Failed")

    print("Mission Complete")
