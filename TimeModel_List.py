#!/usr/bin/env python
# coding: utf-8
from Calculate_DateTime import *
from Insert_Time import *
import copy,json,urllib2
#建立设备人员的可用时间列表，考虑时间占用，同时统计工作中心下的设备、人员和时间模型
def Analysis_Production_Calendar(Materials,Production_Calendar,NowTime,urlpath):
    TimeCalendarList={}
    for i in range(len(Production_Calendar['productionResource'])):
        if 'equipmentId' in Production_Calendar['productionResource'][i]:
            Production_Calendar['productionResource'][i]['equipmentId']=str(Production_Calendar['productionResource'][i]['equipmentId'])
        if 'workerId' in Production_Calendar['productionResource'][i]:
            Production_Calendar['productionResource'][i]['workerId']=str(Production_Calendar['productionResource'][i]['workerId'])
    if 'equipment' in Materials:
        for i in range(len(Materials['equipment'])):
            if 'workCenterId' in Materials['equipment'][i]:
                Materials['equipment'][i]['workCenterId']=str(Materials['equipment'][i]['workCenterId'])
            if 'equipmentId' in Materials['equipment'][i]:
                Materials['equipment'][i]['equipmentId']=str(Materials['equipment'][i]['equipmentId'])
    if 'worker' in Materials:
        for i in range(len(Materials['worker'])):
            if 'workCenterId' in Materials['worker'][i]:
                Materials['worker'][i]['workCenterId']=str(Materials['worker'][i]['workCenterId'])
            if 'workerId' in Materials['worker'][i]:
                Materials['worker'][i]['workerId']=str(Materials['worker'][i]['workerId'])
    if 'workCenter' in Materials:
        for i in range(len(Materials['workCenter'])):
            if 'calendarModelId' not in Materials['workCenter'][i]:
                Materials['workCenter'][i]['calendarModelId']='None'
            if 'workCenterId' in Materials['workCenter'][i]:
                Materials['workCenter'][i]['workCenterId']=str(Materials['workCenter'][i]['workCenterId'])

    lastdate_time=0
    if  Production_Calendar['productionResource']!=[]:
        for i in range(len(Production_Calendar['productionResource'])):
            sf=Production_Calendar['productionResource'][i]['unavailableTime']
            for j in range(len(sf)):
                if sf[j]['endTime']>lastdate_time:
                    lastdate_time=sf[j]['endTime']
                if isinstance(sf[j]['beginTime'],long):
                    sf[j]['beginTime']=timeStamp(sf[j]['beginTime'])
                if isinstance(sf[j]['endTime'],long):
                    sf[j]['endTime']=timeStamp(sf[j]['endTime'])
                if sf[j]['endTime'][11:]=='00:00:00':
                    sf[j]['endTime']=datesubdays(sf[j]['endTime'],1)[:10]+' 24:00:00'
    if lastdate_time==0:
        lastdate_time=NowTime
    else:
        if isinstance(lastdate_time,long):
            lastdate_time=timeStamp(lastdate_time)
    if datecompare(lastdate_time[:10]+' 00:00:00',NowTime[:10]+' 00:00:00')=='true':
        daysnum=datesub(NowTime[:10]+' 00:00:00',lastdate_time[:10]+' 00:00:00')+1
        if daysnum<500:
            daysnum=500
    else:
        daysnum=500
    pdate=NowTime[:10]
    time_=['00:00:00','24:00:00']
    dateline=[pdate]
    timeline=[time_]
    for i in range(daysnum):
        pdate=dateadddays(pdate+' 00:00:00',1)[:10]
        dateline.append(pdate)
        timeline.append(time_)
    for i in range(len(timeline[0])):
        if i%2!=0:
            if timecompare(NowTime[11:],timeline[0][i])=='false' and timecompare(NowTime[11:],timeline[0][i-1])=='true':
                timeline[0]=[NowTime[11:]]+timeline[0][i:]
    Machine_Employee_Tool_Calendar={}
    JobCenter={}
    if 'equipment' in Materials:
        for i in range(len(Materials['equipment'])):
            if 'workCenterId' in Materials['equipment'][i]:
                centerid=Materials['equipment'][i]['workCenterId']
            else:
                Materials['equipment'][i]['workCenterId']='99999'
                centerid=Materials['equipment'][i]['workCenterId']
            equipname=Materials['equipment'][i]['equipmentId']
            if centerid not in JobCenter:
                JobCenter[centerid]=[[equipname],[],'None']
            else:
                JobCenter[centerid][0].append(equipname)

    if 'worker' in Materials:
        for i in range(len(Materials['worker'])):
            if 'workCenterId' not in Materials['worker'][i]:
                Materials['worker'][i]['workCenterId']='99999'
            centerid=Materials['worker'][i]['workCenterId']
            workername=Materials['worker'][i]['workerId']
            if centerid not in JobCenter:
                JobCenter[centerid]=[[],[workername],'None']
            else:
                JobCenter[centerid][1].append(workername)
    if 'workCenter' in Materials:
        for i in range(len(Materials['workCenter'])):
            if 'calendarModelId' in Materials['workCenter'][i]:
                if Materials['workCenter'][i]['workCenterId'] in JobCenter:
                    JobCenter[Materials['workCenter'][i]['workCenterId']][2]=Materials['workCenter'][i]['calendarModelId']
                else:
                    JobCenter[Materials['workCenter'][i]['workCenterId']]=[[],[],Materials['workCenter'][i]['calendarModelId']]
            else:
                if Materials['workCenter'][i]['workCenterId'] in JobCenter:
                    JobCenter[Materials['workCenter'][i]['workCenterId']][2]='None'
                else:
                    JobCenter[Materials['workCenter'][i]['workCenterId']]=[[],[],'None']

    if 'worker' in Materials:
        for i in range(len(Materials['worker'])):
            if 'calendarModelId' not in Materials['worker'][i]:
                if 'workCenterId' in Materials['worker'][i]:
                    id1=Materials['worker'][i]['workCenterId']
                    if id1 in JobCenter:
                        Materials['worker'][i]['calendarModelId']=JobCenter[id1][2]
                    else:
                        Materials['worker'][i]['calendarModelId']='None'
                else:
                    Materials['worker'][i]['calendarModelId']='None'

    if 'equipment' in Materials:
        for i in range(len(Materials['equipment'])):
            if 'calendarModelId' not in Materials['equipment'][i]:
                if 'workCenterId' in Materials['equipment'][i]:
                    id1=Materials['equipment'][i]['workCenterId']
                    if id1 in JobCenter:
                        Materials['equipment'][i]['calendarModelId']=JobCenter[id1][2]
                    else:
                        Materials['equipment'][i]['calendarModelId']='None'
                else:
                    Materials['equipment'][i]['calendarModelId']='None'

    Rtime=copy.deepcopy(timeline)
    for key in Materials:
        if key=='equipment':
            for i in range(len(Materials['equipment'])):
                id=copy.deepcopy(Materials['equipment'][i]['equipmentId'])
                timeline=copy.deepcopy(Rtime)
                if id not in Machine_Employee_Tool_Calendar:
                    Machine_Employee_Tool_Calendar[id]=[dateline,timeline,[],Materials['equipment'][i]['calendarModelId'],0,0,0]
                    if 'workCenterId' in Materials['equipment'][i]:
                        Machine_Employee_Tool_Calendar[id][4]=Materials['equipment'][i]['workCenterId']
                    else:
                        Machine_Employee_Tool_Calendar[id][4]='99999'
                    Kpi=0
                    if Machine_Employee_Tool_Calendar[id][3]!='None':
                        if Machine_Employee_Tool_Calendar[id][3] not in TimeCalendarList:
                            payload={"cmd": "wis-basic/calendar/parseCalendarModelWithOwner","parameters": {"entity": {"calendarModelId": Machine_Employee_Tool_Calendar[id][3],"begin": str(Machine_Employee_Tool_Calendar[id][0][0]+' 00:00:00'),"end": str(Machine_Employee_Tool_Calendar[id][0][-1]+' 00:00:00'),"owner":Materials['owner']}}}
                            payload=json.dumps(payload)
                            res=urllib2.Request(urlpath, data=payload)
                            res=urllib2.urlopen(res)
                            res=res.read()
                            T_=json.loads(res)
                            if 'statusCode' in T_ and T_['statusCode']!=200:
                                Kpi=1
                            else:
                                TimeCalendarList[Machine_Employee_Tool_Calendar[id][3]]=T_
                        else:
                            T_=TimeCalendarList[Machine_Employee_Tool_Calendar[id][3]]
                        if Kpi==0:
                            NewTimeList=T_['response']['result']
                            if NewTimeList!=None:
                                NewTimeList=insertcount(NewTimeList)
                                for z in range(len(NewTimeList)):
                                    sd=NewTimeList[z]['beginTime']
                                    ed=NewTimeList[z]['endTime']
                                    date_insert=sd[:10]
                                    r=copy.deepcopy(Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)])
                                    k=[sd[11:],ed[11:]]
                                    if r==k:
                                        Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)]='None'
                                    else:
                                        if r!='None':
                                            for z in range(len(r)):
                                                r[z]=int(r[z][:2])*3600+int(r[z][3:5])*60+int(r[z][6:])
                                            for z in range(len(k)):
                                                k[z]=int(k[z][:2])*3600+int(k[z][3:5])*60+int(k[z][6:])
                                            r=[0]+r+[86400]
                                            k=Time_Occupation(k,r)
                                            if k!='None':
                                                k=k[1:-1]
                                                l_time=Machine_Employee_Tool_Calendar[id][1]
                                                point_=Machine_Employee_Tool_Calendar[id][0].index(date_insert)
                                                l_time[point_]=copy.deepcopy(inttotime(k))
                                                Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy(l_time)
                                            else:
                                                Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)]='None'
                            else:
                                Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy(timeline)
                        else:
                            Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy(timeline)
                    else:
                        Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy(timeline)
                    if Machine_Employee_Tool_Calendar[id][1][0]!='None':
                        if timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][-1])=='true':
                            Machine_Employee_Tool_Calendar[id][1]=['None']+Machine_Employee_Tool_Calendar[id][1][1:]
                        elif timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][0])=='true' and timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][-1])=='false':
                            for z in range(1,len(Machine_Employee_Tool_Calendar[id][1][0])):
                                if timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][z])=='false' and timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][z-1])=='true':
                                    if z%2!=0:
                                        Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy([[NowTime[11:]]+Machine_Employee_Tool_Calendar[id][1][0][z:]]+Machine_Employee_Tool_Calendar[id][1][1:])
                                        break
                                    else:
                                        Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy([Machine_Employee_Tool_Calendar[id][1][0][z:]]+Machine_Employee_Tool_Calendar[id][1][1:])
                                        break

        if key=='worker':
            for i in range(len(Materials['worker'])):
                id=Materials['worker'][i]['workerId']
                timeline=copy.deepcopy(Rtime)
                if id not in Machine_Employee_Tool_Calendar:
                    Machine_Employee_Tool_Calendar[id]=[dateline,timeline,[],Materials['worker'][i]['calendarModelId'],0,0,0]
                    if 'workCenterId' in Materials['worker'][i]:
                            Machine_Employee_Tool_Calendar[id][4]=Materials['worker'][i]['workCenterId']
                    else:
                        Machine_Employee_Tool_Calendar[id][4]='99999'
                    Kpi=0
                    if Machine_Employee_Tool_Calendar[id][3]!='None':
                        if Machine_Employee_Tool_Calendar[id][3] not in TimeCalendarList:
                            payload={"cmd": "wis-basic/calendar/parseCalendarModelWithOwner","parameters": {"entity": {"calendarModelId": Machine_Employee_Tool_Calendar[id][3],"begin": str(Machine_Employee_Tool_Calendar[id][0][0]+' 00:00:00'),"end": str(Machine_Employee_Tool_Calendar[id][0][-1]+' 00:00:00'),"owner":Materials['owner']}}}
                            payload=json.dumps(payload)
                            res=urllib2.Request(urlpath, data=payload)
                            res=urllib2.urlopen(res)
                            res=res.read()
                            T_=json.loads(res)
                            if 'statusCode' in T_ and T_['statusCode']!=200:
                                Kpi=1
                            else:
                                TimeCalendarList[Machine_Employee_Tool_Calendar[id][3]]=T_
                        else:
                            T_=TimeCalendarList[Machine_Employee_Tool_Calendar[id][3]]
                        if Kpi==0:
                            NewTimeList=T_['response']['result']
                            if NewTimeList!=None:
                                NewTimeList=insertcount(NewTimeList)
                                for z in range(len(NewTimeList)):
                                    sd=NewTimeList[z]['beginTime']
                                    ed=NewTimeList[z]['endTime']
                                    date_insert=sd[:10]
                                    r=copy.deepcopy(Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)])
                                    k=[sd[11:],ed[11:]]
                                    if r==k:
                                        Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)]='None'
                                    else:
                                        if r!='None':
                                            for z in range(len(r)):
                                                r[z]=int(r[z][:2])*3600+int(r[z][3:5])*60+int(r[z][6:])
                                            for z in range(len(k)):
                                                k[z]=int(k[z][:2])*3600+int(k[z][3:5])*60+int(k[z][6:])
                                            r=[0]+r+[86400]
                                            k=Time_Occupation(k,r)
                                            if k!='None':
                                                k=k[1:-1]
                                                l_time=Machine_Employee_Tool_Calendar[id][1]
                                                point_=Machine_Employee_Tool_Calendar[id][0].index(date_insert)
                                                l_time[point_]=copy.deepcopy(inttotime(k))
                                                Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy(l_time)
                                            else:
                                                Machine_Employee_Tool_Calendar[id][1][Machine_Employee_Tool_Calendar[id][0].index(date_insert)]='None'
                            else:
                                Machine_Employee_Tool_Calendar[id][1]=timeline
                        else:
                            Machine_Employee_Tool_Calendar[id][1]=timeline
                    else:
                        Machine_Employee_Tool_Calendar[id][1]=timeline
                    if Machine_Employee_Tool_Calendar[id][1][0]!='None':
                        if timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][-1])=='true':
                            Machine_Employee_Tool_Calendar[id][1]=['None']+Machine_Employee_Tool_Calendar[id][1:]
                        elif timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][0])=='true' and timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][-1])=='false':
                            for z in range(1,len(Machine_Employee_Tool_Calendar[id][1][0])):
                                if timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][z])=='false' and timecompare(NowTime[11:],Machine_Employee_Tool_Calendar[id][1][0][z-1])=='true':
                                    if z%2!=0:
                                        Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy([[NowTime[11:]]+Machine_Employee_Tool_Calendar[id][1][0][z:]]+Machine_Employee_Tool_Calendar[id][1][1:])
                                        break
                                    else:
                                        Machine_Employee_Tool_Calendar[id][1]=copy.deepcopy([Machine_Employee_Tool_Calendar[id][1][0][z:]]+Machine_Employee_Tool_Calendar[id][1][1:])
                                        break

    if Production_Calendar['productionResource']!=[]:
        for i in range(len(Production_Calendar['productionResource'])):
            insertinformation=Production_Calendar['productionResource'][i]
            insertinformation['unavailableTime']=insertcount(insertinformation['unavailableTime'])
            if 'equipmentId' in insertinformation:
                if insertinformation['equipmentId'] in Machine_Employee_Tool_Calendar:
                    insertinformation['unavailableTime']=insertcount(insertinformation['unavailableTime'])
                    for j in range(len(insertinformation['unavailableTime'])):
                        st=insertinformation['unavailableTime'][j]['beginTime']
                        et=insertinformation['unavailableTime'][j]['endTime']
                        r=[st,et]
                        if insertinformation['unavailableTime'][j]['beginTime'][:10] in Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][0]:
                            timedur=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][1][Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][0].index(insertinformation['unavailableTime'][j]['beginTime'][:10])])
                            if timedur!='None':
                                for z in range(len(timedur)):
                                    timedur[z]=int(timedur[z][:2])*3600+int(timedur[z][3:5])*60+int(int(timedur[z][6:]))
                                l_time=timedur
                                r[0]=int(r[0][11:][:2])*3600+int(r[0][11:][3:5])*60+int(r[0][11:][6:])
                                r[1]=int(r[1][11:][:2])*3600+int(r[1][11:][3:5])*60+int(r[1][11:][6:])
                                l_time=[0]+l_time+[86400]
                                km=Time_Occupation(r,l_time)
                            else:
                                km=timedur
                            if km!='None':
                                km=inttotime(km)
                                km=km[1:-1]
                            q=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][0].index(insertinformation['unavailableTime'][j]['beginTime'][:10]))
                            l=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][1])
                            l[q]=copy.deepcopy(km)
                            Machine_Employee_Tool_Calendar[insertinformation['equipmentId']][1]=l

            if 'workerId' in insertinformation:
                if insertinformation['workerId'] in Machine_Employee_Tool_Calendar:
                    insertinformation['unavailableTime']=insertcount(insertinformation['unavailableTime'])
                    for j in range(len(insertinformation['unavailableTime'])):
                        st=insertinformation['unavailableTime'][j]['beginTime']
                        et=insertinformation['unavailableTime'][j]['endTime']
                        r=[st,et]
                        if insertinformation['unavailableTime'][j]['beginTime'][:10] in Machine_Employee_Tool_Calendar[insertinformation['workerId']][0]:
                            timedur=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['workerId']][1][Machine_Employee_Tool_Calendar[insertinformation['workerId']][0].index(insertinformation['unavailableTime'][j]['beginTime'][:10])])
                            if timedur!='None':
                                for z in range(len(timedur)):
                                    timedur[z]=int(timedur[z][:2])*3600+int(timedur[z][3:5])*60+int(int(timedur[z][6:]))
                                l_time=timedur
                                r[0]=int(r[0][11:][:2])*3600+int(r[0][11:][3:5])*60+int(r[0][11:][6:])
                                r[1]=int(r[1][11:][:2])*3600+int(r[1][11:][3:5])*60+int(r[1][11:][6:])
                                l_time=[0]+l_time+[86400]
                                km=Time_Occupation(r,l_time)
                            else:
                                km=timedur
                            if km!='None':
                                km=inttotime(km)
                                km=km[1:-1]
                            q=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['workerId']][0].index(insertinformation['unavailableTime'][j]['beginTime'][:10]))
                            l=copy.deepcopy(Machine_Employee_Tool_Calendar[insertinformation['workerId']][1])
                            l[q]=copy.deepcopy(km)
                            Machine_Employee_Tool_Calendar[insertinformation['workerId']][1]=l
    L=[Machine_Employee_Tool_Calendar,JobCenter]
    return L
