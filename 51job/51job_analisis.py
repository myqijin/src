#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pygal


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


def count_frequency(salaries):
    frequencies = {}
    ranges = range(5000, int(max(salaries) + 5001), 5000)
    for i in ranges:
        frequencies[i] = 0
    for salary in salaries:
        for i in range(0, len(ranges)):
            if salary <= ranges[i]:
                frequencies[ranges[i]] += 1
                break
    return frequencies


def show_salary(s1, s2):
    hist = pygal.Bar()
    hist.x_labels=sorted(s1.keys())
    hist._x_title="Salary range"
    hist._y_title="Num of company"
    hist.add("max",s1.values())
    hist.add("min",s2.values())
    hist.render_to_file('max_salary.svg')

if __name__ == '__main__':
    """主函数"""
    csv_file = "51job_test.csv"
    datas = opencsv(csv_file)
    locs = [column[8] for column in datas]
    max_salary = [float(column[4]) for column in datas if column[4] != '']
    min_salary = [float(column[3]) for column in datas if column[3] != '']
    max_fre = count_frequency(max_salary)
    min_fre = count_frequency(min_salary)
#     show_salary(max_fre, min_fre)
    
