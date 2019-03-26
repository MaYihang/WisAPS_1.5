#!/usr/bin/env python
# coding: utf-8
#将排产结果整理为输出格式
import json,urllib2
def integrated_output(OUTPUT,U,urlpath,Materials,Order,JobCenter):
    m='None'
    for i in range(len(U)):
            knm=int(70+i*(30/len(U)))
            test_data={'cmd': 'wis-production/scheduling/parseSchedulingLogWithOwner','parameters': {'entity': {'owner':Materials['owner'],"schedulingId": Materials['schedulingId'],"progress":knm ,"description": 0}}}
            test_data_urlencode=json.dumps(test_data)
            req_=urllib2.Request(urlpath,data =test_data_urlencode)
            h=U[i][0]+'-'+U[i][1][1][1]
            if h!=m:
                m=h
                zq=1
                U[i].append(str(zq))
            else:
                zq=zq+1
                U[i].append(str(zq))
            U[i].append(-1)
            outmaterials_=U[i][1][1][0]
            for j in range(len(outmaterials_)):
                if '-' in outmaterials_[j][0]:
                    U[i][1][1][0][j][0]=U[i][1][1][0][j][0][:U[i][1][1][0][j][0].index('-')]
            l={}
            if '-' in U[i][0]:
                l['saleOrderId']=U[i][0][:U[i][0].index('-')]
                l['saleOrderLineId']=U[i][0][U[i][0].index('-')+1:]
            l['materialId']=U[i][1][1][0][0][0]
            l['quantity']=U[i][2]
            l['materialRequirement']=[]
            for j in range(len(U[i][1][0][0])):
                PROcess=U[i][1][0][1]
                ppo_=Order[U[i][0]][2].index(PROcess)
                mater_need={}
                if '#' in U[i][1][0][0][j][0]:
                    U[i][1][0][0][j][0]=U[i][1][0][0][j][0][0:U[i][1][0][0][j][0].index('#')]
                if U[i][1][0][0][j][0]!="0"and U[i][1][0][0][j][0]!= l['materialId'] and '-' not in U[i][1][0][0][j][0]:
                    mater_need['materialId']=U[i][1][0][0][j][0]
                else:
                    mater_need['materialId']=-1
                mater_need['quantity']=round(float(U[i][1][0][0][j][1])*float(U[i][2])*(1+float(U[i][1][0][0][j][2])/100),6)
                mater_need['time']=U[i][3]
                mater_need['consumptionRate']=U[i][1][0][0][j][2]
                if mater_need['materialId']!=-1:
                    l['materialRequirement'].append(mater_need)
            if l['materialRequirement']==[]:
                del l['materialRequirement']
            k_=[]
            for z in Order[U[i][0]][17][ppo_]:
                k_material={}
                if '-' in z:
                    continue
                s=Order[U[i][0]][17][ppo_][z]
                if '#' in z:
                    k_material['materialId']=z[0:z.index('#')]
                    k_material['quantity']=s
                else:
                    if z!='0':
                        k_material['materialId']=z
                        k_material['quantity']=s
                if k_material!={}:
                     k_.append(k_material)
            if k_!=[]:
                l['materialNetRequirement']=k_
            l['technologyId']=U[i][1][1][2]
            l['operationId']=U[i][6]
            l['productionTaskNumber']=U[i][8]
            l['startTime']=U[i][3]
            l['endTime']=U[i][4]
            l['workCenterId']=U[i][7]
            if U[i][5] in JobCenter[U[i][7]][0]:
                l['equipmentIds']=[U[i][5]]
            elif U[i][5] in JobCenter[U[i][7]][1]:
                l['workerIds']=[U[i][5]]
            if U[i][9] in JobCenter[U[i][7]][0]:
                l['equipmentIds']=[U[i][9]]
            elif U[i][9] in JobCenter[U[i][7]][1]:
                l['workerIds']=[U[i][9]]
            OUTPUT['productionOrder'].append(l)
    return OUTPUT
