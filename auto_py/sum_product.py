# -*- coding: utf-8 -*-
# @Time : 2021/3/25 11:44
# @Author : zengxiaoyan
# @File : sum_product.py
'''
围绕品项展开的销售额、毛利额和占比的计算
'''
import pymysql,json
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')
def perform(districtId,districtPid,beginTime,endTime,uid):
    '''
    某区域某产品该年度累计业绩额
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    # if companyId == 1 or companyId == 8:
    if db_config['db'] == "suplus_goal_preonline":
        product = "suplus_product_preonline"
    elif db_config['db'] == "suplus_goal":
        product = "suplus_product"
    else:
        product = "suplus_product_test"
    sql = "SELECT a.productName,cast(IFNULL(SUM(total),0) AS CHAR ),a.productId from sale_source_data a,%s.products b WHERE a.companyId = %s  " \
          "and a.districtId = %s  AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.productId = b.id   " \
          "GROUP BY b.id  ORDER BY SUM(total) DESC ,a.productId ASC" %(product,companyId,districtId,beginTime,endTime)
    sql_pid = "SELECT a.productName,cast(IFNULL(SUM(total),0) AS CHAR ),a.productId from sale_source_data a,%s.products b WHERE a.companyId = %s  " \
          "AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.productId = b.id   " \
          "GROUP BY b.id  ORDER BY SUM(total) DESC,a.productId ASC" % (product,companyId, districtPid, beginTime, endTime)
    sql_myself = "SELECT a.productName,cast(IFNULL(SUM(total),0) AS CHAR ),a.productId from sale_source_data a,%s.products b WHERE a.companyId = %s  " \
          "AND a.uid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.productId = b.id   " \
          "GROUP BY b.id  ORDER BY SUM(total) DESC,a.productId ASC" % (product,companyId, uid, beginTime, endTime)
    sql_company = "SELECT a.productName,cast(IFNULL(SUM(total),0) AS CHAR ),a.productId from sale_source_data a,%s.products b WHERE a.companyId = %s  " \
                 " AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.productId = b.id   " \
                 "GROUP BY b.id  ORDER BY SUM(total) DESC,a.productId ASC" % (product,companyId,  beginTime, endTime)
    if uid == 0:

        if districtId  == 0 and districtPid == 0:
            cursor.execute(sql_company)
        elif  districtId == 0 and districtPid != 0:
            cursor.execute(sql_pid)
        else:
            cursor.execute(sql)
    else:
        cursor.execute(sql_myself)
    listPerf = cursor.fetchall()
    perf = []
    for i in listPerf:
        perf.append(i)
    # for j in perf:
    #     print(j)

    return perf

def grossPro(districtId, districtPid, beginTime, endTime,uid):
    '''
    某区域某产品该年度累计毛利额
    毛利额=自营毛利额+机会毛利额
    :return:
    '''
    #自营毛利额
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,product_price b WHERE a.companyId = %s " \
          "AND a.districtId = %s  AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.perfType = 1  " \
          "AND a.saleTypeId = 1  AND a.districtPid=b.districtId AND a.productId=b.productId AND a.expressDate>=b.startTime  " \
          "AND a.expressDate<=b.endTime AND b.deletedAt is null  GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
          % (companyId, districtId, beginTime, endTime)
    sql_pid = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,product_price b WHERE a.companyId = %s " \
          "AND a.districtPid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.perfType = 1  " \
          "AND a.saleTypeId = 1  AND a.districtPid=b.districtId AND a.productId=b.productId AND a.expressDate>=b.startTime  " \
          "AND a.expressDate<=b.endTime AND b.deletedAt is null  GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
          % (companyId, districtPid, beginTime, endTime)
    sql_myself = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,product_price b WHERE a.companyId = %s " \
          "AND a.uid = %s AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.perfType = 1  " \
          "AND a.saleTypeId = 1  AND a.districtPid=b.districtId AND a.productId=b.productId AND a.expressDate>=b.startTime  " \
          "AND a.expressDate<=b.endTime AND b.deletedAt is null  GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
          % (companyId, uid, beginTime, endTime)
    sql_company = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,product_price b WHERE a.companyId = %s " \
                 " AND a.expressDate >= '%s' AND a.expressDate <= '%s'  AND a.perfType = 1  " \
                 "AND a.saleTypeId = 1  AND a.districtPid=b.districtId AND a.productId=b.productId AND a.expressDate>=b.startTime  " \
                 "AND a.expressDate<=b.endTime AND b.deletedAt is null  GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
                 % (companyId, beginTime, endTime)
    if uid == 0:
        if  districtId == 0 and districtPid != 0:
            cursor.execute(sql_pid)
        elif districtId == 0 and districtPid == 0:
            cursor.execute(sql_company)
        else:
            cursor.execute(sql)
    else:
        cursor.execute(sql_myself)
    listGross = cursor.fetchall()
    grossProRoutine = []
    for i in listGross:
        grossProRoutine.append(i)

    # print(grossProRoutine)

    #机会毛利额
    if db_config['db'] == "suplus_goal_preonline":
        customer = "suplus_customer_preonline"
    elif db_config['db'] == "suplus_goal":
        customer = "suplus_customer"
    else:
        customer = "suplus_customer_test"
    sql_chance = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,%s.customer b," \
                 "product_price c WHERE a.companyId = %s  AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId " \
                 "AND a.productId = c.productId AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  " \
                 "AND a.expressDate>=c.startTime  AND a.districtId = %s  AND a.expressDate >= '%s' " \
                 "AND a.expressDate <= '%s' GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
                 % (customer,companyId, districtId,  beginTime, endTime)
    sql_chance_pid = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,%s.customer b," \
                 "product_price c WHERE a.companyId = %s  AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId " \
                 "AND a.productId = c.productId AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  " \
                 "AND a.expressDate>=c.startTime  AND a.districtPid = %s AND a.expressDate >= '%s' " \
                 "AND a.expressDate <= '%s' GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
                     % (customer,companyId, districtPid, beginTime, endTime)
    sql_chance_myself = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,%s.customer b," \
                 "product_price c WHERE a.companyId = %s  AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId " \
                 "AND a.productId = c.productId AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  " \
                 "AND a.expressDate>=c.startTime  AND a.uid = %s AND a.expressDate >= '%s' " \
                 "AND a.expressDate <= '%s' GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC"\
                        % (customer,companyId, uid, beginTime, endTime)
    sql_chance_company = "SELECT productName,cast(IFNULL(SUM(total-saleNum*costPrice),0)AS CHAR ),a.productId FROM sale_source_data a ,%s.customer b," \
                        "product_price c WHERE a.companyId = %s  AND a.perfType = 2 and a.saleTypeId = 1 AND a.customerId = b.customerId " \
                        "AND a.productId = c.productId AND b.serviceAreaPid = c.districtId AND c.endTime>=a.expressDate  " \
                        "AND a.expressDate>=c.startTime   AND a.expressDate >= '%s' " \
                        "AND a.expressDate <= '%s' GROUP BY a.productId ORDER BY SUM(total-saleNum*costPrice) DESC" \
                         % (customer, companyId, beginTime, endTime)
    if uid == 0:
        if  districtId == 0 and districtPid != 0:
            cursor.execute(sql_chance_pid)
        elif districtId == 0 & districtPid == 0:
            cursor.execute(sql_chance_company)
        else:
            cursor.execute(sql_chance)
    else:
        cursor.execute(sql_chance_myself)
    list_chance = cursor.fetchall()
    grossProChance = []
    for j in list_chance:
        grossProChance.append(j)
    # print(grossProChance)

    #总毛利额=自营毛利额+机会毛利额
    grossP = grossProRoutine + grossProChance
    # print(grossP)
    l = len(grossP)
    grossP_new = [list(i) for i in grossP]

    # 相同品项毛利额求和
    delNo = []
    for x in range(l):
        y = x+1
        for z in range(y,l):
            if grossP_new[x][2] == grossP_new[z][2]:
                grossP_new[x][1] = float(grossP_new[x][1]) + float(grossP_new[z][1])
                delNo.append(z)

        grossP_new[x][1] = float(grossP_new[x][1])
    # 删除重复项
    delNo.sort()
    l_delNo = len(delNo)
    counter = 0
    if l_delNo != 0:
        for i in delNo:
            i = i - counter
            grossP_new.pop(i)
            counter = counter + 1

    grossP_list = sorted(grossP_new,key=lambda x:x[1],reverse=True)
    # for j in grossP_list:
    #     print(j)


    return grossP_list


def perform_and_profit(districtId, districtPid, beginTime, endTime,uid):
    '''
    业绩额倒叙
    业绩与毛利额合并
    :param districtId:
    :param districtPid:
    :param beginTime:
    :param endTime:
    :param uid:
    :return:
    '''
    performance = perform(districtId, districtPid, beginTime, endTime,uid)
    profit = grossPro(districtId, districtPid, beginTime, endTime,uid)
    sales = []
    for i in performance:
        sale = []
        c = 0
        for j in profit:
            if i[2] == j[2]:
                sale.append(i[0])
                sale.append(i[1])
                sale.append(i[2])
                sale.append(j[1])
                c = 1
        if c == 0:
            sale.append(i[0])
            sale.append(i[1])
            sale.append(i[2])
            sale.append(0)
        sales.append(sale)
    # print(sales)

    sum_sale = 0
    sum_grossP = 0
    sales_len = len(sales)
    for i in sales:
        sum_sale = sum_sale + float(i[1])
        sum_grossP = sum_grossP + float(i[3])

    # productSale_ratio = []
    # productProfit_ratio = []
    for i in range(sales_len):
        #销售额占比
        if sum_sale <= 0:
            ratio = 0
        else:
            ratio = round(float(sales[i][1]) / sum_sale *100, 2)
        sales[i].append(ratio)
        #毛利额占比
        if sum_grossP <= 0:
            profRatio = 0
        else:
            profRatio = round(float(sales[i][3]) / sum_grossP *100, 2)
        sales[i].append(profRatio)
    y = 1
    for i in sales:

        print(y)
        y = y + 1
        print(i)
    return sales



def sum_districtsPerf(districtIdList,districtPidList,beginTime,endTime):
    '''
    多个区域累计销售额
    :return:
    '''
    dpid_len = len(districtPidList)
    did_len = len(districtIdList)
    all_perf = []

    if dpid_len != 0:
        for i in districtPidList:
            perf = perform(0,i,beginTime,endTime,0)
            for x in perf:
                all_perf.append(x)
    if did_len != 0:
        for j in districtIdList:
            perf = perform(j,0,beginTime,endTime,0)
            for x in perf:
                all_perf.append(x)
    # print(all_perf)

    #将元组变为list
    all_perf = [list(i) for i in all_perf]
    # print(all_perf)
    #相同品项求和
    all_len = len(all_perf)
    delNo = []
    for x in range(all_len):
        y = x + 1
        for z in range(y, all_len):
            if all_perf[x][2] == all_perf[z][2]:
                all_perf[x][1] = float(all_perf[x][1]) + float(all_perf[z][1])
                delNo.append(z)
        all_perf[x][1] = float(all_perf[x][1])

    #去重
    l_delNo = len(delNo)
    counter = 0
    if l_delNo != 0:
        for i in delNo:
            i = i - counter
            all_perf.pop(i)
            counter = counter + 1
    # for i in all_perf:
    #     print(i)
    #     print(type(i[1]))
    all_perf_new = sorted(all_perf,key=lambda x:x[1] ,reverse=True)
    print("区域累计销售额倒叙")
    for i in all_perf_new:
        print(i)

def sum_districtsProf(districtIdList,districtPidList,beginTime,endTime):
    '''
    筛选各区域累计的毛利额和
    :param districtIdList:
    :param districtPidList:
    :param beginTime:
    :param endTime:
    :return:
    '''
    dpid_len = len(districtPidList)
    did_len = len(districtIdList)
    all_prof = []
    if dpid_len != 0:
        for i in districtPidList:
            prof = grossPro(0, i, beginTime, endTime, 0)
            for y in prof:
                all_prof.append(y)
    if did_len != 0:
        for j in districtIdList:
            prof = grossPro(j, 0, beginTime, endTime, 0)
            for y in prof:
                all_prof.append(y)
    #元组转列表
    all_prof = [list(i) for i in all_prof]
    # 相同品项求和
    all_len = len(all_prof)
    delNo = []
    for x in range(all_len):
        y = x + 1
        for z in range(y, all_len):
            if all_prof[x][2] == all_prof[z][2]:
                all_prof[x][1] = float(all_prof[x][1]) + float(all_prof[z][1])
                delNo.append(z)
        all_prof[x][1] = float(all_prof[x][1])

        # 去重
        l_delNo = len(delNo)
        counter = 0
        if l_delNo != 0:
            for i in delNo:
                i = i - counter
                all_prof.pop(i)
                counter = counter + 1

    all_prof_new = sorted(all_prof, key=lambda x: x[1], reverse=True)
    print("区域累计毛利额倒叙")
    for i in all_prof_new:
        print(i)


# def ratio(districtId,districtPid,beginTime,endTime,uid):
#     '''
#     首页（前20）占比：产品销售额/区域总销售额
#     更多页面占比：产品销售额/筛选结果列表页总销售额
#     :return:
#     '''
#     #销售额
#     # performance = perform(districtId,districtPid,beginTime,endTime,uid)
#     # sum_sale = 0
#     # for i in performance:
#     #     sum_sale = sum_sale + float(i[1])
#     # print(sum_sale)
#     #
#     # #毛利额
#     # grossProfit = grossPro(districtId,districtPid,beginTime,endTime,uid)
#     # sum_grossP = 0
#     # for j in grossProfit:
#     #     sum_grossP = sum_grossP + float(j[1])
#
#
#
#     perforProfit = perform_and_profit(districtId,districtPid,beginTime,endTime,uid)
#     sum_sale = 0
#     sum_grossP = 0
#     for i in perforProfit:
#         sum_sale = sum_sale + float(i[1])
#         sum_grossP = sum_grossP + float(i[3])
#     perf_len = len(perforProfit)
#     prof_len = len(perforProfit)
#
#     productSale_ratio = []
#     productProfit_ratio = []
#     for i in range(perf_len):
#         #销售额占比
#         ratio = round(float(perforProfit[i][1]) / sum_sale,4)
#         productSale_ratio.append(ratio)
#     # print(productSale_ratio)
#     for i in range(prof_len):
#         #利润额占比
#         profRatio = round(float(perforProfit[i][3]) / sum_grossP,4)
#         productProfit_ratio.append(profRatio)
#
#     # print("品项销售额占比降序")
#     # perf_ratio = dict(zip(perforProfit,productSale_ratio))
#     # for k,v in perf_ratio.items():
#     #     print(k)
#     #     print(v)
#     #
#     # print("品项毛利额占比降序")
#     # for i in range(prof_len):
#     #     print(perforProfit[i])
#     #     print(productProfit_ratio[i])
#     # prof_ratio = dict(zip(grossProfit,main_productProfit_ratio))  #dict的key值不支持list或dict类型
#
#     return productSale_ratio,productProfit_ratio



if __name__ == "__main__":
    #销售额(非仅看自己时uid为0）
    # perform(0,37,'2021-04-01','2021-09-09',0)

    #毛利额(非仅看自己时uid为0）
    grossPro(0,231,'2020-04-01','2020-08-31',0)

    # perform_and_profit(0,0,'2021-04-01','2021-08-31',0)

    #筛选各个区域销售额求和
    # sum_districtsPerf([],[183,210,287],'2020-01-01','2020-12-31')

    # 筛选各个区域毛利额求和
    # sum_districtsProf([180, 245], [184, 207], '2021-01-01', '2021-03-31')

    # 占比值
    # ratio(0,179,'2021-01-01','2021-12-31',0)
