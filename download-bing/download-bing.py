#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create By Doracoin
# Github: https://github.com/doracoin

import json, urllib2, os, sys

# 要查询的天数(尽量写大点, 反正最多只能查询到当天和过去7天的)
days = 30
# 超时时间
time_out = 10
# 是否下载全部可能支持的分辨率(大部分图片都有三个分辨率, 1920x1200, 1920x1080, 1366x768, 其中只有1920x1200有水印)
all_px = True
# 默认保存路径
down_dir = "." + os.path.sep + "bing_wallpaper"
# 接口地址
bingUrl = "".join(['http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=', str(days), '&mkt=zh-cn'])

for i in range(0, len(sys.argv)):
    if (i == len(sys.argv) - 1):
        key = sys.argv[i]
        value = ""
    else:
        key = sys.argv[i]
        value = sys.argv[i + 1]
        # print "key: %s, value: %s" % (key, value)
    if ("-d" == key):
        days = value
        bingUrl = "".join(['http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=', str(days), '&mkt=zh-cn'])
    if ("-t" == key):
        ime_out = int(value)
    if ("-a" == key):
        if ("yes" == str(value).lower() or "y" == str(value).lower()):
            all_px = True
        else:
            all_px = False
    if ("-p" == key):
        down_dir = value
    if (i < 2 and ("-h" == key or "-help" == key or "--help" == key)):
        print "    -d    (number)   指定查询的天数, 最多只能查询到当天和过去7天的"
        print "    -t    (number)   请求超时时间, 单位：秒"
        print "    -a    (y/n, Y/N) 是否尝试下载所有分辨率的图片, 默认 yes"
        print "    -p    (string)   指定图片保存路径, 注意你的系统的分隔符 '\\' or '/'"
        print "    -h    显示帮助"
        exit(0)


def download_img(url):
    try:
        if (os.path.exists(down_dir + os.path.sep + os.path.basename(url)) == False):
            img_data = urllib2.urlopen(urllib2.Request(url)).read()
            fp = open(down_dir + os.path.sep + os.path.basename(url), 'wb')
            fp.write(img_data)
            fp.close()
            print url, "图片下载成功"
        else:
            print url, "该图片已存在，跳过"
    except urllib2.URLError, e:
        if isinstance(e, urllib2.HTTPError):
            print url, "该图片无法下载:", e.code, "" if e.reason == None else e.reason
        else:
            print url, "该图片无法下载", "" if e.reason == None else e.reason


def get_bing_wallpaper():
    if (os.path.exists(down_dir) == False):
        os.makedirs(down_dir)
    req = urllib2.Request(bingUrl)
    try:
        res_data = urllib2.urlopen(req, timeout=time_out).read()
        print "请求壁纸信息成功，正在解析\n"
    except urllib2.URLError, e:
        print "查询接口失败，有可能是网络问题，或是Bing官方关闭了这个接口，请稍后重试", "" if e.reason == None else e.reason
        exit()
    s = json.loads(res_data)
    img_counts = len(s["images"])
    for i in range(0, img_counts):
        item = s["images"][i]["url"]  # 默认1920x1080分辨率
        item_base = s["images"][i]["urlbase"]  # 图片baseurl，可以拼接分辨率
        # 1920x1080
        download_img("http://www.bing.com" + item)
        if bool(all_px):
            # 1366x768
            download_img("http://www.bing.com" + item_base + "_1366x768.jpg")
            # 1920x1200 (有水印)
            download_img("http://www.bing.com" + item_base + "_1920x1200.jpg")
        print "\n"


if __name__ == '__main__':
    print "\nWelcome to use < Bing Wallpaper Downloader 1.0 >\n"
    print "文件将会被下载到: ", down_dir
    print "是否尝试多分辨率: ", "是" if all_px == True else "否"
    print "尝试查询天数: ", days, "\n"

    # 开始下载
    get_bing_wallpaper()
