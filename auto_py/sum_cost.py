# -*- coding: utf-8 -*-
# @Time : 2021/2/25 11:03
# @Author : zengxiaoyan
# @File : sum_cost.py
import pymysql
from auto_py.sum_incrment import get_Increment,get_Pid_total,get_Pid_Increment
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')
chance_ratio = gol.get_value('chance_ratio')
# companyId = 382
# db_config ={"host": "114.55.200.59",
#             "port": 32306,
#             "user": "zengxiaoyan",
#             "password": "zengxiaoyan_12345",
#             "db": "suplus_goal_test",
#             "charset": 'utf8'}
# db_config2 ={"host": "114.55.200.59",
#             "port": 32306,
#             "user": "zengxiaoyan",
#             "password": "zengxiaoyan_12345",
#             "db": "suplus_enterprise_test",
#             "charset": 'utf8'}

def get_usercost(id ,beginTime, endTime):
    '''
    业务员总费用=费用登记+搭赠
    :return:
    '''
    #获取费用登记部分
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtId = '%s' AND costTime >= '%s' " \
          "AND costTime <= '%s'" % (companyId,id, beginTime, endTime)
    cursor.execute(sql)
    sum = cursor.fetchall()
    costList = [i[0] for i in sum]
    cost = costList[0]
    # print(cost)

    #搭赠费用
    # db1 = pymysql.connect(**db_config)
    # cursor1 = db.cursor()
    sql_perf = "SELECT IFNULL(SUM(a.saleNum*b.costPrice),0) FROM sale_source_data a, product_price b WHERE a.companyId = '%s' AND a.saleTypeId != 1 " \
               "AND a.districtId = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'AND a.productId = b.productId " \
               "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND a.districtSaleType != 2 " \
               "AND b.deletedAt is NULL ORDER BY a.id" % (companyId, id, beginTime, endTime)
    cursor.execute(sql_perf)
    sum = cursor.fetchall()
    cost_perfList = [i[0] for i in sum]
    cost_RIperf = cost_perfList[0]

    #区外搭赠费用
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    sql_Outperf = "SELECT IFNULL(SUM(a.saleNum*b.costPrice),0) from sale_source_data a, product_price b,%s.customer c WHERE a.customerId = c.customerId " \
               "AND c.serviceAreaPid = b.districtId AND a.productId = b.productId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                  "AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' " \
                  "AND a.districtSaleType = 2" % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_Outperf)
    sum = cursor.fetchall()
    cost_perfList = [i[0] for i in sum]
    cost_Outperf = cost_perfList[0]

    cost_perf = float(cost_RIperf) + float(cost_Outperf)

    #业务员累计区域费用合计
    user_cost = float(cost) + float(cost_perf)
    print("业务员累计区域费用")
    print(user_cost)

    return  user_cost,cost_perf    #区域费用，搭赠费用

def get_pidcost(pid, beginTime, endTime):
    '''
    大区经理的区域费用总计
    费用总计=∑(辖区所有片区的费用总计）+大区经理自己的费用总计
    :return:
    '''
    #经理个人费用登记
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(IFNULL(SUM(costMoney),0)as CHAR) FROM user_cost WHERE companyId = '%s' AND districtPid = '%s' AND districtId = 0 AND costTime >= '%s' " \
          "AND costTime <= '%s'" % (companyId, pid, beginTime, endTime)
    cursor.execute(sql)
    sum = cursor.fetchall()
    costList = [i[0] for i in sum]
    cost = costList[0]

    # 经理个人搭赠费用
    # db1 = pymysql.connect(**db_config)
    # cursor1 = db1.cursor()
    sql_RIperf = "SELECT cast(IFNULL(SUM(a.saleNum*b.costPrice),0) as CHAR) FROM sale_source_data a, product_price b WHERE a.companyId = '%s' AND a.saleTypeId != 1 " \
               "AND a.districtPid = '%s' AND a.districtId = 0 AND a.expressDate >= '%s' AND a.expressDate <= '%s'AND a.productId = b.productId " \
               "AND a.districtPid=b.districtId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND a.districtSaleType != 2 " \
               "AND b.deletedAt is NULL " % (companyId, pid, beginTime, endTime)
    cursor.execute(sql_RIperf)
    sum = cursor.fetchall()
    cost_perfList = [i[0] for i in sum]
    cost_RIperf = cost_perfList[0]
    # print(type(cost_perf))

    #经理区外搭赠费用
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    sql_Outperf = "SELECT cast(IFNULL(SUM(a.saleNum*b.costPrice),0) as CHAR) FROM sale_source_data a, product_price b,%s.customer c " \
                  "WHERE a.customerId = c.customerId AND c.serviceAreaPid = b.districtId AND a.productId = b.productId AND a.expressDate >= b.startTime " \
                  "AND a.expressDate <= b.endTime AND b.deletedAt is NULL AND a.companyId = %s AND a.saleTypeId != 1 AND a.districtPid = '%s' AND a.districtId = 0 " \
                  "AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.districtSaleType = 2 " \
                 "AND b.deletedAt is NULL " % (customer,companyId, pid, beginTime, endTime)
    cursor.execute(sql_Outperf)
    sum = cursor.fetchall()
    cost_perfList = [i[0] for i in sum]
    cost_Outperf = cost_perfList[0]

    cost_perf = float(cost_RIperf) + float(cost_Outperf)


    #遍历底下业务员费用
    db2 = pymysql.connect(**db_config2)
    cursor2 = db2.cursor()
    sql_id = "SELECT cast(id as CHAR) FROM cfg_district WHERE parent_id = %s" % (pid)
    cursor2.execute(sql_id)
    id = cursor2.fetchall()
    user_cost = 0
    if id:
        list = [i[0] for i in id]
        # user_cost = 0
        for id in list:
            id_cost = get_usercost(id,beginTime,endTime)
            user_cost = user_cost + id_cost[0]

    #大区经理累计区域总费用
    pid_cost =float(cost) + float(cost_perf) + user_cost
    print("区域经理累计区域总费用")
    print(pid_cost)
    return pid_cost,cost_perf   #区域费用，搭赠费用

def get_costRate(id ,beginTime, endTime):
    '''
    业务员累计区域费用率=累计区域费用/累计区域业绩
    :return:
    '''
    user_cost = get_usercost(id ,beginTime, endTime)
    user_increment = get_Increment(id ,beginTime, endTime)[4]
    # print(type(user_increment))
    if user_increment != 0:
        # costRate = round(user_cost / user_increment,4)
        costRate = user_cost[0] / user_increment
        print("业务员累计区域费用率")
        print(round(costRate,4))
    else:
        costRate = 0
        print("-")
    return costRate

def get_pid_costRate(pid ,beginTime, endTime):
    '''
    大区经理的累计区域费用率=（大区经理的费用总计÷大区经理的区域业绩）
    :return:
    '''
    pid_cost = get_pidcost(pid ,beginTime, endTime)
    pid_increment = get_Pid_total(pid ,beginTime, endTime)[0]
    if pid_increment != 0:
        pid_costRate = pid_cost[0] / pid_increment
        print("大区经理累计区域费用率")
        print(round(pid_costRate,5))
    else:
        pid_costRate = 0
        print("大区经理累计区域费用率  -")
    return pid_costRate


def get_personcost(id ,beginTime, endTime):
    '''
    业务员累计个人总费用=区域费用+区外合作业绩×区域费用率-∑（区内合作订单业绩-区内合作业绩）×区域费用率  √

    :return:
    '''
    #业务员个人业绩
    personTotal = get_Increment(id ,beginTime, endTime)[3]

    #业务员区域费用率
    costRate = get_costRate(id ,beginTime, endTime)
    if costRate == '-':
        costRate = 0

    usercost = get_usercost(id ,beginTime, endTime)
    increment = get_Increment(id ,beginTime, endTime)
    chanceOut = increment[2]
    chanceInall = increment[5]
    chanceIn = increment[1]
    personCost = usercost[0] + float(chanceOut) * costRate - (float(chanceInall) - float(chanceIn)) * costRate
    print("业务员累计个人总费用")
    print(personCost)
    return personCost

def get_pid_personcost(pid ,beginTime, endTime):
    '''
    大区经理累计个人总费用 =区域费用+∑业务员区外合作业绩×系数+区外合作业绩×区域费用率-∑（区内合作订单业绩-区内合作业绩）×区域费用率  √
    :param pid:
    :param beginTime:
    :param endTime:
    :return:
    '''
    #大区经理个人业绩
    personTotal = get_Pid_total(pid ,beginTime, endTime)[1]

    #遍历二级区域获取区外分成业绩
    db2 = pymysql.connect(**db_config2)
    cursor2 = db2.cursor()
    sql_id = "SELECT cast(id as CHAR) FROM cfg_district WHERE parent_id = %s" % (pid)
    cursor2.execute(sql_id)
    id = cursor2.fetchall()
    chanceOutPerf = 0
    chanceInAllPerf = 0
    chanceInPerf = 0
    if id:
        list = [i[0] for i in id]
        # user_cost = 0
        for id in list:
            performence = get_Increment(id,beginTime, endTime)
            chanceOutPerf = chanceOutPerf + float(performence[2])
            chanceInAllPerf = chanceInAllPerf + float(performence[5])
            chanceInPerf = chanceInPerf + float(performence[1])

    #大区经理区域费用率
    costRate = get_pid_costRate(pid ,beginTime, endTime)
    if costRate == '-':
        costRate = 0
    pid_cost = get_pidcost(pid ,beginTime, endTime)
    pid_incrment = get_Pid_Increment(pid ,beginTime, endTime)
    pid_chanceOut = pid_incrment[2]
    pid_chanceInall = pid_incrment[3]
    pid_chanceIn = pid_incrment[1]
    pid_personCost = pid_cost[0] + float(chanceOutPerf) * chance_ratio * costRate + float(pid_chanceOut) * costRate - (float(pid_chanceInall) - float(pid_chanceIn)) * costRate - (float(chanceInAllPerf) - float(chanceInPerf)) * costRate
    print("大区经理累计个人总费用")
    print(pid_personCost)
    return pid_personCost

def companyCost(beginTime, endTime):
    '''
    公司区域费用= 所有大区区域费用总和
    :return:
    '''
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    companyCost = 0
    if pid:
        list = [i[0] for i in pid]
        for pid in list:
            cost = get_pidcost(pid,beginTime, endTime)
            companyCost = companyCost + cost[0]
    print("公司费用")
    print(companyCost)
    return companyCost

if __name__ == "__main__":
    #业务员累计区域费用
    # get_usercost(178,'2020-01-01','2020-12-31')

    #大区经理累计区域费用
    # get_pidcost(177, '2021-01-01', '2021-01-31')

    # 业务员累计区域费用率
    # get_costRate(178,'2021-01-01', '2021-01-31')

    # 大区经理累计区域费用率
    # get_pid_costRate(37, '2021-03-01', '2021-03-05')

    #累计业务员个人总费用
    # get_personcost(178,'2021-01-01', '2021-03-04')

    # 累计大区经理个人总费用
    get_pid_personcost(37, '2021-03-01', '2021-03-05')

    #公司费用
    # companyCost('2021-03-01', '2021-03-04')