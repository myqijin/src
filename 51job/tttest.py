#!/usr/bin/env python3
# -*- coding: utf-8 -*-


odd = [x for x in range(0, 101) if x % 2 == 0]
print(sum(odd))

for x in range(0, 35):
    y = (94 - 2 * x) / 4
    if y % 4 == 0:
        print("x=%d, y=%d" % (x, y))
    else:
        continue


verifycode = input("Please enter verification code:")
print(verifycode)