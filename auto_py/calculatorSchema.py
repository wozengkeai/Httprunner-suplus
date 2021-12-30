# -*- coding: utf-8 -*-
# @Time : 2021/7/2 17:03
# @Author : zengxiaoyan
# @File : calculatorSchema.py
'''
计划方案内数据统计
'''
import pymysql
import jmespath
import ast,json
from auto_py import gol,config
db_config = gol.get_value('db_config')
companyId = gol.get_value('companyId')
def schema(districtId,districtPid,year,month):
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(schemeContent as CHAR) FROM scheme WHERE companyId = %s AND districtPid = %s AND districtId = %s " \
          "AND `year` = %s AND `month` = %s and id = 274" \
          % (companyId,districtPid,districtId,year,month)
    sql_Pid = "SELECT schemeContent FROM scheme WHERE companyId = %s AND districtPid = %s AND `year` = %s AND `month` = %s" % (
    companyId,districtPid,year,month)
    if districtId == 0 and districtPid != 0:
        cursor.execute(sql_Pid)
    else:
        cursor.execute(sql)
    schemeData = cursor.fetchall()
    schemaList = []
    for i in schemeData:
        i = list(i)
        schemaList.append(i[0])
    # print(schemaList)

    schemaList = [json.loads(i) for i in schemaList]
    print(schemaList)
    # currentSale = jmespath.search('currentSale', schemaList)
    currentSaleSum = 0
    currentProfitSum = 0
    saleIncrementSum = 0
    for i in schemaList:
        currentSale = jmespath.search('currentSale',i)
        currentProfit = jmespath.search('currentProfit',i)
        saleIncrement = jmespath.search('sales[*].products[*].saleIncrement',i)
        print(saleIncrement)
        # print(currentSale)
        currentSaleSum = float(currentSale) + currentSaleSum  #模拟业绩
        currentProfitSum = float(currentProfit) + currentProfitSum   #计划利润
        # saleIncrementSum = saleIncrementSum + float(saleIncrement)
    currentProfitRatio = currentProfitSum / currentSaleSum    #计划利润率


if __name__ == "__main__":
    schema(178,177,2021,6)