# -*- coding: utf-8 -*-
# @Time : 2021/2/24 15:11
# @Author : zengxiaoyan
# @File : sum_incrment.py
import pymysql,json
from auto_py.sum_correspond import get_resSale
import datetime
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')
chance_ratio = gol.get_value('chance_ratio')
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
# companyId = 382
#
# chance_ratio = 0.3
def get_Increment(id,beginTime,endTime):
    '''
    业务员
    个人业绩=自营业绩+区内合作业绩+区外合作业绩
    区域业绩=∑(自营业绩+区内合作订单业绩）
    常规业绩，机会业绩,个人总业绩
    :return:
    '''
    #自营业绩
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql_routine = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 1 AND expressDate >= '%s' " \
          "AND expressDate <= '%s' AND districtId = %s " %(companyId,beginTime,endTime,id)
    cursor.execute(sql_routine)
    sum = cursor.fetchall()
    list = []
    for i in sum:
        list.append(i[0])
    routineIncrement = list[0]
    print("自营业绩")
    print(routineIncrement)

    #机会区内业绩
    # cursor1 = db.cursor()
    sql_chance1 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
          "AND districtSaleType = 1 AND expressDate <= '%s' AND districtId = %s " %(companyId,beginTime,endTime,id)
    cursor.execute(sql_chance1)
    sumChance = cursor.fetchall()
    if sumChance:
        list = []
        for i in sumChance:
            list.append(i[0])
        chanceIncrement = list[0]
    else:
        chanceIncrement = 0
    print("机会区内业绩")
    print(chanceIncrement)

    # 机会区外业绩
    # cursor2 = db.cursor()
    sql_chance2 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
                  "AND districtSaleType = 2 AND expressDate <= '%s' AND districtId = %s " % (companyId,beginTime, endTime,id)
    cursor.execute(sql_chance2)
    sumChance2 = cursor.fetchall()
    if sumChance2:
        list = []
        for i in sumChance2:
            list.append(i[0])
        chanceIncrement2 = list[0]

    else:
        chanceIncrement2 = 0
    print("机会区外业绩")
    print(chanceIncrement2)


    #区内机会业绩整单
    # cursor3 = db.cursor()
    sql_chance3 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE expressNo in (SELECT expressNo FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 " \
                  "AND perfType = 2 AND expressDate >= '%s' AND expressDate <= '%s' AND districtId = %s AND districtSaleType = 1)" % (companyId,beginTime, endTime,id)
    cursor.execute(sql_chance3)
    sumChance3 = cursor.fetchall()
    if sumChance3:
        list = []
        for i in sumChance3:
            list.append(i[0])
        chanceIncrement3 = list[0]
    else:
        chanceIncrement3 = 0
    # print(chanceIncrement3)


    #个人业绩
    total = float(routineIncrement) + float(chanceIncrement) + float(chanceIncrement2)
    print("个人总业绩")
    print(total)

    #区域业绩
    distotal = float(routineIncrement) + float(chanceIncrement3)
    print("区域业绩")
    print(distotal)

    # #增量业绩
    # correspond_sale = get_resSale()
    return routineIncrement,chanceIncrement,chanceIncrement2,total,distotal,chanceIncrement3

def get_Pid_Increment(pid,beginTime, endTime):
    '''
    区域经理
    :return:
    '''
    #经理个人自营
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql_routine = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 1 AND expressDate >= '%s' " \
                  "AND expressDate <= '%s' AND districtId = 0 and districtPid = %s " % (companyId,beginTime, endTime,pid)
    cursor.execute(sql_routine)
    sum = cursor.fetchall()
    list = []
    for i in sum:
        list.append(i[0])
    routineIncrement = list[0]
    print("经理自营业绩")
    print(routineIncrement)

    # 经理个人机会区内业绩
    # cursor1 = db.cursor()
    sql_chance1 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
                  "AND districtSaleType = 1 AND expressDate <= '%s' AND districtId = 0 and districtPid = %s " % (companyId,beginTime, endTime,pid)
    cursor.execute(sql_chance1)
    sumChance = cursor.fetchall()
    if sumChance:
        list = []
        for i in sumChance:
            list.append(i[0])
        chanceIncrement = list[0]
    else:
        chanceIncrement = 0
    print("经理机会区内业绩")
    print(chanceIncrement)

    # 经理机会区外业绩
    # cursor2 = db.cursor()
    sql_chance2 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE companyId = '%s' AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
                  "AND districtSaleType = 2 AND expressDate <= '%s' AND districtId = 0 and districtPid = %s " % (companyId,beginTime, endTime,pid)
    cursor.execute(sql_chance2)
    sumChance2 = cursor.fetchall()
    if sumChance2:
        list = []
        for i in sumChance2:
            list.append(i[0])
        chanceIncrement2 = list[0]

    else:
        chanceIncrement2 = 0
    print("经理机会区外业绩")
    print(chanceIncrement2)

    # 经理区内机会业绩整单
    # cursor3 = db.cursor()
    sql_chance3 = "SELECT cast(IFNULL(SUM(total),0)as CHAR) FROM sale_source_data WHERE expressNo in (SELECT expressNo FROM sale_source_data WHERE companyId = '%s' " \
                  "AND saleTypeId = 1 " \
                  "AND perfType = 2 AND expressDate >= '%s' AND expressDate <= '%s' AND districtId = 0 and districtPid = %s AND districtSaleType = 1)" % (
                  companyId,beginTime, endTime,pid)
    cursor.execute(sql_chance3)
    sumChance3 = cursor.fetchall()
    if sumChance3:
        list = []
        for i in sumChance3:
            list.append(i[0])
        chanceIncrement3 = list[0]
    else:
        chanceIncrement3 = 0
    # print(chanceIncrement3)

    return routineIncrement,chanceIncrement,chanceIncrement2,chanceIncrement3

def get_Pid_total(pid,beginTime, endTime):
    '''
    区域经理
    区域业绩=∑(辖区所有片区的区域业绩）+大区经理自营业绩+大区经理的区内合作订单业绩
    大区经理个人总业绩 =∑(辖区内业务员的常规业绩+区内机会业绩+区外机会业绩*系数）+大区经理常规业绩+大区经理的区内机会业绩+大区经理的区外机会业绩
    :return:
    '''
    #获取一级区域下所有二级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT cast(id as CHAR) FROM cfg_district WHERE parent_id = %s" %(pid)
    cursor.execute(sql_id)
    id = cursor.fetchall()
    if id:
        list = [i[0] for i in id]
        # print(list)
        #机会分成
        disOutchance = 0
        #二级区域业绩
        distotal = 0
        disroutine = 0
        disInchance = 0
        for id in list:
            increment = get_Increment(id,beginTime,endTime)
            distotal = increment[4] + distotal
            # c = get_Increment(id,beginTime,endTime)[2]
            disOutchance = disOutchance + float(increment[2])*chance_ratio
            disroutine = disroutine + float(increment[0])
            disInchance = disInchance + float(increment[1])
    else:
        distotal = 0
        disOutchance = 0
        disroutine = 0
        disInchance = 0
    Pid_Increment = get_Pid_Increment(pid,beginTime,endTime)
    pid_routine = Pid_Increment[0]
    pid_chance = Pid_Increment[3]
    #经理区域业绩
    pid_distotal = distotal + float(pid_routine) + float(pid_chance)
    print("经理区域业绩")
    print(pid_distotal)

    pid_chance1 = Pid_Increment[1]
    pid_chance2 = Pid_Increment[2]
    #经理个人业绩
    pid_total = disroutine + disInchance + disOutchance + float(pid_routine) + float(pid_chance1) + float(pid_chance2)
    print("经理个人业绩")
    print(pid_total)

    #经理自营总业绩（包含二级）
    pid_routineAllPerf = disroutine + float(pid_routine)
    # 经理机会总业绩（包含二级）
    pid_chanceAllPerf = disInchance + disOutchance + float(pid_chance1) + float(pid_chance2)

    return  pid_distotal,pid_total,pid_routineAllPerf,pid_chanceAllPerf



def company_total(beginTime, endTime):
    '''
    公司的累计当前业绩
    :return:
    '''
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    company_total = 0
    if pid:
        list = [i[0] for i in pid]
        for pid in list:
            pid_total = get_Pid_total(pid,beginTime, endTime)
            company_total = company_total + float(pid_total[0])
    print("公司累计业绩")
    print(company_total)
    return company_total


if __name__ == "__main__":
    # increment = get_Increment(245,'2020-01-01','2020-12-31')
    # print("业务员常规，区内，区外，个人业绩，区域业绩")
    # print(increment)

    # pid_incrment = get_Pid_Increment(177,'2021-01-01','2021-03-01')
    # print("大区经理常规，区内，区外，区内整单业绩")
    # print(pid_incrment)

    get_Pid_total(210,'2020-04-01','2021-03-31')

    #公司业绩
    # company_total('2021-03-01','2021-03-04')