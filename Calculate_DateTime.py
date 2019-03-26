#!/usr/bin/env python
# coding: utf-8
#日期时间的计算类
import datetime,time

def timeStamp(timeNum): #毫秒戳转成日期时间
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def date_timechrchuo(dt): #日期时间转成毫秒戳
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeArray) * 1000)
    return timestamp

def timetosecond(t): #时分秒转成秒数
    h,m,s=t.strip().split(":")
    T=int(h)*3600+int(m)*60+int(s)
    return T

def datesub(Jobstartdate,Jobfinishdate): #日期相减计算天数
    delta=datetime.datetime.strptime(Jobfinishdate, '%Y-%m-%d %H:%M:%S')-datetime.datetime.strptime(Jobstartdate, '%Y-%m-%d %H:%M:%S')
    return delta.days

def dateaddtime(date, second): #时间加秒数
    date=str(datetime.datetime.strptime(date,'%H:%M:%S')+datetime.timedelta(seconds=second))
    return date

def dateadddays(date, day): #日期加天数
    date = str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=day))
    return date

def datesubdays(date, day): #日期减天数
    date = str(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(days=day))
    return date

def datecompare(date1, date2): #日期比较
    tim1 = time.mktime(time.strptime(date1, '%Y-%m-%d %H:%M:%S'))
    tim2 = time.mktime(time.strptime(date2, '%Y-%m-%d %H:%M:%S'))
    if tim1 >= tim2:
        date = 'true'
    else:
        date = 'false'
    return date

def timecompare(date1,date2): #时间比较
    k,f,c=date1.strip().split(":")
    kfc=int(k)*3600+int(f)*60+int(c)
    m,d,l=date2.strip().split(":")
    mdl=int(m)*3600+int(d)*60+int(l)
    if kfc>=mdl:
        date='true'
    else:
        date='false'
    return date

def inttotime(l): #秒数转成时分秒格式
    for i in range(len(l)):
        m,s=divmod(l[i],60)
        h,m=divmod(m,60)
        l[i]="%02d:%02d:%02d"%(h,m,s)
    return l
