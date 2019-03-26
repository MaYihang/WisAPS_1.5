# coding: utf-8
from ftplib import FTP
from Main import Scheduling_Plan
import time,json
import tarfile
# !/usr/bin/python
# -*- coding: utf-8 -*-

from ftplib import FTP

def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.connect(host, 21)  # 连接
    ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
    return ftp


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024  # 设置缓冲块大小
    fp = open(localpath, 'wb')  # 以写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    ftp=ftpconnect("10.24.11.204", "ftpusers", "abc123")
    downloadfile(ftp,"/victer_plan/schedulingdata.txt","E:/plandata.txt")
    with open(r'E:/plandata.txt','rb') as input:
        readinput=input.read()
        input.close()
        Input=json.loads(readinput)
    Production_Calendar=Input['Production_Calendar']
    BOM=Input['BOM']
    Sales_Order=Input['Sales_Order']
    Materials=Input['Materials']
    OUTPUT=Scheduling_Plan(Production_Calendar,BOM,Sales_Order,Materials)
    output=json.dumps(OUTPUT)
    f1=open('e:/output1.txt','wb')
    f1.write(output)
    uploadfile(ftp,"/victer_plan/data3.txt","e:/output1.txt")
    ftp.quit()