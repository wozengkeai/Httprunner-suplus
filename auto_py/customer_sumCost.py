# -*- coding: utf-8 -*-
# @Time : 2021/4/20 16:19
# @Author : zengxiaoyan
# @File : customer_sumCost.py
'''
客户的费用统计
'''
import pymysql
# from auto_py.customer_product import costprice

from auto_py import gol,config
db_config = gol.get_value('db_config')
companyId = gol.get_value('companyId')

def customerCost(customerId,beginTime,endTime,valueType,uid):
    '''
    客户固定费用
    :return:
    valueType: 1 固定，2 变动
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    if db_config['db'] == "suplus_goal_preonline":
        salary = "suplus_salary_preonline"
    elif db_config['db'] == "suplus_goal":
        salary = "suplus_salary"
    else:
        salary = "suplus_salary_test"
    sql_change = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost a,%s.cfg_subject b WHERE a.costId = b.id " \
          "AND b.value_Type = %s AND a.customerId = '%s' AND costTime BETWEEN '%s' AND '%s' AND uid = '%s' AND a.costId NOT in (13,30)" \
          % (salary,valueType,customerId,beginTime,endTime,uid)
    sql_change_noC = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost a,%s.cfg_subject b WHERE a.costId = b.id " \
                 "AND b.value_Type = %s  AND costTime BETWEEN '%s' AND '%s' AND uid = '%s' AND a.costId NOT in (13,30)" \
                 % (salary, valueType,  beginTime, endTime, uid)

    #搭赠费用另外统计
    sql_fix = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost a,%s.cfg_subject b WHERE a.costId = b.id " \
          "AND b.value_Type = %s  AND costTime BETWEEN '%s' AND '%s' AND uid = '%s' AND a.costId NOT in (13,30)" \
          % (salary,valueType,  beginTime, endTime, uid)

    if valueType == 1:
        sql = sql_fix
    else:
        if customerId == 0:
            sql = sql_change_noC
        else:
            sql = sql_change
    cursor.execute(sql)
    costData = cursor.fetchall()
    costList = list(costData)

    userCost = costList[0][0]
    print(userCost)

    return userCost

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
    # print(costPrice)

    return cost_price

def customerGift(districtId,districtPid,beginTime,endTime,customerId,uid,nowdate):
    '''
    客户的搭赠费用
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()

    #个人登记搭赠
    sql_register_salesman = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtId = '%s' " \
                            "AND costTime >= '%s' AND costTime <= '%s' AND customerId = %s and uid = %s AND costId in (13,30,29)" \
                            % (companyId,districtId, beginTime, endTime,customerId,uid)
    sql_register_salesman_noC = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtId = '%s' " \
                            "AND costTime >= '%s' AND costTime <= '%s'  and uid = %s AND costId in (13,30,29)" \
                            % (companyId, districtId, beginTime, endTime,  uid)
    sql_register_manage = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtId = 0 " \
                            "AND districtPid = %s AND costTime >= '%s' AND costTime <= '%s' AND customerId = %s and uid = %s AND costId in (13,30,29)" \
                          % (companyId,districtPid, beginTime, endTime,customerId,uid)
    sql_register_manage_noC = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtId = 0 " \
                          "AND districtPid = %s AND costTime >= '%s' AND costTime <= '%s'  and uid = %s AND costId in (13,30,29)" \
                          % (companyId, districtPid, beginTime, endTime,  uid)
    #区内搭赠
    sql_in_salesman = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b WHERE a.companyId = %s " \
                      "AND a.saleTypeId != 1 AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' " \
                      "AND a.districtSaleType != 2 AND a.districtSaleType != 2 AND a.uid = '%s' AND a.productId = b.productId " \
                      "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND customerId = %s " \
                      "AND b.deletedAt is NULL ORDER BY a.id" %(companyId,districtId,beginTime,endTime,uid,customerId)

    sql_in_salesman_noC = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b WHERE a.companyId = %s " \
                      "AND a.saleTypeId != 1 AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' " \
                      "AND a.districtSaleType != 2 AND a.districtSaleType != 2 AND a.uid = '%s' AND a.productId = b.productId " \
                      "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime  " \
                      "AND b.deletedAt is NULL ORDER BY a.id" % (
                      companyId, districtId, beginTime, endTime, uid)

    sql_in_manage = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b WHERE a.companyId = %s " \
                      "AND a.saleTypeId != 1 AND a.districtId = 0 AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' " \
                      "AND a.districtSaleType != 2 AND a.districtSaleType != 2 AND a.uid = '%s' AND a.productId = b.productId " \
                      "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND customerId = %s " \
                      "AND b.deletedAt is NULL ORDER BY a.id" % (companyId, districtPid, beginTime, endTime, uid,customerId)

    sql_in_manage_noC = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b WHERE a.companyId = %s " \
                    "AND a.saleTypeId != 1 AND a.districtId = 0 AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' " \
                    "AND a.districtSaleType != 2 AND a.districtSaleType != 2 AND a.uid = '%s' AND a.productId = b.productId " \
                    "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime  " \
                    "AND b.deletedAt is NULL ORDER BY a.id" % (
                    companyId, districtPid, beginTime, endTime, uid)


    #区外搭赠
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    sql_out_salesman = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b," \
                       "%s.customer c WHERE a.customerId = c.customerId AND c.serviceAreaPid = b.districtId  AND a.customerId = %s " \
                       "AND a.productId = b.productId AND a.districtSaleType = 2 AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                       "AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtId = %s  AND a.expressDate >= '%s' " \
                       "AND a.expressDate <= '%s' AND a.uid = '%s'" % (customer,customerId,companyId,districtId,beginTime,endTime,uid)

    sql_out_salesman_noC = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b," \
                       "%s.customer c WHERE a.customerId = c.customerId AND c.serviceAreaPid = b.districtId   " \
                       "AND a.productId = b.productId AND a.districtSaleType = 2 AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                       "AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtId = %s  AND a.expressDate >= '%s' " \
                       "AND a.expressDate <= '%s' AND a.uid = '%s'" % (
                       customer,  companyId, districtId, beginTime, endTime, uid)

    sql_out_manage = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b," \
                     "%s.customer c WHERE a.customerId = c.customerId AND c.serviceAreaPid = b.districtId AND a.customerId = %s " \
                     "AND a.productId = b.productId AND a.districtSaleType = 2 AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                     "AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtId = 0 and a.districtPid = '%s'  " \
                     "AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.uid = '%s'" % (customer,customerId,companyId, districtPid, beginTime, endTime, uid)

    sql_out_manage_noC = "SELECT cast(IFNULL(a.saleNum,0) as CHAR),b.districtId,b.productId FROM sale_source_data a, product_price b," \
                     "%s.customer c WHERE a.customerId = c.customerId AND c.serviceAreaPid = b.districtId  " \
                     "AND a.productId = b.productId AND a.districtSaleType = 2 AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                     "AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtId = 0 and a.districtPid = '%s'  " \
                     "AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.uid = '%s'" % (
                     customer,  companyId, districtPid, beginTime, endTime, uid)

    if districtId != 0:
        #业务员
        if customerId == 0:
            #无客户，整个区域
            sql_register = sql_register_salesman_noC
            sql_in = sql_in_salesman_noC
            sql_out = sql_out_salesman_noC
        else:
            sql_register = sql_register_salesman
            sql_in = sql_in_salesman
            sql_out = sql_out_salesman

    else:
        #一级区域
        if customerId == 0:
            sql_register = sql_register_manage_noC
            sql_in = sql_in_manage_noC
            sql_out = sql_out_manage_noC
        else:
            sql_register = sql_register_manage
            sql_in = sql_in_manage
            sql_out = sql_out_manage

    #登记搭赠
    cursor.execute(sql_register)
    registerDataList = cursor.fetchall()
    registerData = [i[0] for i in registerDataList]
    print(registerData)

    #区内搭赠
    cursor.execute(sql_in)
    inDataList = cursor.fetchall()
    inData = [i for i in inDataList]
    print(inData)
    inCost = 0
    for i in inData:
        num = i[0]
        price_districtPid = i[1]
        productId = i[2]
        cost_price = costprice(price_districtPid,productId,nowdate)
        if cost_price != '-':
            inCost = inCost + float(num) * float(cost_price)

    #区外搭赠
    cursor.execute(sql_out)
    outDataList = cursor.fetchall()
    outData = [i for i in outDataList]
    print(outData)
    outCost = 0
    for j in outData:
        num = j[0]
        price_districtPid = j[1]
        productId = j[2]
        cost_price = costprice(price_districtPid, productId, nowdate)
        if cost_price != '-':
            outCost = outCost + float(num) * float(cost_price)


    #搭赠总费用
    giftCost = float(registerData[0]) + float(inCost) + float(outCost)
    print("搭赠总费用")
    print(giftCost)

    return giftCost

# def customerCost(customerId,districtId,districtPid,beginTime,endTime):
#     '''
#     某区域客户的搭赠费用
#     :param customerId:
#     :param districtId:
#     :param districtPid:
#     :param beginTime:
#     :param endTime:
#     :return:
#     '''
#     db = pymysql.connect(**db_config)
#     cursor = db.cursor()
#     sql_user = "SELECT * FROM cast (IFNULL(user_cost,0) as CHAR) WHERE companyId = %s AND districtId = %s AND costTime >= '%s' " \
#           "AND costTime <= '%s' AND customerId = '%s'" % (companyId,districtId,beginTime,endTime,customerId)
#     sql_manage = "SELECT * FROM cast (IFNULL(user_cost,0) as CHAR) WHERE companyId = %s AND districtPid = %s AND costTime >= '%s' " \
#           "AND costTime <= '%s' AND customerId = '%s'" % (companyId,districtPid,beginTime,endTime,customerId)
#     if districtId == 0:
#         sql = sql_manage
#     else:
#         sql = sql_user


if __name__ == "__main__":
    #客户登记费用-不包含搭赠
    # customerCost('3946559539544064','2020-05-01','2020-05-31',2,'3259949165191936')

    #客户搭赠费用 districtId,districtPid,beginTime,endTime,customerId,uid,nowdate
    customerGift(0,96,'2020-05-01','2020-05-31','3668350665900032','3247228580772352','2021-05-13')
