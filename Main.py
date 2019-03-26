#!/usr/bin/env python
# coding: utf-8
import datetime,time,copy,json,urllib2,collections,os,sys,math
import Catch_urlpath
from CheckInput import checkinput
from Plan_Calculate import Input_Parameter_Analysis,calculateplan
#from Genetic_Algorithm import AlgorithmOptimization

def Scheduling_Plan(Production_Calendar,BOM,Sales_Order,Materials):
    OUTPUT={}
    Production_Calendar=json.loads(Production_Calendar)
    Materials=json.loads(Materials)
    BOM=json.loads(BOM)
    Sales_Order=json.loads(Sales_Order)
    #file_path=Materials['path']
    file_path='application.properties'
    props=Catch_urlpath.Properties(file_path)
    urlpath=props.get('cgi.url')
    #获取当前时间XXXX年XX月XX日 XX时XX分XX秒
    NowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #入参校验
    Sales_Order=checkinput().CheckSales_Order(Sales_Order)
    BOM=checkinput().CheckBOM(BOM)
    Materials=checkinput().CheckMaterials(Materials)
    Production_Calendar=checkinput().CheckProduction_Calendar(Production_Calendar)
    #检查入参是否异常，如果异常直接输出code
    if 'error' in Sales_Order:
        OUTPUT=Sales_Order
        return OUTP
    if 'error' in BOM:
        OUTPUT=BOM
        return OUTPUT
    if 'error' in Materials:
        OUTPUT=Materials
        return OUTPUT
    if 'error' in Production_Calendar:
        OUTPUT=Production_Calendar
        return OUTPUT

    #执行排产
    try:
        L=Input_Parameter_Analysis(Production_Calendar,BOM,Sales_Order,Materials,NowTime,urlpath,OUTPUT)
        #if 1==1:
        #OUTPUT=AlgorithmOptimization(Production_Calendar,BOM,Sales_Order,Materials,NowTime,OUTPUT,urlpath,L)
        #print(OUTPUT)
        #else:
        OUTPUT=calculateplan(Production_Calendar,BOM,Sales_Order,Materials,NowTime,OUTPUT,urlpath,L)
    except Exception as e:
        OUTPUT['error']=500
    if 'error' in OUTPUT and OUTPUT['error']==0:
        OUTPUT={'productionOrder':[]}
    #OUTPUT=json.dumps(OUTPUT)
    return OUTPUT



Materials='{"owner":"I201812210109","path":"/data/websrv/tomcat_production_8130/webapps/ROOT/WEB-INF/classes///application.properties","schedulingId":200002252329,"equipment":[{"calendarModelId":298,"workCenterId":151,"equipmentReplacementIds":[],"equipmentId":200923746044},{"calendarModelId":297,"workCenterId":152,"equipmentReplacementIds":[],"equipmentId":923745653},{"calendarModelId":297,"workCenterId":152,"equipmentReplacementIds":[],"equipmentId":923745637}],"stock":[{"quantity":18.000000,"transit":[{"quantity":72.000000,"transitTime":1550505600000}],"distribution":[{"quantity":72.000000,"distributionTime":1550505600000}],"materialId":2087915272}],"worker":[{"workerId":1141},{"workerId":894,"workCenterId":151},{"workerId":854,"workCenterId":151},{"workerId":817,"workCenterId":154},{"workerId":818,"workCenterId":155},{"workerId":819,"workCenterId":152},{"workerId":820,"workCenterId":157},{"workerId":814,"workCenterId":153},{"workerId":813}],"workCenter":[{"workCenterId":200001781905},{"calendarModelId":297,"workCenterId":151},{"workCenterId":152},{"workCenterId":153},{"workCenterId":154},{"workCenterId":155},{"workCenterId":156},{"workCenterId":150},{"workCenterId":149}]}'


Sales_Order='{"saleOrder":[{"quantity":8000000.000000,"saleOrderLineId":202048474653,"saleOrderId":202048328961,"deliveryDate":1548000000000,"materialId":2087915272,"priority":0}]}'

BOM='{"technologyFlow":[{"materialId":2087915272,"operation":[{"workerIds":[],"workTime":60.0,"transferQuantity":0,"basicQuantity":1.000000,"material":[{"consumptionRate":10.000000,"materialType":"purchase_material","materialId":2087915273,"materialQuantity":10.000000}],"minQuantity":1.000000,"prepareTime":0.5,"workCenterId":151,"equipmentIds":[],"keyCapability":"equipment","operationId":200002121939,"increaseQuantity":1.000000,"scrapRate":20.0}],"technologyId":201930224262}]}'
Production_Calendar='{"productionResource":[{"unavailableTime":[{"beginTime":1553443200000,"endTime":1553529600000}],"equipmentId":923745653},{"unavailableTime":[{"beginTime":1553443200000,"endTime":1553529600000}],"equipmentId":923745637},{"workerId":819,"unavailableTime":[{"beginTime":1553443200000,"endTime":1553529600000},{"beginTime":1553443200000,"endTime":1553529600000},{"beginTime":1553443200000,"endTime":1553529600000},{"beginTime":1553443200000,"endTime":1553529600000},{"beginTime":1553529600000,"endTime":1553594400000}]}]}'

OUTPUT=Scheduling_Plan(Production_Calendar,BOM,Sales_Order,Materials)
print(OUTPUT)
