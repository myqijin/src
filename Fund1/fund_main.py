#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from Fund1.fundMysql import Mysql
from Fund1.web1234567 import Fund

if __name__ == '__main__':
    """main"""

    file = r'D:\Onedrive\文档\fund.xlsx'

    # Fund object
    fund = Fund()
    fundids = fund.readxls(file)

    # SQL object
    fundsql = Mysql(host='localhost', port=3306, user='root', password='112233', db='fundcollection', charset='utf8')
    fundsql.connect()
    table = 'fund_info'
    try:
        for fundid in fundids[1:]:
            fundid = str(int(fundid))
            url = 'http://fund.eastmoney.com/f10/jjfl_' + fundid + '.html'
            name, scale, founded, updatedt, purchase_fee, management_fee, trustee_fee, sales_charge = fund.get_data(url)
            sql = "select * from " + table + " where ID = " + fundid + ";"
            r = fundsql.select(sql)
            print(r)
            if r:
                update = "update " + table + " set scale = " + scale + ", updatedt = " + updatedt + " WHERE ID = " + fundid + ";"
                e_r = fundsql.execute(update)
            else:
                insert = "INSERT INTO " \
                         + table + " " \
                                   "(ID,name,founded,scale,updatedt,purchasing_fee,sales_charge,management_fee,trustee_fee) " \
                                   "VALUES ('" + fundid + "','" + name + "'," + founded + "," + scale + "," + updatedt + "," + purchase_fee + "," + sales_charge + "," + management_fee + "," + trustee_fee + ");"
                e_r = fundsql.insert(insert)
        # print(e_r)
    finally:
        fundsql.dbclose()
