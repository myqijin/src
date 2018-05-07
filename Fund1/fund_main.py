#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Fund1.web1234567 import *

if __name__ == '__main__':
    """主函数"""
    file = r'D:\Onedrive\文档\fund.xlsx'
    fund = Fund()
    fundids = fund.readxls(file)
    print(len(fundids))
    for fundid in fundids[1:]:
        url = 'http://fund.eastmoney.com/f10/jjfl_' + str(int(fundid)) + '.html'
        scale, founded, purchase_fee, management_fee, trustee_fee, sales_charge = fund.get_data(url)

