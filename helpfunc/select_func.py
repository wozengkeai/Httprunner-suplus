# -*- coding: utf-8 -*-
# @Time : 2020/9/24 11:45
# @Author : zengxiaoyan
# @File : select_func.py
# class select_data():
import time
# import numpy as np
import pymysql
db_config ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

db_config1 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

db_config2 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

db_config3 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

db_config4 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

def select_customerId():
    db3 = pymysql.connect(**db_config3)
    cursor3 = db3.cursor()
    sql_customer = 'SELECT customerId FROM customer WHERE companyId = 382 AND `status` = 1 AND isLock = 0 ORDER BY customerId'

    cursor3.execute(sql_customer)
    cusList = []
    news = cursor3.fetchall()
    # print(type(news))
    for cid in news:
        cusList.append(str(cid[0]))
    # print(cusList)
    return cusList

def select_customerName():
    db3 = pymysql.connect(**db_config3)
    cursor3 = db3.cursor()
    sql_name = 'SELECT customerName FROM customer WHERE companyId = 382 AND `status` = 1 AND isLock = 0 ORDER BY customerId'
    nameList = []
    cursor3.execute(sql_name)
    name = cursor3.fetchall()
    for cid in name:
        nameList.append(str(cid[0]))
    customer = [str(id)+str(name) for id,name in zip(cusList,nameList)]
    print(customer)
    return customer
def select_source_data():
    # 客户本年度/同期年度累计业绩

    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = 'SELECT cast(IFNULL(SUM(total),0) as CHAR) FROM sale_source_data WHERE companyId = 382  AND ' \
          'expressDate < "2020-10-01"  AND expressDate >= "2020-01-01" and customerId = '
    # sql_uid = 'SELECT cast(IFNULL(SUM(total),0) as CHAR) FROM sale_source_data WHERE companyId = 382  AND ' \
    #       'expressDate < "2020-10-01"  AND expressDate >= "2020-01-01" and uid = "3252348558521088" and customerId = '
    dataList = []
    for customerId in cusList:
        cursor.execute(sql + customerId)
        data = cursor.fetchall()
        for d in data:
            dataList.append(d[0])
        # print(dataList[0])
    print(dataList)
    data = dict(zip(customer,dataList))
    datanew = sorted(data.items(),key=lambda x:x[1],reverse=True)
    print(datanew)
    db.close()

def select_profit():
    #累计利润

    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql1 = 'SELECT cast(IFNULL(SUM(total),0) AS CHAR)FROM sale_source_data WHERE companyId = 382  AND expressDate < "2020-10-01"  AND expressDate >= "2020-01-01" and customerId = '
    sql2 = "SELECT cast(IFNULL(SUM(saleNum)*2,0) AS CHAR) FROM sale_source_data WHERE   expressDate < '2020-10-01' AND expressDate > '2020-01-01' AND saleTypeId = 1 AND customerId = "
    sql3 = "SELECT IFNULL(SUM(costMoney),0) FROM user_cost WHERE costTime >= '2020-01-01' AND '2020-10-01'> costTime AND customerId = "
    # sql_profit = "select (" + sql1 + customerId + ")-(" + sql2 + customerId +")"
    # print(sql_profit)


    profitList = []
    # profitList = []
    for customerId in cusList:
        cursor.execute("select (" + sql1 + customerId + ")-(" + sql2 + customerId +")-(" + sql3 + customerId + ")")
        data = cursor.fetchall()
        for d in data:
            profitList.append(d[0])
    print(profitList)

    profitdata = dict(zip(customer, profitList))
    profitdata2 = sorted(profitdata.items(),key=lambda x:x[1],reverse=True)
    print(profitdata2)



def get_saleSum(productId,begin,end,districtIds,uid):
    '''
    获取品项销售额
    :return:
    '''
    dpids = districtIds[0]
    # print(dpids)
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(SUM(total)/10000 as CHAR) from sale_source_data  WHERE companyId = 359 AND productId = '%s' AND expressDate >= '%s' " \
          "AND expressDate <= '%s' " %(productId,begin,end)
    sql_gr = "SELECT cast(SUM(total)/10000 as CHAR) from sale_source_data  WHERE companyId = 359 AND productId = '%s' AND expressDate >= '%s' " \
             "AND expressDate <= '%s' and uid = '%s' " %(productId,begin,end,uid)
    sql_qy = "SELECT cast(SUM(total)/10000 as CHAR) from sale_source_data  WHERE companyId = 359 AND productId = '%s' AND expressDate >= '%s' " \
             "AND expressDate <= '%s' and districtPid = '%s'" % (productId, begin, end, dpids)
    #判断是否是公司
    if dpids == 0:
        cursor.execute(sql)
    #登陆账户本人
    elif dpids == -1:
        cursor.execute(sql_gr)
    else:
        cursor.execute(sql_qy)
    saleSum = []
    res = cursor.fetchall()
    for sale in res:
        saleSum.append(sale[0])
    # salesum = format(float(saleSum[0]),'0.2f')
    # salesum = salesum.rstrip('0')
    salesum = round(float(saleSum[0])  ,2)
    # print(type(saleSum))
    return str(salesum)


def get_grossProfitSum(productId,begin,end):
    '''
    获取品项毛利额值
    :param productId:
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql_zy = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice)/10000,0) as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = 359 AND a.perfType = 1 " \
             "AND a.productId = '%s' AND a.saleTypeId = 1 AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.districtPid=b.districtId " \
             "AND a.productId=b.productId AND a.expressDate>=b.startTime AND a.expressDate<=b.endTime  " %(productId,begin,end)
    sql_jh = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice)/10000,0) as CHAR) FROM sale_source_data a ,suplus_customer_test.customer b ,product_price c WHERE a.companyId = 359 " \
             "AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId AND b.serviceAreaPid = c.districtId " \
             "AND c.endTime>=a.expressDate AND a.productId = '%s' AND a.expressDate>=c.startTime AND a.expressDate >= '%s' AND a.expressDate <= '%s'"  %(productId,begin,end)
    cursor.execute(sql_zy)
    profit_zy = cursor.fetchall()
    res_zy = []
    for zy in profit_zy:
        res_zy.append(zy[0])

    cursor.execute(sql_jh)
    profit_jh = cursor.fetchall()
    res_jh = []
    for jh in profit_jh:
        res_jh.append(jh[0])
    grossProfitSum =float(res_zy[0]) + float(res_jh[0])
    grossProfitSum = format(grossProfitSum,'0.2f').rstrip('0')
    return str(grossProfitSum)


def get_saleproduct(districtIds,districtId,uid,listType):
    #销售产品
    if listType == 1:
        dpids = districtId
    else:
        dpids = districtIds[0]
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(count(DISTINCT productId) as CHAR) from sale_source_data  WHERE companyId = 359  AND expressDate >= '2021-01-01' AND expressDate <= '2021-12-31' "
    sql_gr = " SELECT cast(count(DISTINCT productId) as CHAR) from sale_source_data  WHERE companyId = 359  AND expressDate >= '2021-01-01' " \
             "AND expressDate <= '2021-12-31' AND uid = '%s'" % (uid)
    sql_qy = " SELECT cast(count(DISTINCT productId) as CHAR) from sale_source_data  WHERE companyId = 359  AND expressDate >= '2021-01-01' " \
             "AND expressDate <= '2021-12-31' AND districtPid = '%s'" % (dpids)

    if dpids == 0:
        cursor.execute(sql)
    elif dpids == -1:
        cursor.execute(sql_gr)
    else:
        cursor.execute(sql_qy)
    product_count = cursor.fetchall()
    res = []
    for i in product_count:
        res.append(i[0])
    return int(res[0])

def get_mainProductCount(districtId):
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql_qy = " SELECT cast(count(DISTINCT productId) as CHAR) from sale_source_data  WHERE companyId = 359  AND expressDate >= '2021-01-01' " \
             "AND expressDate <= '2021-12-31' AND districtPid = '%s'" % (districtId)
    cursor.execute(sql_qy)
    product_count = cursor.fetchall()
    res = []
    for i in product_count:
        res.append(i[0])
    return int(res[0])

if __name__ == "__main__":

    cusList = select_customerId()
    customer = select_customerName()
    # select_profit()
    # select_source_data()
    # get_saleSum('4110613748842496','2021-01-01','2021-02-01',[185],'3302742697280000')
    # get_grossProfitSum('4092509320986624','2021-01-01','2021-02-01')
    # get_sale_cycle()
    get_saleproduct([-1],'3302742697280000',1)