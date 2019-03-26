#!/usr/bin/env python
# coding: utf-8
#根据工艺BOM将订单拆分成生产任务
from Calculate_ProductionNum import calculatenum
import copy,time,collections
def Analysis_Sales_Order(Sales_Order,production,Materials,OUTPUT,urlpath):
    Order={}
    prioritylist=[]
    Keylist=[]
    for i in range(len(Sales_Order['saleOrder'])):
        if Sales_Order['saleOrder'][i]['quantity']==0:
            Sales_Order['saleOrder'][i]=[]
    S={'saleOrder':[]}
    for i in range(len(Sales_Order['saleOrder'])):
        if Sales_Order['saleOrder'][i]!=[]:
            S['saleOrder'].append(Sales_Order['saleOrder'][i])
    Sales_Order=copy.deepcopy(S)

    if Sales_Order['saleOrder']==[]:
        Order={'error':0}
        return Order
    for i in range(len(Sales_Order['saleOrder'])):
        ordername_=str(Sales_Order['saleOrder'][i]['saleOrderId'])+'-'+str(Sales_Order['saleOrder'][i]['saleOrderLineId'])
        Keylist.append(ordername_)
        if ordername_ not in Order:
            Order[ordername_]=[[] for j in range(18)]
        Order[ordername_][0]=str(Sales_Order['saleOrder'][i]['materialId'])
        Processfunction=[]
        l=[Order[ordername_][0]]
        ConsumptionRate_=[]
        time_start=time.time()
        while l!=[]:
            for j in range(len(l)):
                if l[j] in production:
                    materiallist=production[l[j]][7]
                    Bom_=l[j]+'&'+production[l[j]][8]+'='
                    consumptionRate_=[]
                    for z in range(len(materiallist)):
                        if 'materialQuantity' not in materiallist[z]:
                            materiallist[z]['materialQuantity']='1'
                        Bom_+=materiallist[z]['materialQuantity']+'*'+materiallist[z]['materialId']+'+'
                        ki=materiallist[z]['materialQuantity']
                        kd=materiallist[z]['materialId']
                        consumptionRate_.append(materiallist[z]['consumptionRate'])
                        if materiallist[z]['materialType']=='manufacture_material':
                            l.append(materiallist[z]['materialId'])
                    ConsumptionRate_.append( consumptionRate_)
                    Bom_=Bom_[:-1]
                    Processfunction.append(Bom_)
                    del l[j]
                    break
                else:
                    del l[j]
                    break
        Order[ordername_][1]=Processfunction
        processnum=[]
        for j in range(len(Processfunction)):
            processnum.append('process'+str(len(Processfunction)-j))
        Order[ordername_][2]=processnum
        process_material={}
        for j in range(len(Processfunction)):
            information_=production[Processfunction[j][:Processfunction[j].index('&')]]
            Order[ordername_][3].append(information_[1])
            Order[ordername_][4].append(information_[2])
            Order[ordername_][5].append(information_[3])
            Order[ordername_][6].append(information_[5])
            Order[ordername_][7].append(information_[4])
            Order[ordername_][8].append(information_[6])
            Order[ordername_][12].append(information_[9])
            Order[ordername_][13].append(information_[10])
            Order[ordername_][14].append(information_[11])
            Order[ordername_][15].append(information_[12])
            Order[ordername_][16]=ConsumptionRate_
        NUM=calculatenum(Order[ordername_][1],Order[ordername_][0],Sales_Order['saleOrder'][i]['quantity'],Order[ordername_][14],Order[ordername_][16])
        Order[ordername_][17]=NUM[1]
        Order[ordername_][9]=NUM[0]
        Order[ordername_][11]=str(Sales_Order['saleOrder'][i]['priority'])
        prioritylist.append(Sales_Order['saleOrder'][i]['priority'])
    orderlist=collections.OrderedDict()
    orderlist2=[]
    time_start=time.time()
    while prioritylist!=[]:
        time_end=time.time()
        if time_end-time_start>600:
            Order={}
            Order['error']=106
            Order['saleOrder']=Sales_Order['saleOrder'][i]
            Order['saleOrderLineId']=Sales_Order['saleOrder'][i]['saleOrderLineId']
            return Order
        orderlist2.append(Keylist[prioritylist.index(max(prioritylist))])
        del Keylist[prioritylist.index(max(prioritylist))]
        del prioritylist[prioritylist.index(max(prioritylist))]
    for i in range(len(orderlist2)):
        orderlist[orderlist2[i]]=Order[orderlist2[i]]
    Order=orderlist
    return Order
