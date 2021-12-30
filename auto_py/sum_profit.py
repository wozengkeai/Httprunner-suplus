# -*- coding: utf-8 -*-
# @Time : 2021/2/25 16:20
# @Author : zengxiaoyan
# @File : sum_profit.py
import pymysql
from auto_py.sum_cost import get_personcost,get_pid_personcost,get_usercost,get_costRate,get_pid_costRate,get_pidcost,companyCost
from auto_py.sum_incrment import get_Increment,get_Pid_Increment,get_Pid_total,company_total
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')
chance_ratio = gol.get_value('chance_ratio')
# chance_ratio = 0.3
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

def get_grossProfit(id, beginTime, endTime):
    '''
    业务员业绩毛利额=自营毛利额+机会毛利额
    自营毛利额=自营业绩-自营成本
    机会毛利额= 机会业绩-机会成本
    累计个人总毛利=累计个人业绩总毛利+SKU加码毛利-公司应得毛利
    :return:
    '''
    #自营毛利额
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
          "AND a.saleTypeId = 1 AND a.districtId = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId " \
          "AND a.productId=b.productId AND a.expressDate>=b.startTime AND a.expressDate<=b.endTime" % (companyId, id, beginTime, endTime)
    cursor.execute(sql)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    routineProfit = list[0]
    # print(routineProfit)

    #区内机会毛利额
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    # db1 = pymysql.connect(**db_config)
    # cursor1 = db1.cursor()
    sql_chance = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
          "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
          "AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate AND a.expressDate>=c.startTime AND a.districtId = '%s' " \
          "AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND districtSaleType = 1  " % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_chance)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    chanceInProfit = list[0]
    # print(chanceProfit)

    #区内机会整单毛利额
    sql_chanceInall = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c WHERE " \
                      "a.companyId = %s AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                      "AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  AND a.expressDate>=c.startTime AND a.expressNo in " \
                      "(SELECT expressNo FROM sale_source_data WHERE companyId = %s AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
                      "AND expressDate <= '%s' AND districtId = %s  AND districtSaleType = 1  )  " % ( customer,companyId,companyId, beginTime, endTime ,id)
    cursor.execute(sql_chanceInall)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    chanceInallProfit = list[0]

    #区外机会毛利
    # db4 = pymysql.connect(**db_config)
    # cursor4 = db4.cursor()
    sql_outchance = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                    "WHERE a.companyId = %s AND a.perfType = 2 and a.saleTypeId = 1 AND districtSaleType = 2 AND a.customerId = b.customerId " \
                    "AND a.productId = c.productId AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate AND a.expressDate>=c.startTime " \
                    "AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'   " % (
                    customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_outchance)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    chanceOutProfit = list[0]
    # print(chanceOutProfit)

    #个人业绩总毛利额
    perfProfit = float(routineProfit) + float(chanceInProfit) + float(chanceOutProfit)
    print("个人业绩总毛利额")
    print(perfProfit)

    #区域业绩毛利额
    districtPerfProfit = float(routineProfit) + float(chanceInallProfit)
    print("区域毛利")
    print(districtPerfProfit)

    #区外SKU加码毛利额
    # db2 = pymysql.connect(**db_config)
    # cursor2 = db2.cursor()
    sql_extract_out = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0) as CHAR) FROM sale_source_data a,product_extra_bonus b,%s.customer c WHERE " \
                  "a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND a.productId = b.productId AND c.serviceAreaPid = b.districtId " \
                  "AND a.customerId = c.customerId AND a.companyId = %s AND a.districtId =  %s AND a.expressDate >= '%s' " \
                  "AND a.expressDate <= '%s' AND a.districtSaleType = 2 AND a.saleTypeId = 1" % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_extract_out)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    extractOutProfit = list[0]
    # print("SKU加码毛利额")
    # print(extractProfit)

    #区内SKU加码毛利额
    # db2 = pymysql.connect(**db_config)
    # cursor2 = db2.cursor()
    sql_extract_in = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0)as CHAR) FROM sale_source_data a,product_extra_bonus b WHERE a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                      "AND a.productId = b.productId   AND a.companyId = %s AND a.districtId = %s AND a.districtPid = b.districtId AND a.expressDate >= '%s'" \
                      " AND a.expressDate <= '%s' AND a.districtSaleType = 1 AND a.saleTypeId = 1" % (companyId, id, beginTime, endTime)
    cursor.execute(sql_extract_in)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    extractInProfit = list[0]

    #自营加码
    sql_extract_routine = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0)as CHAR) FROM sale_source_data a,product_extra_bonus b WHERE a.expressDate >= b.startTime AND a.expressDate <= b.endTime " \
                     "AND a.productId = b.productId   AND a.companyId = %s AND a.districtId = %s AND a.districtPid = b.districtId AND a.expressDate >= '%s'" \
                     " AND a.expressDate <= '%s' AND a.perfType = 1 AND a.saleTypeId = 1" % (
                     companyId, id, beginTime, endTime)
    cursor.execute(sql_extract_routine)
    sumRoutine = cursor.fetchall()
    list = [i[0] for i in sumRoutine]
    extractProfit = list[0]

    #个人加码利润额
    personExtract = float(extractOutProfit) + float(extractProfit) + float(extractInProfit)
    print("个人加码利润额")
    print(personExtract)

    # 业务员--公司应得毛利额--区内
    # db3 = pymysql.connect(**db_config)
    # cursor3 = db3.cursor()
    sql_companyIn = "SELECT cast(IFNULL(SUM(saleNum*companyProfit),0)as CHAR) FROM sale_source_data a,company_profit_setting b,%s.customer c WHERE " \
                  "a.productId = b.productId AND c.serviceAreaId = b.districtId AND a.customerId = c.customerId AND a.expressDate >= b.startTime " \
                  "AND a.expressDate <= b.endTime AND a.companyId = %s AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  " \
                  "AND a.districtSaleType = 1 AND a.saleTypeId = 1" % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_companyIn)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    companyInProfit = list[0]
    # print("公司应得毛利额")
    # print(companyProfit)

    #自营
    sql_companyRoutine = "SELECT cast(IFNULL(SUM(saleNum*companyProfit),0)as CHAR) FROM sale_source_data a,company_profit_setting b,%s.customer c WHERE " \
                    "a.productId = b.productId AND c.serviceAreaId = b.districtId AND a.customerId = c.customerId AND a.expressDate >= b.startTime " \
                    "AND a.expressDate <= b.endTime AND a.companyId = %s AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  " \
                    "AND a.perfType = 1 AND a.saleTypeId = 1" % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_companyRoutine)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    companyRoutineProfit = list[0]

    #业务员-公司应得-区外
    sql_company_out = "SELECT cast(IFNULL(SUM(saleNum*companyProfit),0)as CHAR) FROM sale_source_data a,company_profit_setting b,%s.customer c WHERE " \
                  "a.productId = b.productId AND c.serviceAreaId = b.districtId AND a.customerId = c.customerId AND a.expressDate >= b.startTime " \
                  "AND a.expressDate <= b.endTime AND a.companyId = %s AND a.districtId = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  " \
                  "AND a.districtSaleType = 2 AND a.saleTypeId = 1" % (customer,companyId, id, beginTime, endTime)
    cursor.execute(sql_company_out)
    sum_out = cursor.fetchall()
    list = [i[0] for i in sum_out]
    companyOutProfit = list[0]
    sum_companyProfit = float(companyInProfit) + float(companyOutProfit) + float(companyRoutineProfit)
    print("业务员公司应得毛利额")
    print(sum_companyProfit)

    #业务员累计个人总毛利额=累计个人业绩总毛利+SKU加码毛利-公司应得毛利
    grossProfit = perfProfit + float(personExtract) - float(sum_companyProfit)
    print("业务员累计个人总毛利额")
    print(grossProfit)

    return routineProfit,chanceInProfit,chanceOutProfit,extractProfit,extractOutProfit,grossProfit,companyInProfit,companyOutProfit,extractInProfit,\
           companyRoutineProfit,districtPerfProfit,chanceInallProfit

def pid_grossProfit(pid, beginTime, endTime):
    '''
    大区经理个人总毛利额 = 业绩毛利额+ SKU加码 - 公司应得利润
    业绩毛利额= 自营业绩毛利+机会业绩毛利+二级区外业绩*分成系数
    SKU加码毛利区外业绩按照对应所在区内的区域价格算
    :return:
    '''
    # 自营毛利额
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,product_price b WHERE a.companyId = '%s' AND a.perfType = 1 " \
          "AND a.saleTypeId = 1 AND a.districtId = 0 AND a.districtPid = '%s' AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.districtPid=b.districtId " \
          "AND a.productId=b.productId AND a.expressDate>=b.startTime AND a.expressDate<=b.endTime" % (
          companyId, pid, beginTime, endTime)
    cursor.execute(sql)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_routineProfit = list[0]
    # print(pid_routineProfit)

    # 经理个人机会毛利额
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    # db1 = pymysql.connect(**db_config)
    # cursor1 = db1.cursor()
    sql_chance = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c " \
                 "WHERE a.companyId = '%s' AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                 "AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate AND a.expressDate>=c.startTime AND a.districtId = 0 AND a.districtPid = '%s' " \
                 "AND a.expressDate >= '%s' AND a.expressDate <= '%s'   " % (customer,companyId, pid, beginTime, endTime)
    cursor.execute(sql_chance)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_chanceProfit = list[0]
    # print(pid_chanceProfit)

    #二级业务员区外业绩分成毛利
    # 获取一级区域下所有二级区域id
    db3 = pymysql.connect(**db_config2)
    cursor3 = db3.cursor()
    sql_id = "SELECT cast(id as CHAR) FROM cfg_district WHERE parent_id = %s" % (pid)
    cursor3.execute(sql_id)
    id = cursor3.fetchall()
    routinePro = 0
    chanceInpro = 0
    chanceOutPro = 0
    chanceInAllPro = 0
    #二级自营+区内加码，区外加码
    extractProfit = 0
    extractInProfit = 0
    extractOutProfit = 0
    #二级自营+区内公司应该，区外公司应得
    companyInProfit = 0
    companyOutProfit = 0
    companyRoutineProfit = 0
    if id:
        list = [i[0] for i in id]
        for id in list:
            id_profit = get_grossProfit(id,beginTime, endTime)
            routinePro = routinePro + float(id_profit[0])
            chanceInpro = chanceInpro + float(id_profit[1])
            chanceOutPro = chanceOutPro + float(id_profit[2]) * chance_ratio
            chanceInAllPro = chanceInAllPro + float(id_profit[11])

            # person_extractProfit = get_grossProfit(id,beginTime, endTime)
            extractProfit = extractProfit + float(id_profit[3])
            extractOutProfit = extractOutProfit + float(id_profit[4])
            extractInProfit = extractInProfit + float(id_profit[8])

            companyInProfit = companyInProfit + float(id_profit[6])
            companyOutProfit = companyOutProfit + float(id_profit[7])
            companyRoutineProfit = companyRoutineProfit + float(id_profit[9])

    # print(chanceOutPro)

    #大区经理业绩总毛利额
    perfProfit = float(routinePro) + float(chanceInpro) + float(chanceOutPro) + float(pid_routineProfit) + float(pid_chanceProfit)
    print("大区经理业绩总毛利额")
    print(perfProfit)
    #大区经理自营总毛利（包含二级）
    routineAllProfit = float(routinePro) + float(pid_routineProfit)
    #大区经理机会总毛利额（包含二级）
    chanceAllProfit = float(pid_chanceProfit) +  float(chanceInpro) + float(chanceOutPro)

    #大区经理自己区内机会整单毛利
    sql_chanceInall = "SELECT cast(IFNULL(SUM(total-saleNum*costPrice),0)as CHAR) FROM sale_source_data a ,%s.customer b ,product_price c WHERE " \
                      "a.companyId = %s AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId AND a.productId = c.productId " \
                      "AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  AND a.expressDate>=c.startTime AND a.expressNo in " \
                      "(SELECT expressNo FROM sale_source_data WHERE companyId = %s AND saleTypeId = 1 AND perfType = 2 AND expressDate >= '%s' " \
                      "AND expressDate <= '%s' AND districtId = 0 and districtPid = %s  AND districtSaleType = 1  )  " % (
                      customer,companyId, companyId, beginTime, endTime, pid)
    cursor.execute(sql_chanceInall)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_chanceInallProfit = list[0]

    #大区经理区域业绩总毛利额(包含二级）
    districtPerfProfit = float(pid_routineProfit) + float(pid_chanceInallProfit) + float(routinePro) + float(chanceInAllPro)
    print("大区经理区域业绩总毛利额")
    print(districtPerfProfit)

    #经理SKU加码毛利==∑(辖区内业务员的常规业绩对应的加码SKU加码毛利额+区内机会业绩对应的加码SKU加码毛利额+区外机会业绩对应的加码SKU加码毛利额*系数）
    # +大区经理常规业绩对应的加码SKU加码毛利额+大区经理的区内机会业绩对应的加码SKU加码毛利额+大区经理的区外机会业绩对应的加码SKU加码毛利额

    #大区经理自己 区内加码
    # db2 = pymysql.connect(**db_config)
    # cursor2 = db2.cursor()
    sql_extractIn = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0)as CHAR) FROM sale_source_data a,product_extra_bonus b WHERE a.expressDate >= b.startTime " \
                  "AND a.expressDate <= b.endTime AND a.productId = b.productId   AND a.companyId = %s AND a.districtId = 0 AND a.districtPid = %s " \
                  "AND a.districtPid = b.districtId AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.districtSaleType = 1 " \
                  "AND a.saleTypeId = 1" % (companyId, pid, beginTime, endTime)
    cursor.execute(sql_extractIn)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_extractInProfit = list[0]

    #自营加码
    sql_extractRoutine = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0)as CHAR) FROM sale_source_data a,product_extra_bonus b WHERE a.expressDate >= b.startTime " \
                    "AND a.expressDate <= b.endTime AND a.productId = b.productId   AND a.companyId = %s AND a.districtId = 0 AND a.districtPid = %s " \
                    "AND a.districtPid = b.districtId AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.perfType = 1 " \
                    "AND a.saleTypeId = 1" % (companyId, pid, beginTime, endTime)
    cursor.execute(sql_extractRoutine)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_extractRoutineProfit = list[0]

    #大区经理自己区外加码
    # db5 = pymysql.connect(**db_config)
    # cursor5 = db5.cursor()
    sql_extract = "SELECT cast(IFNULL(SUM(saleNum*extraBonus),0)as CHAR) FROM sale_source_data a,product_extra_bonus b,%s.customer c WHERE a.expressDate >= b.startTime " \
                  "AND a.expressDate <= b.endTime AND a.productId = b.productId AND c.serviceAreaPid = b.districtId AND a.customerId = c.customerId " \
                  "AND a.companyId = %s AND a.districtId = 0 AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s' AND a.districtSaleType = 2 " \
                  "AND a.saleTypeId = 1" % (customer,companyId, pid, beginTime, endTime)
    cursor.execute(sql_extract)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    pid_extractOutProfit = list[0]

    #大区经理自营加码毛利（包含二级）
    extractRoutineAllPro = float(extractProfit) + float(pid_extractRoutineProfit)
    # 大区经理机会加码毛利（包含二级）
    extractChanceAllPro = float(extractInProfit) + float(extractOutProfit) * chance_ratio + float(pid_extractInProfit) + float(pid_extractOutProfit)
    #大区经理加码总毛利
    persanExtractPro =  float(extractProfit) + float(extractInProfit) + float(extractOutProfit) * chance_ratio + float(pid_extractInProfit) + float(pid_extractOutProfit) + float(pid_extractRoutineProfit)
    print("经理SKU加码毛利")
    print(persanExtractPro)

    #大区经理-公司应得利润 自营
    # db4 = pymysql.connect(**db_config)
    # cursor4 = db4.cursor()
    sql_companyRoutine = "SELECT cast(IFNULL(SUM(saleNum*companyProfit),0)as CHAR) FROM sale_source_data a,company_profit_setting b,%s.customer c WHERE a.productId = b.productId AND c.serviceAreaId = b.districtId" \
                  " AND a.customerId = c.customerId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND a.companyId = %s " \
                  "AND a.districtId = 0 AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.saleTypeId = 1 AND a.perfType = 1" % (
                  customer,companyId, pid, beginTime, endTime)
    cursor.execute(sql_companyRoutine)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    CompanyRoutineProfit = list[0]

    #机会 公司应得
    sql_companyChance = "SELECT cast(IFNULL(SUM(saleNum*companyProfit),0)as CHAR) FROM sale_source_data a,company_profit_setting b,%s.customer c WHERE a.productId = b.productId AND c.serviceAreaId = b.districtId" \
                         " AND a.customerId = c.customerId AND a.expressDate >= b.startTime AND a.expressDate <= b.endTime AND a.companyId = %s " \
                         "AND a.districtId = 0 AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'   AND a.saleTypeId = 1 AND a.perfType = 2" % (
                             customer,companyId, pid, beginTime, endTime)
    cursor.execute(sql_companyChance)
    sum = cursor.fetchall()
    list = [i[0] for i in sum]
    CompanyChanceProfit = list[0]

    #大区经理 自营部分公司应得（包含二级|）
    companyRoutineAllProfit = float(CompanyRoutineProfit) + float(companyRoutineProfit)
    #大区经理 机会部分公司应得（包含二级）
    companyChanceAllProfit = float(CompanyChanceProfit) + float(companyInProfit) + float(companyOutProfit) * chance_ratio
    #大区经理 公司应得
    pid_companyProfit = float(CompanyRoutineProfit) + float(CompanyChanceProfit) + float(companyInProfit) + float(companyOutProfit) * chance_ratio + float(companyRoutineProfit)
    print("大区经理公司应得利润")
    print(pid_companyProfit)

    #大区经理个人毛利额
    pid_profit = perfProfit + float(persanExtractPro) - float(pid_companyProfit)
    print("大区经理个人总毛利额")
    print(pid_profit)
    return pid_profit,pid_routineProfit,pid_chanceProfit,pid_extractRoutineProfit,pid_extractInProfit,pid_extractOutProfit,CompanyRoutineProfit,\
           CompanyChanceProfit,chanceAllProfit,routineAllProfit,extractRoutineAllPro,extractChanceAllPro,companyRoutineAllProfit,companyChanceAllProfit,districtPerfProfit

def profit(id, beginTime, endTime):
    '''
    业务员的净利润=个人总业绩毛利-个人费用
    :return:
    '''
    grossProfit = get_grossProfit(id, beginTime, endTime)
    personCost = get_personcost(id, beginTime, endTime)
    profit = float(grossProfit[5]) - personCost
    print(profit)
    return profit

def pid_profit(pid, beginTime, endTime):
    '''
    大区经理净利润=ge人总业绩毛利-个人费用
    :return:
    '''
    grossProfit = pid_grossProfit(pid, beginTime, endTime)
    personCost = get_pid_personcost(pid, beginTime, endTime)
    profit = float(grossProfit[0]) - personCost
    print("大区经理净利润")
    print(profit)
    return profit


def profitRate(id, beginTime, endTime):
    '''
    业务员
常规利润率=（常规订单的毛利额-常规业绩×区域费用率+常规订单中有加码的SKU加码毛利总额-常规订单中有公司提价的SKU公司应得利润总额）÷常规业绩×100%
机会利润率=（机会订单的毛利额-机会业绩×区域费用率+机会订单中有加码的SKU加码毛利总额-机会订单中有公司提价的SKU公司应得利润总额）÷机会业绩×100%
区域利润率= （区域毛利-区域费用）/区域业绩
    :return:
    '''
    grossProfit = get_grossProfit(id, beginTime, endTime)
    routineGrossProfit = float(grossProfit[0])
    chanceGrossProfit = float(grossProfit[1]) + float(grossProfit[2])
    extractRoutineProfit = float(grossProfit[3])
    extractChanceProfit = float(grossProfit[4]) + float(grossProfit[8])
    companyRoutineProfit = float(grossProfit[9])
    compangChanceProfit = float(grossProfit[6]) + float(grossProfit[7])
    districtPerfProfit = float(grossProfit[10])


    performance = get_Increment(id, beginTime, endTime)
    routinePerf = float(performance[0])
    chancePerf = float(performance[1]) + float(performance[2])
    districtTotal = float(performance[4])

    costRate = float(get_costRate(id, beginTime, endTime))

    usercostList = get_usercost(id, beginTime, endTime)
    usercost = float(usercostList[0])

    #常规利润率
    if routinePerf != 0:
        routineProfitRate = (routineGrossProfit - routinePerf * costRate + extractRoutineProfit - companyRoutineProfit) / routinePerf
    else:
        routineProfitRate = 0
    print(routineProfitRate)

    #机会利润率
    if chancePerf != 0:
        chanceProfitRate = (chanceGrossProfit - chancePerf * costRate + extractChanceProfit - compangChanceProfit) / chancePerf
    else:
        chanceProfitRate = 0
    print(chanceProfitRate)

    #区域利润率
    if districtTotal != 0:
        districtProfitRate = (districtPerfProfit - usercost) / districtTotal
    else:
        districtProfitRate = 0

    #总利润率=(个人毛利-个人费用)/个人总业绩=个人净利润/个人总业绩
    personProfit = profit(id, beginTime, endTime)
    personTotal = get_Increment(id, beginTime, endTime)
    personTotalPerf = float(personTotal[3])
    if personTotalPerf != 0:
        profitRate = float(personProfit) / float(personTotal[3])
    else:
        profitRate = 0
    print(profitRate)

    return districtProfitRate,routineProfitRate,chanceProfitRate,profitRate


def pid_profitRate(pid, beginTime, endTime):
    '''
    大区经理
    常规利润率=（常规订单的毛利额+常规订单中有加码的SKU加码毛利总额-常规订单中有公司提价的SKU公司应得利润总额-常规业绩×区域费用率）÷常规业绩
    机会利润率=(机会订单的毛利额+机会订单中有加码的SKU加码毛利总额-机会订单中有公司提价的SKU公司应得利润总额-机会业绩×区域费用率）÷机会业绩
    :return:
    '''
    grossProfit = pid_grossProfit(pid, beginTime, endTime)
    routineGrossProfit = float(grossProfit[9])
    chanceGrossProfit = float(grossProfit[8])
    extractRoutineProfit = float(grossProfit[10])
    extractChanceProfit = float(grossProfit[11])
    companyRoutineProfit =float(grossProfit[12])
    companyChanceProfit = float(grossProfit[13])
    districtPerfProfit = float(grossProfit[14])

    disPerf = get_Pid_total(pid, beginTime, endTime)
    districtTotal = float(disPerf[0])
    personTotal = float(disPerf[1])
    routinePerf = float(disPerf[2])
    chancePerf = float(disPerf[3])

    costRate = float(get_pid_costRate(pid, beginTime, endTime))
    usercostList = get_pidcost(pid, beginTime, endTime)
    usercost = float(usercostList[0])

    # 常规利润率
    if routinePerf != 0:
        routineProfitRate = (routineGrossProfit - routinePerf * costRate + extractRoutineProfit - companyRoutineProfit) / routinePerf
    else:
        routineProfitRate = 0
    print(routineProfitRate)

    # 机会利润率
    if chancePerf != 0:
        chanceProfitRate = ( chanceGrossProfit - chancePerf * costRate + extractChanceProfit - companyChanceProfit) / chancePerf
    else:
        chanceProfitRate = 0
    print(chanceProfitRate)

    # 区域利润率
    if districtTotal != 0:
        districtProfitRate = (districtPerfProfit - usercost) / districtTotal
    else:
        districtProfitRate = 0
    print(districtProfitRate)

    # 总利润率=(个人毛利-个人费用)/个人总业绩=个人净利润/个人总业绩
    personProfit = pid_profit(pid, beginTime, endTime)
    # personTotal = get_Increment(id, beginTime, endTime)
    if personTotal != 0:
        profitRate = float(personProfit) / personTotal
    else:
        profitRate = 0
    print(profitRate)

    return districtProfitRate, routineProfitRate, chanceProfitRate, profitRate

def companyProfitRate( beginTime, endTime):
    '''
    公司区域利润率 = =（公司毛利-公司费用）÷公司业绩
    :return:
    '''
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    companyGrossProfit = 0
    if pid:
        list = [i[0] for i in pid]
        for pid in list:
            grossProfit = pid_grossProfit(pid, beginTime, endTime)
            companyGrossProfit = companyGrossProfit + float(grossProfit[14])
    print("公司毛利")
    print(companyGrossProfit)

    Cost = companyCost(beginTime,endTime)
    performance = company_total(beginTime,endTime)

    companyProfit = float(companyGrossProfit) - float(Cost)
    print(companyProfit)
    companyProfitRate = companyProfit / float(performance)
    print(companyProfitRate)

if __name__ == "__main__":
    #业务员累计个人总毛利额
    # get_grossProfit(178,'2021-01-01', '2021-01-31')

    # 大区经理累计个人总毛利额
    # pid_grossProfit(177, '2021-01-01', '2021-01-31')

    #业务员个人净利润
    # profit(178,'2021-01-01', '2021-01-31')

    # 大区经理个人净利润
    # pid_profit(37, '2021-03-01', '2021-03-05')

    #业务员利润率
    print(profitRate(180, '2020-01-01', '2020-12-31'))
    print("区域利润率，常规利润率，机会利润率，总利润率")

    #大区经理利润率
    # print(pid_profitRate(177, '2021-03-01', '2021-03-08'))
    # print("区域利润率，常规利润率，机会利润率，总利润率")

    #公司利润率
    # companyProfitRate('2020-04-01', '2021-03-05')