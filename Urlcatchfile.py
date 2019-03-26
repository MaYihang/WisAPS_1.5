#!/usr/bin/env python
# coding: utf-8
#通过URL获取文件下载到本地
#将本地文件上传到指定URL
#import urllib
import urllib2
#import requests
url = 'https://cdn.i5sesol.com/wis/NzgAACiKuwSNpIkV-ee25d11a-9f78-4996-ab91-a002bf5e2d02'
def urlgetpostfile(url):

    print "downloading with urllib2"
    f=urllib2.urlopen(url)
    data=f.read()
    with open("e:/code.txt", "wb") as code:
        code.write(data)


urlgetpostfile(url)