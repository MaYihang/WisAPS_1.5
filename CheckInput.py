#!/usr/bin/env python
# coding: utf-8
#校验入参类，如果发现异常返回error
import json,copy
class checkinput:
    def CheckMaterials(self,Materials):
        if 'NoKeyCapacity' not in Materials:
            Materials['NoKeyCapacity'] = 0
        if 'owner' not in Materials:
            Materials = {}
            Materials['error'] = 900
            return Materials
        if 'path' not in Materials:
            Materials = {}
            Materials['error'] = 901
            return Materials
        if 'equipment' in Materials:
            for i in range(len(Materials['equipment'])):
                equipmentmaterial = Materials['equipment'][i]
                if 'equipmentId' not in equipmentmaterial:
                    Materials = {}
                    Materials['error'] = 902
                    return Materials
        if 'worker' in Materials:
            for i in range(len(Materials['worker'])):
                workermaterial = Materials['worker'][i]
                if 'workerId' not in workermaterial:
                    Materials = {}
                    Materials['error'] = 903
                    return Materials
        if 'workCenter' in Materials:
            for i in range(len(Materials['workCenter'])):
                workcentermaterial = Materials['workCenter'][i]
                if 'workCenterId' not in workcentermaterial:
                    Materials = {}
                    Materials['error'] = 904
                    return Materials
        return Materials

    def CheckSales_Order(self,Sales_Order):
        for i in range(len(Sales_Order['saleOrder'])):
            saleorder = Sales_Order['saleOrder'][i]

            if 'saleOrderId' not in saleorder:
                Sales_Order = {}
                Sales_Order['error'] = 800
                return Sales_Order

            if 'saleOrderLineId' not in saleorder:
                Sales_Order = {}
                Sales_Order['error'] = 801
                Sales_Order['saleOrderId'] = saleorder['saleOrderId']
                return Sales_Order

            if 'quantity' not in saleorder:
                Sales_Order = {}
                Sales_Order['error'] = 802
                Sales_Order['saleOrderId'] = saleorder['saleOrderId']
                Sales_Order['saleOrderLineId'] = saleorder['saleOrderLineId']
                return Sales_Order

            if 'materialId' not in saleorder:
                Sales_Order = {}
                Sales_Order['error'] = 803
                Sales_Order['saleOrderId'] = saleorder['saleOrderId']
                Sales_Order['saleOrderLineId'] = saleorder['saleOrderLineId']
                return Sales_Order

            if 'priority' not in saleorder:
                Sales_Order = {}
                Sales_Order['error'] = 804
                Sales_Order['saleOrderId'] = saleorder['saleOrderId']
                Sales_Order['saleOrderLineId'] = saleorder['saleOrderLineId']
                return Sales_Order
            Sales_Order['saleOrder'][i] = copy.deepcopy(saleorder)
        return Sales_Order

    def CheckBOM(self,BOM):
        bom = BOM['technologyFlow']
        Materialsid = []
        contnum = 0
        for i in range(len(bom)):
            if 'technologyId' not in bom[i]:
                BOM = {}
                BOM['error'] = 702
                return BOM
            if 'materialId' not in bom[i]:
                BOM = {}
                BOM['error'] = 700
                BOM['technologyId'] = bom[i]['technologyId']
                return BOM
            if 'operation' not in bom[i]:
                BOM = {}
                BOM['technologyId'] = bom[i]['technologyId']
                BOM['error'] = 701
                return BOM
            if 'operation' in bom[i]:
                for j in range(len(bom[i]['operation'])):
                    if 'operationId' not in bom[i]['operation'][j]:
                        BOM = {}
                        BOM['error'] = 703
                        BOM['technologyId'] = bom[i]['technologyId']
                        return BOM
                    if 'workerIds' not in bom[i]['operation'][j]:
                        bom[i]['operation'][j]['workerIds'] = []
                    if 'workTime' not in bom[i]['operation'][j]:
                        bom[i]['operation'][j]['workTime'] = 0.0
                    if 'material' not in bom[i]['operation'][j]:
                        bom[i]['operation'][j]['material'] = []
                    if 'material' in bom[i]['operation'][j]:
                        for z in range(len(bom[i]['operation'][j]['material'])):
                            if bom[i]['operation'][j]['material'][z]['materialId'] not in Materialsid:
                                Materialsid.append(bom[i]['operation'][j]['material'][z]['materialId'])
                            else:
                                bom[i]['operation'][j]['material'][z]['materialId'] = copy.deepcopy(
                                    str(bom[i]['operation'][j]['material'][z]['materialId']) + '#' + str(contnum))
                                Materialsid.append(bom[i]['operation'][j]['material'][z]['materialId'])
                                contnum += 1
                            if 'consumptionRate' not in bom[i]['operation'][j]['material'][z]:
                                bom[i]['operation'][j]['material'][z]['consumptionRate'] = 0.0
                            if 'materialQuantity' not in bom[i]['operation'][j]['material'][z]:
                                bom[i]['operation'][j]['material'][z]['materialQuantity'] = 1.0
                            if 'materialId' not in bom[i]['operation'][j]['material'][z]:
                                BOM = {}
                                BOM['operationId'] = bom[i]['operation'][j]['operationId']
                                BOM['technologyId'] = bom[i]['technologyId']
                                BOM['error'] = 704
                                return BOM
                            if 'materialType' not in bom[i]['operation'][j]['material'][z]:
                                BOM = {}
                                BOM['operationId'] = bom[i]['operation'][j]['operationId']
                                BOM['technologyId'] = bom[i]['technologyId']
                                BOM['materialId'] = bom[i]['operation'][j]['material'][z]['materialId']
                                BOM['error'] = 705
                                return BOM
                    if 'workCenterId' not in bom[i]['operation'][j]:
                        BOM = {}
                        BOM['technologyId'] = bom[i]['technologyId']
                        BOM['operationId'] = bom[i]['operation'][j]['operationId']
                        BOM['error'] = 706
                        return BOM
                    if 'scrapRate' not in bom[i]['operation'][j]:
                        bom[i]['operation'][j]['scrapRate'] = 0.0
                    if 'equipmentIds' not in bom[i]['operation'][j]:
                        bom[i]['operation'][j]['equipmentIds'] = []
                    if 'keyCapability' not in bom[i]['operation'][j]:
                        BOM = {}
                        BOM['technologyId'] = bom[i]['technologyId']
                        BOM['operationId'] = bom[i]['operation'][j]['operationId']
                        BOM['error'] = 707
                        return BOM
        BOM['technologyFlow'] = copy.deepcopy(bom)
        return BOM

    def CheckProduction_Calendar(self,Production_Calendar):
        productioncalendar = Production_Calendar['productionResource']
        for i in range(len(productioncalendar)):
            if 'equipmentId' not in productioncalendar[i] and 'workerId' not in productioncalendar[i]:
                Production_Calendar = {}
                Production_Calendar['error'] = 600
                return Production_Calendar
            else:
                for j in range(len(productioncalendar[i]['unavailableTime'])):
                    if 'beginTime' not in productioncalendar[i]['unavailableTime'][j] or 'endTime' not in \
                            productioncalendar[i]['unavailableTime'][j]:
                        if 'equipmentId' in productioncalendar[i]:
                            equipmentid = productioncalendar[i]['equipmentId']
                            Production_Calendar = {}
                            Production_Calendar['equipmentId'] = equipmentid
                            Production_Calendar['error'] = 601
                            return Production_Calendar
                        elif 'workerId' in productioncalendar[i]:
                            workerid = productioncalendar[i]['workerId']
                            Production_Calendar = {}
                            Production_Calendar['workerId'] = workerid
                            Production_Calendar['error'] = 602
                            return Production_Calendar
        return Production_Calendar
