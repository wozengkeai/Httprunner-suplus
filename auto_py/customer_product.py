# -*- coding: utf-8 -*-
# @Time : 2021/4/19 17:20
# @Author : zengxiaoyan
# @File : customer_product.py
'''
0.10.0版本业绩小工具
客户的品项计算
某一区域内某一客户的所有品项
'''

import pymysql
from auto_py.sum_cost import get_usercost,get_pidcost
from auto_py.customer_sumCost import customerCost,customerGift
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')

def customerProduct(customerId,beginTime,endTime,districtId,districtPid,uid):
    '''
    某区域客户卖过的产品列表
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT productId,productName ,cast(SUM(saleNum) as CHAR ),cast(MAX(salePrice) as CHAR ) FROM sale_source_data WHERE companyId = %s " \
          "AND customerId = '%s' AND expressDate >= '%s' AND expressDate <= '%s' and districtId = %s and saleTypeId = 1 AND uid = %s GROUP BY productId" \
          % (companyId,customerId,beginTime,endTime,districtId,uid)
    sqlP = "SELECT productId,productName ,cast(SUM(saleNum) as CHAR ),cast(MAX(salePrice) as CHAR ) FROM sale_source_data WHERE companyId = %s " \
           "AND customerId = '%s' AND expressDate >= '%s' AND expressDate <= '%s' and districtPid = %s and saleTypeId = 1 AND uid = %s GROUP BY productId" \
          % (companyId,customerId,beginTime,endTime,districtPid,uid)
    if districtId == 0:
        sql = sqlP  #一级区域
    else:
        sql = sql
    productList = []
    cursor.execute(sql)
    productData = cursor.fetchall()
    for i in productData:
        productList.append(i)
    print(productList)
    return productList

def costprice(districtPid,productId,nowDate):
    '''
    产品成本：登录用户所在区域当前月份的产品结算成本
    成本取筛选器的时间成本，不是当前实际时间！！
    :param districtPid:
    :param productId:
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql_price = "SELECT cast(IFNUll(costPrice,0) as CHAR ) FROM product_price WHERE districtId = %s and productId = '%s' " \
                "AND  startTime <= '%s' AND endTime >= '%s'  AND deletedAt is NULL " % (districtPid, productId,nowDate,nowDate)
    cursor.execute(sql_price)
    priceList = []
    priceData = cursor.fetchall()
    for i in priceData:
        priceList.append(i)
    if priceList:
        cost_price = float(priceList[0][0])
    else:
        cost_price = '-'
    print(cost_price)

    return cost_price


def grossProfitRate(districtPid,productId,salePrice,nowDate):
    '''
    根据数量和售价实时计算毛利率，成本由数据库而来
    成本：登录用户所在区域当前月份的产品结算成本
    计算公式=（销售价格-结算成本）/销售价格
    :return:
    '''
    cost_price = costprice(districtPid,productId,nowDate)
    if cost_price == '-':
        grossProfitRate = '-'
    else:
        grossProfitRate = (salePrice - float(cost_price)) / salePrice *100
    print(grossProfitRate)


def customerPerf(customerId,beginTime,endTime,districtId,districtPid,nowDate,uid):
    '''
    单客户业绩/利润合计
    某一客户的产品业绩之和=销售数量*售价
    同期：单个客户的利润总和=正常销售数量*（售价-成本）-变动费用
    模拟：单个客户的利润总和=正常销售数量*（售价-成本）-促销费用-搭赠费用-变动费用
    :return:
    :districtPid:
    :districtId: 为0时代表一级区域
    '''
    productList = customerProduct(customerId,beginTime,endTime,districtId,districtPid,uid)

    #搭赠费用
    usercost = customerGift(districtId,districtPid,beginTime,endTime,customerId,uid,nowDate)
    giftCost = usercost


    #变动费用
    changeCost = customerCost(customerId,beginTime,endTime,2,uid)
    productPerf = 0
    productProfit = 0
    for i in productList:
        productPerf = productPerf + float(i[2])*float(i[3])    #数量*售价
        userPrice = costprice(districtPid,i[0],nowDate)
        if userPrice != '-':
            productProfit = productProfit + float(i[2]) * (float(i[3]) - float(userPrice))  #数量*(售价-成本)
        else:
            productProfit = productProfit

    #同期单客户利润总和
    customerGrossP = productProfit  - float(changeCost) - float(giftCost)

    print("客户端单客户业绩合计")
    print(productPerf)
    print("客户端单客户利润合计")
    print(customerGrossP)


    return productPerf,customerGrossP


def virtualGift(districtPid,productId,giftNum,nowDate):
    '''
    虚拟搭赠费用=虚拟搭赠数量*成本
    :return:
    '''
    #搭赠成本
    giftCostPrice = costprice(districtPid,productId,nowDate)
    #单产品虚拟搭赠费用
    virtualGiftCost = giftNum * giftCostPrice

    print(virtualGiftCost)

def customerSt(customerId,beginTime,endTime,districtId,districtPid,uid,nowDate):
    '''
    同期业绩、利润
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    sql_salesman = "SELECT CAST(IFNULL(SUM(total),0) AS char) FROM sale_source_data WHERE districtId = %s AND uid = '%s' AND expressDate >= '%s' " \
                   "AND expressDate <= '%s' AND customerId = '%s'" % (districtId,uid,beginTime,endTime,customerId)

    sql_salesman_noC = "SELECT CAST(IFNULL(SUM(total),0) AS char) FROM sale_source_data WHERE districtId = %s AND uid = '%s' AND expressDate >= '%s' " \
                   "AND expressDate <= '%s' " % (districtId, uid, beginTime, endTime)

    sql_manage = "SELECT CAST(IFNULL(SUM(total),0) AS char) FROM sale_source_data WHERE districtPid = %s AND uid = '%s' AND expressDate >= '%s' " \
                   "AND expressDate <= '%s' AND customerId = '%s'" % (districtPid, uid, beginTime, endTime, customerId)

    sql_manage_noC = "SELECT CAST(IFNULL(SUM(total),0) AS char) FROM sale_source_data WHERE districtPid = %s AND uid = '%s' AND expressDate >= '%s' " \
                 "AND expressDate <= '%s' " % (districtPid, uid, beginTime, endTime)

    # 自营毛利额
    sql_regular_salesman = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
          "AND a.saleTypeId = 1 AND a.districtId = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId " \
          "AND a.productId=b.productId AND '%s'>=b.startTime AND '%s'<=b.endTime and a.customerId = %s and a.uid = %s AND b.deletedAt is null" % (
          companyId, districtId, beginTime, endTime,nowDate,nowDate,customerId,uid)

    sql_regular_salesman_noC = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
          "AND a.saleTypeId = 1 AND a.districtId = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId and a.uid = %s " \
          "AND a.productId=b.productId AND '%s'>=b.startTime AND '%s'<=b.endTime AND b.deletedAt is null" % (
          companyId, districtId, beginTime, endTime,uid,nowDate,nowDate)

    sql_regular_manage = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
          "AND a.saleTypeId = 1 AND a.districtId = 0 AND a.districtPid = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId " \
          "AND a.productId=b.productId AND '%s'>=b.startTime AND '%s'<=b.endTime and a.uid = %s and a.customerId = %s AND b.deletedAt is null" % (
          companyId, districtPid, beginTime, endTime,nowDate,nowDate,uid,customerId)

    sql_regular_manage_noC = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
                         "AND a.saleTypeId = 1 AND a.districtId = 0 AND a.districtPid = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId " \
                         "AND a.productId=b.productId AND '%s'>=b.startTime AND '%s'<=b.endTime and a.uid = %s AND b.deletedAt is null" % (
                             companyId, districtPid, beginTime, endTime,nowDate,nowDate, uid)

    #机会毛利额
    sql_chance_salesman = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                 "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                 "AND b.serviceAreaPid = c.districtId AND c.endTime>='%s' AND '%s'>=c.startTime  AND a.districtId = '%s' " \
                 "AND a.expressDate >= '%s' AND a.expressDate <= '%s' and a.customerId = %s  AND c.deletedAt is null" \
                          % (customer,companyId,nowDate,nowDate, districtId, beginTime, endTime,customerId)

    sql_chance_salesman_noC = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                 "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                 "AND b.serviceAreaPid = c.districtId AND c.endTime>='%s' AND '%s'>=c.startTime  AND a.districtId = '%s' " \
                 "AND a.expressDate >= '%s' AND a.expressDate <= '%s' and c.deletedAt is null  " % (customer,companyId, nowDate,nowDate,districtId, beginTime, endTime)

    sql_chance_manage =  "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                 "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                 "AND b.serviceAreaPid = c.districtId AND c.endTime>='%s' AND '%s'>=c.startTime AND a.districtId = 0 AND a.districtPid = '%s' " \
                 "AND a.expressDate >= '%s' AND a.expressDate <= '%s' and a.customerId = %s AND c.deletedAt is null " \
                         % (customer,companyId, nowDate,nowDate,districtPid, beginTime, endTime,customerId)

    sql_chance_manage_noC = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                 "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                 "AND b.serviceAreaPid = c.districtId AND c.endTime>='%s' AND '%s'>=c.startTime AND a.districtId = 0 AND a.districtPid = '%s' " \
                 "AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND c.deletedAt is null  " % (customer,companyId,nowDate,nowDate, districtPid, beginTime, endTime)


    if districtId == 0:
        #一级区域
        if customerId == 0:
            #noCustomer代表整个区域，不区分单客户
            sql = sql_manage_noC
            sql_regular = sql_regular_manage_noC
            sql_chance = sql_chance_manage_noC

        else:
            sql = sql_manage
            sql_regular = sql_regular_manage
            sql_chance = sql_chance_manage

    else:
        # 二级业务员
        if customerId == 0:
            sql = sql_salesman_noC #业绩
            sql_regular = sql_regular_salesman_noC  #自营毛利额
            sql_chance = sql_chance_salesman_noC  #机会毛利额
        else:
            sql = sql_salesman
            sql_regular = sql_regular_salesman
            sql_chance = sql_chance_salesman
    #业绩
    cursor.execute(sql)
    perfsum = cursor.fetchall()
    perfData = [i[0] for i in perfsum]

    #自营毛利额
    cursor.execute(sql_regular)
    regularsum = cursor.fetchall()
    regularData = [i[0] for i in regularsum]

    # 机会毛利额
    cursor.execute(sql_chance)
    chancesum = cursor.fetchall()
    chanceData = [i[0] for i in chancesum]

    #变动费用
    changeCost = customerCost(customerId, beginTime, endTime, 2, uid)
    #固定费用
    fixCost = customerCost(customerId, beginTime, endTime, 1, uid)
    #搭赠费用
    usercost = customerGift(districtId, districtPid, beginTime, endTime, customerId, uid, nowDate)
    giftCost = usercost


    if customerId == 0:   #总合计
        #同期利润=正常销售数量*（售价-成本）-变动费用-固定费用-搭赠费用=自营毛利额+机会毛利额-变动费用-固定费用-搭赠费用
        profit = float(regularData[0]) + float(chanceData[0]) - float(fixCost) - float(changeCost) - float(giftCost)
        print("客户同期总业绩")
        print(perfData[0])

        print("客户同期总利润")
        print(profit)

    else:
        profit = float(regularData[0]) + float(chanceData[0])  - float(changeCost) - float(giftCost)
        print("单客户同期业绩")
        print(perfData[0])
        print("客户同期利润")
        print(profit)

    return perfData[0],profit






if __name__ == "__main__":
    #某客户的产品列表
    # customerProduct('3668350661771264','2020-04-01','2020-04-30',0,37,'3247228580405760')

    #计算毛利率districtPid,productId,salePrice
    # grossProfitRate(25,'3659694170161152',95,'2021-04-07')

    #某一客户的所有产品总和 customerId,beginTime,endTime,districtId,districtPid,nowDate,uid
    # customerPerf('3659680461586432','2020-04-01','2020-04-30',26,25,'2021-04-13','3246374275117568')

    #虚拟搭赠费用
    # virtualGift(177,'',200,'2021-04-29')

    # costprice(25,'3659694170161152','2021-04-14')

    #同期数据customerId,beginTime,endTime,districtId,districtPid,uid,nowDate
    customerSt(0,'2020-05-01','2020-05-31',0,37,'3247228580405760','2021-06-08')