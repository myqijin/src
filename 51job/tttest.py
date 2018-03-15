#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

s1="上海-长宁区"
s2="上海"
s3="上海浦东新区科苑路88号德国中心（近张江地铁站）"
arr = re.match(r'(\S+)\-(\S+)',s1)
if arr:
    print(arr[2])
else:

