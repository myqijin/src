#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon


def pdopencsv(filename):
    try:
        datas = pd.read_csv(filename, encoding='gbk', header=0)
    except FileNotFoundError:
        print("Sorry, file cannot be found!")
    except PermissionError:
        print("File access denied!")
    else:
        return datas


def basic_sh_map(ax=None, lllat=30.7, urlat=31.7, lllon=121., urlon=122.):
    m = Basemap(ax=ax, projection='stere', lon_0=(urlon + lllon) / 2, lat_0=(urlat + lllat) / 2,
                llcrnrlat=lllat, urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon, resolution='f')
    m.drawcoastlines()
    shp_info = m.readshapefile(
        r"C:\Users\myqijin\workspace\my_scrapy\src\51job\CHN_adm_shp\CHN_adm3", 'states', drawbounds=True)
    for info, shp in zip(m.states_info, m.states):
        proid = info["NAME_2"]
        if proid == "Shanghai":
            poly = Polygon(shp, facecolor='w', edgecolor='b', lw=0.2)
    return m, poly


if __name__ == '__main__':
    """主函数"""
    # 计时开始
    start_time = time.clock()
    # 读取csv文件
    csv_file = "51job_test.csv"
    datas = pdopencsv(csv_file)
    position = pd.DataFrame(datas, columns=["company", "lng", "lat"])
    position = position.dropna(axis=0, thresh=2)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    map, ploy = basic_sh_map(ax)
    ax.add_patch(ploy)
    xi = position['lng'].tolist()
    yi = position['lat'].tolist()
    x, y = map(xi, yi)
    map.scatter(x, y, s=1, c='r')
    ax.set_title("Position Distribution")
    plt.show()

    # 计时结束
    end_time = time.clock()
    print("Consuming time: %.3f s." % (end_time - start_time))
    print("Mission Complete!")
