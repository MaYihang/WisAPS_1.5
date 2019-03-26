#!/usr/bin/env python
# coding: utf-8
from Calculate_DateTime import *
import copy
#时间插空计算
def insertcount(inserttime):
    U=[]
    for i in range(len(inserttime)):
        if 'available' not in  inserttime[i]:
            inserttime[i]['available']='0'
        if inserttime[i]['available']=='0':
            if 'begin' in inserttime[i]:
                sd=inserttime[i]['begin']
            elif 'beginTime' in inserttime[i]:
                sd=inserttime[i]['beginTime']
            if 'end' in inserttime[i]:
                ed=inserttime[i]['end']
            elif 'endTime' in inserttime[i]:
                ed=inserttime[i]['endTime']
            if ed[11:]=='23:59:00':
                ed=ed[:11]+'24:00:00'
            if datecompare(sd[:10]+' 00:00:00',ed[:10]+' 00:00:00')=='false':
                sdate=sd[:10]
                d={}
                d['beginTime']=sd
                d['endTime']=sd[:10]+' 24:00:00'
                d['available']='0'
                U.append(d)
                t=sd[:10]
                t=dateadddays(t+' 00:00:00',1)[:10]
                stopN=0
                while t!=ed[:10]:
                    d={}
                    d['beginTime']=t+' 00:00:00'
                    d['endTime']=t+' 24:00:00'
                    d['available']='0'
                    U.append(d)
                    t=dateadddays(t+' 00:00:00',1)[:10]
                if ed!=t+' 00:00:00':
                    d={}
                    d['beginTime']=t+' 00:00:00'
                    d['endTime']=ed
                    d['available']='0'
                    U.append(d)
            elif sd[:10]==ed[:10]:
                d={}
                d['beginTime']=sd
                d['endTime']=ed
                d['available']='0'
                U.append(d)
    return U

def Time_Occupation(k,r):
    if k[0]!=k[1]:
        for z in range(len(r)-1):
            if r[z+1]>k[0]>r[z] and z%2!=0:
                t1=r[:z+1]+[k[0]]
            elif r[z+1]>=k[0]>=r[z] and z%2==0:
                t1=r[:z+1]
            if r[z+1]>k[1]>r[z] and z%2!=0:
                t2=[k[1]]+r[z+1:]
                r=t1+t2
                break
            elif r[z+1]>=k[1]>=r[z] and z%2==0:
                t2=r[z+1:]
                r=t1+t2
                break
        if r==[0,86400]:
            r='None'
    return r

def Time_Crossing(l1):
    l2=[]
    if len(l1)>1:
        for i in range(len(l1)):
            l22=[]
            for j in range(len(l1[i])):
                k=l1[i][j]
                l22.append(int(k[0:2])*3600+int(k[3:5])*60+int(k[6:]))
            l2.append([0]+l22+[86400])
        r=[0,0,86400,86400]
        l3=l2
        if len(l3)>1:
            for i in range(len(l3)):
                for j in range(len(l3[i])-1):
                    if j%2==0:
                        k=[l3[i][j],l3[i][j+1]]
                        if k[0]!=k[1]:
                            r=Time_Occupation(k,r)
        L=[r[0]]
        for i in range(1,len(r)):
            if L!=[]:
                if r[i]==L[-1]:
                    del L[-1]
                else:
                    L.append(r[i])
            else:
                L.append(r[i])

        R=[]
        for i in range(len(L)):
            R.append(dateaddtime('00:00:00',L[i]))
        L=[]
        for i in range(len(R)-1):
            if i%2!=0:
                L.append([R[i][11:],R[i+1][11:]])
    else:
        Tlist=l1[0]
        L=[]
        for i in range(1,len(Tlist)):
            if i%2!=0:
                L.append([Tlist[i-1],Tlist[i]])
    return L

def inserttime(l1,l2,date1,date2,starttime):
    sst=copy.deepcopy(starttime)
    ll1=copy.deepcopy(l1)
    ll2=[0 for i in range(len(l2))]
    for i in range(len(l1)):
        ll1[i]=int(l1[i][:2])*3600+int(l1[i][3:5])*60+int(l1[i][6:])
    for i in range(len(l2)):
        ll2[i]=int(l2[i][:2])*3600+int(l2[i][3:5])*60+int(l2[i][6:])
    ll2=[0]+ll2+[86400]
    km=0
    starttime=int(starttime[:2])*3600+int(starttime[3:5])*60+int(starttime[6:])
    if date1==date2:
        if ll1[0]<=starttime<ll1[1]:
            ll1=[starttime,ll1[1]]
            km=1
        elif ll1[0]>=starttime:
            km=1
        elif ll1[1]<starttime:
            km=0
    else:
        km=1
    if km==1:
        ll2=Time_Occupation(ll1,ll2)
        if len(ll2)<=2:
            ll2='None'
        elif len(ll2)>2 and ll2!='None':
            ll2=inttotime(ll2)
        if ll2!='None':
            ll2=ll2[1:-1]
    else:
        ll2=l2
    starttime=copy.deepcopy(sst)
    return ll2
