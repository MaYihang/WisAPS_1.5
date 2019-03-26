#!/usr/bin/env python
# coding: utf-8
#工艺和BOM转换为便于排产的格式
import copy
def BOM_Correction(BOM):
    bom=BOM['technologyFlow']
    L=[]
    for i in range(len(bom)):
        lastmaterial=bom[i]['materialId']
        twolevelprocess=bom[i]['operation']
        techId=bom[i]['technologyId']
        sorttwolevelprocess=[]
        thisprocessId=[]
        thisinputmaterial=[]
        thisoutputmaterial=[]
        nextprocessId=[]
        idsort=[]
        iddict={}
        for j in range(len(twolevelprocess)):
            if twolevelprocess[j]['operationId'] not in iddict:
                iddict[twolevelprocess[j]['operationId']]=twolevelprocess[j]
            idsort.append(j)
            if 'nextOperationId' in twolevelprocess[j]:
                nextprocessId.append(twolevelprocess[j]['nextOperationId'])
            else:
                nextprocessId.append('None')
            if 'operationId' in twolevelprocess[j]:
                thisprocessId.append(twolevelprocess[j]['operationId'])
        lastid='None'
        id_=[]
        ThisProcessId=copy.deepcopy(thisprocessId)
        NextProcessId=copy.deepcopy(nextprocessId)
        if 'None' not in NextProcessId:
            for j in range(len(NextProcessId)):
                if NextProcessId[j] not in ThisProcessId:
                    BOM={}
                    BOM['error']=102
                    BOM['technologyId']=int(bom[i]['technologyId'])
                    BOM['operationId']=int(ThisProcessId[j])
                    return BOM
            BOM={}
            BOM['error']=105
            BOM['technologyId']=int(bom[i]['technologyId'])
            return BOM

        else:
            if NextProcessId.count('None')>1:
                BOM={}
                BOM['error']=105
                BOM['technologyId']=int(bom[i]['technologyId'])
                return BOM
            else:
                p_=[nextprocessId.index('None')]
        for j in range(len(ThisProcessId)):
            t_=[]
            for k in range(len(p_)):
                id_.append(idsort[p_[k]])
                if ThisProcessId[p_[k]] in NextProcessId:
                    for z in range(len(NextProcessId)):
                        if NextProcessId[z]==ThisProcessId[p_[k]]:
                            q_=z
                            t_.append(q_)

            p_=t_

        if j!=len(ThisProcessId)-1:
            BOM={}
            BOM['error']=105
            BOM['technologyId']=int(bom[i]['technologyId'])
            return BOM
        id_.reverse()
        Twolevelprocess=[]
        for j in range(len(id_)):
            Twolevelprocess.append(twolevelprocess[id_[j]])

        for j in range(len(Twolevelprocess)):
            l={}
            l['materialId']=str(lastmaterial)+'-'+str(j)
            l['operation']=[Twolevelprocess[j]]
            l['technologyId']=techId
            if j!=len(Twolevelprocess)-1:
                r={}
                r['consumptionRate']=0.0
                r['materialType']='manufacture_material'
                r['materialId']=l['materialId']
                r['materialQuantity']=1.0
                Twolevelprocess[j+1]['material'].append(r)
            else:
                l['materialId']=lastmaterial
            L.append(l)
    BOM['technologyFlow']=L
    return BOM

def Analysis_BOM(BOM,JobCenter):
    BOM=BOM_Correction(BOM)
    if 'error' in BOM:
        return BOM
    for i in range(len(BOM['technologyFlow'])):
        BOM['technologyFlow'][i]['materialId']=str(BOM['technologyFlow'][i]['materialId'])
        BOM['technologyFlow'][i]['technologyId']=str(BOM['technologyFlow'][i]['technologyId'])
        for j in range(len(BOM['technologyFlow'][i]['operation'])):
            if 'workCenterId' in BOM['technologyFlow'][i]['operation'][j]:
                   BOM['technologyFlow'][i]['operation'][j]['workCenterId']=str(BOM['technologyFlow'][i]['operation'][j]['workCenterId'])
            if 'material' in BOM['technologyFlow'][i]['operation'][j]:
                if BOM['technologyFlow'][i]['operation'][j]['material']!=[]:
                    for z in range(len(BOM['technologyFlow'][i]['operation'][j]['material'])):
                        if 'materialId' in BOM['technologyFlow'][i]['operation'][j]['material'][z]:
                            BOM['technologyFlow'][i]['operation'][j]['material'][z]['materialId']=str(BOM['technologyFlow'][i]['operation'][j]['material'][z]['materialId'])
                        if 'operationId' in BOM['technologyFlow'][i]['operation'][j]['material'][z]:
                            BOM['technologyFlow'][i]['operation'][j]['material'][z]['operationId']=str(BOM['technologyFlow'][i]['operation'][j]['material'][z]['operationId'])
                        if 'materialQuantity' in BOM['technologyFlow'][i]['operation'][j]['material'][z]:
                            BOM['technologyFlow'][i]['operation'][j]['material'][z]['materialQuantity']=str(BOM['technologyFlow'][i]['operation'][j]['material'][z]['materialQuantity'])
                else:
                    BOM['technologyFlow'][i]['operation'][j]['material'].append({"consumptionRate":0,"materialType":"purchase_material","materialId":"0","materialQuantity":"0"})

    production={}
    for i in range(len(BOM['technologyFlow'])):
        materialname_=BOM['technologyFlow'][i]['materialId']
        if materialname_ not in production:
            production[materialname_]=['None']
        operation_=BOM['technologyFlow'][i]['operation']
        for j in range(len(operation_)):
            u=[]
            equiplist=[]
            if 'equipmentId' not in operation_[j]:
                if str(operation_[j]['workCenterId']) not in JobCenter:
                    BOM={}
                    BOM['error']=103
                    BOM['workCenterId']=int(operation_[j]['workCenterId'])
                    return BOM
                else:
                    operation_[j]['equipmentId']=JobCenter[str(operation_[j]['workCenterId'])][0]
            for k in range(len(operation_[j]['equipmentId'])):
                equiplist.append(operation_[j]['equipmentId'][k])
            u.append(equiplist)
            workerlist=[]
            if 'workerId' not in operation_[j]:
                if str(operation_[j]['workCenterId']) not in JobCenter:
                    BOM={}
                    BOM['error']=103
                    BOM['workCenterId']=int(operation_[j]['workCenterId'])
                    return BOM
                else:
                    operation_[j]['workerId']=JobCenter[str(operation_[j]['workCenterId'])][1]
            for k in range(len(operation_[j]['workerId'])):
                workerlist.append(operation_[j]['workerId'][k])
            u.append(workerlist)
            u.append(int(operation_[j]['prepareTime']))
            u.append(int(operation_[j]['workTime']))
            u.append(int(operation_[j]['minQuantity']))
            u.append(int(operation_[j]['transferQuantity']))
            u.append(operation_[j]['material'])
            production[materialname_]+=u
            production[materialname_].append(BOM['technologyFlow'][i]['technologyId'])
            production[materialname_].append(BOM['technologyFlow'][i]['operation'][0]['operationId'])
            production[materialname_].append(operation_[j]['keyCapability'])
            production[materialname_].append(operation_[j]['scrapRate'])
            production[materialname_].append(operation_[j]['workCenterId'])
    return production
