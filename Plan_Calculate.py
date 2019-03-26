#!/usr/bin/env python
# coding: utf-8
#排产计算
from TimeModel_List import Analysis_Production_Calendar
from Process_Parameter_Correction import *
from Split_Task import Analysis_Sales_Order
from Calculate_DateTime import *
from Insert_Time import *
from Integrated_Output import integrated_output
import json,urllib2,time,math
def Input_Parameter_Analysis(Production_Calendar,BOM,Sales_Order,Materials,NowTime,urlpath,OUTPUT):
    L=Analysis_Production_Calendar(Materials,Production_Calendar,NowTime,urlpath)
    Machine_Employee_Tool_Calendar=L[0]
    JobCenter=L[1]
    production=Analysis_BOM(BOM,JobCenter)
    if 'error' in production:
        return production
    Order=Analysis_Sales_Order(Sales_Order,production,Materials,OUTPUT,urlpath)
    if 'error' in Order:
        L=Order
        return L
    else:
        L=[Order,Machine_Employee_Tool_Calendar,JobCenter]
    return L

def calculateplan(Production_Calendar,BOM,Sales_Order,Materials,NowTime,OUTPUT,urlpath,L):
    AddTimeCalendarList={}
    NoKeyCapacity=Materials['NoKeyCapacity']
    if 'error' in L:
        OUTPUT=L
        return OUTPUT
    Order=L[0]
    Machine_Employee_Tool_Calendar=L[1]
    JobCenter=L[2]
    U=[]
    u={}
    schedulingprocesscont=0
    for key in Order:
        knm=int(30+schedulingprocesscont*(40/len(Order)))
        u[key]='2019-01-01 00:00:00'
        schedulingprocesscont+=1
        payload={"cmd":"wis-production/scheduling/getSchedulingById","parameters":{"id":Materials['schedulingId'],"owner":Materials['owner']}}
        payload=json.dumps(payload)
        res=urllib2.Request(urlpath,data=payload)
        res=urllib2.urlopen(res)
        res=res.read()
        T_=json.loads(res)
        if 'response' in T_ and 'result' in T_['response'] and type(T_['response']['result'])=='dict' and 'statusDict' in T_['response']['result'] and T_['response']['result']['statusDict']=='stop':
            OUTPUT={}
            OUTPUT['error']=0
            return OUTPUT
        l=Order[key]
        Num=l[9]
        bominput=[]
        bomoutput=[]
        processname=[]
        for i in range(len(l[1])):
            zz=l[16][i]
            num=Num[i]
            m=l[1][i]
            m1=m[m.index('=')+1:]
            m2=m[:m.index('=')]
            z=0
            t1=[]
            if '+' not in m1:
                if '*' in m1:
                    x=m1[m1.index('*')+1:]
                    y=m1[:m1.index('*')]
                else:
                    x=m1
                    y='1'
                t1.append([x,y,zz[0]])
            else:
                for j in range(len(m1)):
                    if m1[j]=='+':
                        if '*' in m1[z:j]:
                            x=m1[z:j][m1[z:j].index('*')+1:]
                            y=m1[z:j][0:m1[z:j].index('*')]
                            if y=='':
                                y='1'
                        else:
                            x=m1[z:j]
                            y='1'
                        t1.append([x,y,zz[0]])
                        zz=zz[1:]
                        z=j+1

                if '*' in m1[z:]:
                    x=m1[z:][m1[z:].index('*')+1:]
                    y=m1[z:][:m1[z:].index('*')]
                    if y=='':
                        y='1'
                else:
                    x=m1[z:]
                    y='1'
                t1.append([x,y,zz[0]])
                zz=zz[1:]
            bominput.append([t1,l[2][i]])
            t2=[]
            temid=m2[m2.index('&')+1:]
            m2=m2[:m2.index('&')]
            if '+' not in m2:
                if '*' in m2:
                    x=m2[m2.index('*')+1:]
                    y=m2[:m2.index('*')]
                else:
                    x=m2
                    y='1'
                t2.append([x,y])
            else:
                for j in range(len(m2)):
                    if m2[j]=='+':
                        if '*' in m1[z:j]:
                            x=m2[z:j][m2[z:j].index('*')+1:]
                            y=m2[z:j][0:m2[z:j].index('*')]
                        else:
                            x=m2[z:j]
                            y='1'
                        t2.append([x,y])
                        z=j+1
                if '*' in m2[z:]:
                    x=m2[z:][m2[z:].index('*')+1:]
                    y=m2[z:][z:m2[z:].index('*')]
                else:
                    x=m2[z:]
                    y='1'
                t2.append([x,y])
            bomoutput.append([t2,l[2][i],temid,num])
        production_ID=Order[key][0]
        Raw_Material=[]
        Raw_Material_num=[]
        output=[]
        output.append(production_ID)
        for i in range(len(bominput)):
            for j in range(len(bominput[i][0])):
                km=bominput[i][0][j][0]
                km_num=bominput[i][0][j][1]
                h=0
                for z in range(len(bomoutput)):
                    for f in range(len(bomoutput[z][0])):
                        if bomoutput[z][0][f][0]==km:
                            h=1
                            break
                    if h==1:
                        break
                if h==0:
                    Raw_Material.append(km)
                    Raw_Material_num.append(km_num)

        satisfy_time=[]
        for i in range(len(Raw_Material)):
            satisfy_time.append(NowTime)
        Raw_Material=[Raw_Material,satisfy_time]
        Bomoutput=copy.deepcopy(bomoutput)
        Bominput=copy.deepcopy(bominput)
        time_start=time.time()
        while Bomoutput!=[]:
            payload={"cmd":"wis-production/scheduling/getSchedulingById","parameters":{"id":Materials['schedulingId'],"owner":Materials['owner']}}
            payload=json.dumps(payload)
            res=urllib2.Request(urlpath,data=payload)
            res=urllib2.urlopen(res)
            res=res.read()
            T_=json.loads(res)
            if 'response' in T_ and 'result' in T_['response'] and type(T_['response']['result'])=='dict' and 'statusDict' in T_['response']['result'] and T_['response']['result']['statusDict']=='stop':
                OUTPUT={}
                OUTPUT['error']=0
                return OUTPUT
            stopbreak=0
            for i in range(len(Bominput)):
                num=Bomoutput[i][-1]
                hg=1
                for j in range(len(Bominput[i][0])):
                    if Bominput[i][0][j][0] not in Raw_Material[0]:
                        hg=hg*0
                    else:
                        hg=hg*1
                if hg==1:
                    Datesatic=[]
                    for z in range(len(Bominput[i][0])):
                        if Datesatic==[]:
                            Datesatic=Raw_Material[1][Raw_Material[0].index(Bominput[i][0][z][0])]
                        if datecompare(Raw_Material[1][Raw_Material[0].index(Bominput[i][0][z][0])],Datesatic)=='true':
                            Datesatic=Raw_Material[1][Raw_Material[0].index(Bominput[i][0][z][0])]
                    capcity_list=[]
                    k=l[2].index(Bominput[i][1])
                    if l[13][k]=='equipment':
                        machinecapacitylist=[]
                        keysource='equipment'
                        if l[3][k]==[]:
                            OUTPUT['error']=100
                            OUTPUT['workCenterId']=int(l[15][k])
                            return OUTPUT
                            os.exit()
                        for z in range(len(l[3][k])):
                            machinecapacitylist.append(Machine_Employee_Tool_Calendar[l[3][k][z]])
                    elif l[13][k]=='person':
                        keysource='person'
                        machinecapacitylist=[]
                        if l[4][k]==[]:
                            OUTPUT['error']=100
                            OUTPUT['workCenterId']=int(l[15][k])
                            return OUTPUT
                            os.exit()
                        for z in range(len(l[4][k])):
                            machinecapacitylist.append(Machine_Employee_Tool_Calendar[l[4][k][z]])
                    T=machinecapacitylist[0][0]
                    if Datesatic[:10] in T:
                        po=T.index(Datesatic[:10])
                        poo=copy.deepcopy(po)
                        starttime=copy.deepcopy(Datesatic[11:])
                        z=po
                        while z<len(T):
                            if z==len(T)-1:
                                t=T[z]+' 00:00:00'
                                adddays=[]
                                for f in range(1,366):
                                    adddays.append(dateadddays(t,f)[:10])
                                sd_=adddays[0]
                                ed_=adddays[-1]
                                for vivo in Machine_Employee_Tool_Calendar:
                                    Machine_Employee_Tool_Calendar[vivo][0]=copy.deepcopy(Machine_Employee_Tool_Calendar[vivo][0]+adddays)
                                    Machine_Employee_Tool_Calendar[vivo][1]=copy.deepcopy(Machine_Employee_Tool_Calendar[vivo][1]+[['00:00:00','24:00:00'] for oppo in range(len(adddays))])
                                    Kpi=0
                                    if Machine_Employee_Tool_Calendar[vivo][3]!='None':
                                        timeID=int(Machine_Employee_Tool_Calendar[vivo][3])
                                        if timeID not in AddTimeCalendarList:
                                            payload={"cmd": "wis-basic/calendar/parseCalendarModelWithOwner","parameters": {"entity": {"calendarModelId": timeID,"begin": sd_+' 00:00:00',"end": ed_+' 00:00:00',"owner":Materials['owner']}}}
                                            payload=json.dumps(payload)
                                            res=urllib2.Request(urlpath, data=payload)
                                            res=urllib2.urlopen(res)
                                            res=res.read()
                                            T_=json.loads(res)
                                            if 'statusCode' in T_ and T_['statusCode']!=200:
                                                Kpi=1
                                            else:
                                                AddTimeCalendarList[timeID]=T_
                                        else:
                                            T_=AddTimeCalendarList[timeID]
                                        if Kpi==0:
                                            NewTimeList=T_['response']['result']
                                            if NewTimeList!=None:
                                                NewTimeList=insertcount(NewTimeList)
                                                for ss in range(len(NewTimeList)):
                                                    sd=NewTimeList[ss]['beginTime']
                                                    ed=NewTimeList[ss]['endTime']
                                                    date_insert=sd[:10]
                                                    r=Machine_Employee_Tool_Calendar[vivo][1][Machine_Employee_Tool_Calendar[vivo][0].index(date_insert)]
                                                    if sd[:10]==NowTime[:10]:
                                                        sd=NowTime
                                                    k_=[sd[11:],ed[11:]]
                                                    if r==k_:
                                                        Machine_Employee_Tool_Calendar[vivo][1][Machine_Employee_Tool_Calendar[vivo][0].index(date_insert)]='None'
                                                    else:
                                                        if r!='None':
                                                            for zz in range(len(r)):
                                                                r[zz]=int(r[zz][:2])*3600+int(r[zz][3:5])*60+int(r[zz][6:])
                                                            for z in range(len(k_)):
                                                                k_[z]=int(k_[z][:2])*3600+int(k_[z][3:5])*60+int(k_[z][6:])
                                                            k_=Time_Occupation(k_,r)
                                                            if k_!='None':
                                                                k_=k_[1:-1]
                                                                l_time=Machine_Employee_Tool_Calendar[vivo][1]
                                                                point_=Machine_Employee_Tool_Calendar[vivo][0].index(date_insert)
                                                                l_time[point_]=copy.deepcopy(inttotime(k_))
                                                                Machine_Employee_Tool_Calendar[vivo][1]=copy.deepcopy(l_time)
                                                            else:
                                                                Machine_Employee_Tool_Calendar[vivo][1][Machine_Employee_Tool_Calendar[vivo][0].index(date_insert)]=copy.deepcopy('None')
                                    T=Machine_Employee_Tool_Calendar[vivo][0]

                                if l[13][k]=='equipment' and l[3][k]!='None':
                                    machinecapacitylist=[]
                                    keysource='equipment'
                                    for s in range(len(l[3][k])):
                                        machinecapacitylist.append(Machine_Employee_Tool_Calendar[l[3][k][s]])
                                elif l[13][k]=='person' or l[4][k]=='None':
                                    machinecapacitylist=[]
                                    keysource='person'
                                    for s in range(len(l[4][k])):
                                        machinecapacitylist.append(Machine_Employee_Tool_Calendar[l[4][k][s]])

                            for w in range(len(machinecapacitylist)):
                                stopbreak=0
                                time_=[]
                                mn=[]
                                if machinecapacitylist[w][1][z]!='None':
                                    time_.append(machinecapacitylist[w][1][z])
                                    for f in range(1,len(time_[0])):
                                        if f%2!=0:
                                            mn.append([time_[0][f-1],time_[0][f]])
                                if mn!=[]:
                                    for f in range(len(mn)):
                                        st=mn[f][0]
                                        et=mn[f][1]
                                        if timecompare(starttime,et)=='true' and z==poo:
                                            continue
                                        elif timecompare(starttime,et)=='false' and timecompare(starttime,st)=='true' and z==poo:
                                            st=starttime
                                        mn[f]=[st,et]
                                        timeduring=(int(et[:2])*3600+int(et[3:5])*60+int(et[6:]))-(int(st[:2])*3600+int(st[3:5])*60+int(st[6:]))
                                        if l[7][l[2].index(Bominput[i][1])]==0:
                                            n=num
                                        else:
                                            n=round(timeduring/l[7][l[2].index(Bominput[i][1])],6)
                                        if n<num:
                                            if n>=l[6][k]:
                                                num-=n
                                                r=copy.deepcopy(mn[f])
                                                fe=copy.deepcopy(machinecapacitylist[w][1])
                                                re=copy.deepcopy(inserttime(r,fe[z],T[z],T[poo],starttime))
                                                machinecapacitylist[w][1][z]=copy.deepcopy(re)
                                                v_=l[2].index(Bominput[i][1])
                                                if keysource=='equipment':
                                                    productmachine=l[3][v_][w]
                                                else:
                                                    productmachine=l[4][v_][w]
                                                endtime=T[z]+' '+et
                                                if et=='24:00:00':
                                                    endtime=dateadddays(T[z][:10]+' 00:00:00',1)
                                                if datecompare(u[key],endtime)=='false':
                                                    u[key]=endtime
                                                U.append([key,[Bominput[i],Bomoutput[i]],n,T[z]+' '+st,endtime,productmachine,l[12][v_],machinecapacitylist[w][4]])

                                                t_k=T[z]+' '+et
                                                if et=='24:00:00':
                                                    t_k=dateadddays(T[z][:10]+' 00:00:00',1)
                                                if Bomoutput[i][0][0][0] not in Raw_Material[0]:
                                                    Raw_Material[0].append(Bomoutput[i][0][0][0])
                                                    Raw_Material[1].append(t_k)
                                                else:
                                                    ctime=Raw_Material[1][Raw_Material[0].index(Bomoutput[i][0][0][0])]
                                                    if datecompare(t_k,ctime)=='true':
                                                        Raw_Material[1][Raw_Material[0].index(Bomoutput[i][0][0][0])]=t_k
                                        else:
                                            if num>=l[6][k]:
                                                et=dateaddtime(st,math.ceil(num*l[7][l[2].index(Bominput[i][1])]))[11:]
                                                mn[f]=[st,et]
                                                v_=l[2].index(Bominput[i][1])
                                                if keysource=='equipment':
                                                    productmachine=l[3][v_][w]
                                                else:
                                                    productmachine=l[4][v_][w]
                                                endtime=T[z]+' '+et
                                                if et=='24:00:00':
                                                    endtime=dateadddays(T[z][:10]+' 00:00:00',1)
                                                if datecompare(u[key],endtime)=='false':
                                                    u[key]=endtime
                                                U.append([key,[Bominput[i],Bomoutput[i]],num,T[z]+' '+st,endtime,productmachine,l[12][v_],machinecapacitylist[w][4]])
                                                r=copy.deepcopy(mn[f])
                                                fe=copy.deepcopy(machinecapacitylist[w][1])
                                                re=copy.deepcopy(inserttime(r,fe[z],T[z],T[poo],starttime))
                                                machinecapacitylist[w][1][z]=copy.deepcopy(re)
                                                t_k=T[z]+' '+et
                                                if et=='24:00:00':
                                                    t_k=dateadddays(T[z][:10]+' 00:00:00',1)
                                                if Bomoutput[i][0][0][0] not in Raw_Material[0]:
                                                    Raw_Material[0].append(Bomoutput[i][0][0][0])
                                                    Raw_Material[1].append(t_k)
                                                else:
                                                    ctime=Raw_Material[1][Raw_Material[0].index(Bomoutput[i][0][0][0])]
                                                    if datecompare(t_k,ctime)=='true':
                                                        Raw_Material[1][Raw_Material[0].index(Bomoutput[i][0][0][0])]=t_k
                                                del Bominput[i]
                                                del Bomoutput[i]
                                                stopbreak=1
                                        if stopbreak==1:
                                            break
                                if stopbreak==1:
                                    break

                            if keysource=='person':
                                for e in range(len(machinecapacitylist)):
                                    Machine_Employee_Tool_Calendar[l[4][k][e]]=copy.deepcopy(machinecapacitylist[e])
                            else:
                                for e in range(len(machinecapacitylist)):
                                    Machine_Employee_Tool_Calendar[l[3][k][e]]=copy.deepcopy(machinecapacitylist[e])
                            if stopbreak==1:
                                break
                            z+=1
                if stopbreak==1:
                    break
    OUTPUT['productionOrder']=[]
    OUTPUT['jiaohuoT']=u
    OUTPUT=integrated_output(OUTPUT,U,urlpath,Materials,Order,JobCenter)
    return OUTPUT
