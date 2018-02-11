#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def get_salary_range(salary):
    try:
        s_min, s_max = salary.split("-")
    except:
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


salary = "15-20万/"
max_salary, min_salary = get_salary_range(salary)
print(max_salary, min_salary)
