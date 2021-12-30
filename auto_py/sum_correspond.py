from auto_py.get_token import get_token
from auto_py.header import get_time,get_uuid,get_sign
import requests
import pymysql,json
from auto_py import gol,config
companyId = gol.get_value('companyId')
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')

def get_resSale(n,year,districtId):
    #同期累计业绩值,n表示当前为营销年第几月
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT monthData FROM correspond_sale_setting WHERE `year` = %s AND districtId = %s" %(year,districtId)
    cursor.execute(sql)
    monthdata = cursor.fetchall()
    # print(monthdata)
    list = []
    for i in monthdata:
        list.append(i[0])

    count = 0
    if list:
        L = json.loads(list[0])
        i = 0
        for j in L:
            count = count + j['count']
            i = i + 1
            if i >= n:
                print("同期累计业绩")
                print(count)
                return count
    print("同期累计业绩")
    print(count)
    return count

def pid_resSale(n,year,districtPid):
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT monthData FROM correspond_sale_setting WHERE `year` = %s AND districtId = 0 AND districtPid =  %s" % (year, districtPid)
    cursor.execute(sql)
    monthdata = cursor.fetchall()
    list = []
    for i in monthdata:
        list.append(i[0])

    pid_sameTermPerf = 0
    if list:
        L = json.loads(list[0])
        i = 0
        for j in L:
            pid_sameTermPerf = pid_sameTermPerf + j['count']
            i = i + 1
            if i >= n:
                print("同期累计业绩")
                print(pid_sameTermPerf)
                return pid_sameTermPerf
    print("大区经理同期累计业绩")
    print(pid_sameTermPerf)
    return pid_sameTermPerf

def company_resSale(n,year):
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    sameTermPerf = 0
    if pid:
        list = [i[0] for i in pid]

        for pid in list:
            pid_sameTermPerf = pid_resSale(n,year,pid)
            sameTermPerf = sameTermPerf + pid_sameTermPerf
    print("公司同期累计业绩")
    print(sameTermPerf)
    return sameTermPerf

def sum_profit(n,year,districtId):
    #累计同期利润额
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT monthData FROM correspond_profit_setting WHERE `year` =  %s AND districtId = %s" %(year,districtId)
    cursor.execute(sql)
    monthdata = cursor.fetchall()
    list = []
    for i in monthdata:
        list.append(i[0])
    count = 0
    if list:
        L = json.loads(list[0])
        i = 0
        for j in L:
            count = count + j['count']
            i = i + 1
            if i >= n:
                print("同期累计利润")
                print(count)
                return count
    print("同期累计利润")
    print(count)
    return count

def pid_profit(n,year, districtPid):
    '''
    经理的同期利润
    :param year:
    :param districtPid:
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT monthData FROM correspond_profit_setting WHERE `year` = %s AND districtId = 0 AND districtPid =  %s" % ( year, districtPid)
    cursor.execute(sql)
    monthdata = cursor.fetchall()
    list = []
    for i in monthdata:
        list.append(i[0])
    pid_sameTermPro = 0
    if list:
        L = json.loads(list[0])
        i = 0
        for j in L:
            pid_sameTermPro = pid_sameTermPro + j['count']
            i = i + 1
            if i >= n:
                print("同期累计利润额")
                print(pid_sameTermPro)
                return pid_sameTermPro
    print("大区经理同期累计利润额")
    print(pid_sameTermPro)
    return pid_sameTermPro

def company_resProfit(n,year):
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    sameTermPro = 0
    if pid:
        list = [i[0] for i in pid]

        for pid in list:
            pid_sameTermPro = pid_profit(n,year,pid)
            sameTermPro = sameTermPro + pid_sameTermPro
    print("公司同期累计利润额")
    print(sameTermPro)

def sum_cost(n,year,districtId):
    #累计同期费用额= 同期业绩*同期费用率
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(crspCostRate as CHAR) FROM cost_rate_setting WHERE companyId = %s AND `year` = %s AND districtId = %s" %(companyId,year,districtId)
    cursor.execute(sql)
    re = cursor.fetchall()
    l = []
    for i in re:
        l.append(i[0])
    if l:
        costRate = l[0]
    # print(costRate)
    else:
        costRate = 0
    total_sale = get_resSale(n,year,districtId)
    cost = total_sale * float(costRate) / 100
    print("同期累计费用")
    print(cost)


def pid_cost(n,year,districtPid):
    #累计同期费用额= 同期业绩*同期费用率
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(crspCostRate as CHAR) FROM cost_rate_setting WHERE companyId = %s AND `year` = %s AND districtId = 0 and districtPid = %s" %(companyId,year,districtPid)
    cursor.execute(sql)
    re = cursor.fetchall()
    l = []
    for i in re:
        l.append(i[0])
    if l:
        costRate = l[0]
    # print(costRate)
    else:
        costRate = 0
    total_sale = pid_resSale(n,year,districtPid)
    cost = total_sale * float(costRate) / 100
    print("大区经理同期累计费用")
    print(cost)
    return cost

def company_resCost(n,year):
    # 获取一级区域id
    db1 = pymysql.connect(**db_config2)
    cursor = db1.cursor()
    sql_id = "SELECT id FROM cfg_district WHERE company_id = %s AND parent_id = 0" % (companyId)
    cursor.execute(sql_id)
    pid = cursor.fetchall()
    sameTermCost = 0
    if pid:
        list = [i[0] for i in pid]

        for pid in list:
            pid_sameTermCost = pid_cost(n,year,pid)
            sameTermCost = sameTermCost + pid_sameTermCost
    print("公司同期累计费用额")
    print(sameTermCost)

if __name__ == "__main__":
    #累计同期业绩
    # get_resSale(10,2020,245)
    pid_resSale(12,2020,210)
    # company_resSale(12,2020)

    #累计同期利润额
    # sum_profit(1,2021,178)
    # pid_profit(3,2021,177)
    # company_resProfit(8,2020)

    #累计同期费用额
    # sum_cost(1,2020,178)
    # pid_cost(3,2021,177)
    # company_resCost(3,2021)