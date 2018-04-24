#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

params = {'loginname': "myqijin@foxmail.com", 'password': "password"}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("cookies is set to:")
print(r.cookies.get_dict())
print("----------")
print("go to profile page...")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php", cookies=r.cookies)
print(r.text)
