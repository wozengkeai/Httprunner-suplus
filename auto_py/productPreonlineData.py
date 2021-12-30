# -*- coding: utf-8 -*-
# @Time : 2021/5/31 11:47
# @Author : zengxiaoyan
# @File : productPreonlineData.py
'''
品项销售额/毛利额，接口返回值校验
'''
import datetime
import calendar
import re
from auto_py import gol,config
from auto_py.sum_product import perform_and_profit
from auto_py.calculatorPreonlineData import get_districtId_districtPid
import pymysql
from decimal import Decimal, ROUND_HALF_UP
db_config = gol.get_value('db_config')
db_config2 = gol.get_value('db_config2')
companyId = gol.get_value('companyId')

def get_product_district(data):
    '''
    获取品项有权限区域
    :param items:
    :return:
    '''
    items = data['items']
    print(items)

    district_list = []
    for i in items:
        item = []
        district_dict = {}
        if i['status'] == 1:
            item.append(i['id'])
            district_dict['districtIds'] = item

            # print(district_dict)
            district_list.append(district_dict)
    print(district_list)
    return district_list

def get_product_district_db(uid):
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    sql = "SELECT IFNULL(group_concat(relative_ids),-1) from role_permission_spec WHERE company_id = %s AND `name` = 'dataItem' AND uid = '%s' " % (companyId,uid)
    sql_admin = "SELECT admin_type FROM user_info WHERE company_id = %s AND uid = '%s'" % (companyId,uid)
    sql_allDistrict = "SELECT id FROM cfg_district WHERE company_id = %s AND enabled = 1" %(companyId)
    #判断主管理员
    cursor.execute(sql_admin)
    adminType = cursor.fetchall()
    adminType = [i[0] for i in adminType]
    # print(adminType)
    if adminType[0] == 1:
        #主管理有全部区域权限
        cursor.execute(sql_allDistrict)
        data = cursor.fetchall()
        # print(data)
        items = [i[0] for i in data]
        # print(items)
    else:
        cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)
        district = [i[0] for i in data]

        # items = []
        # if district[0] == None:
        #     items.append(-1)
        # else:
        items = [int(s) for s in re.findall(r'-?\d+',district[0])]
        items.append(-1)
        items = list(set(items))
    # print(items)

    district_list = []
    for i in items:
        item = []
        district_dict = {}
        item.append(i)
        district_dict['districtIds'] = item

        district_list.append(district_dict)
    # print(district_list)
    return district_list




def get_beginTime_and_endTime():
    '''
    根据当前时间获取当前营销年，起始时间与结束时间
    :return:
    '''
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT startYear,startMonth,endYear,endMonth FROM sale_cycle WHERE companyId = %s" % (companyId)
    cursor.execute(sql)
    data = cursor.fetchall()
    timedata = [i for i in data]
    # print(timedata)
    current = datetime.datetime.now().year
    # print(type(current))
    if timedata[0][0] == 1:
        beginYear = current
    else:
        beginYear = current - 1

    if timedata[0][2] == 1:
        endYear = current
    else:
        endYear = current + 1

    beginMonth = timedata[0][1]
    endMonth = timedata[0][3]

    end = calendar.monthrange(int(endYear), int(endMonth))[1]  # 获取当前年月的当月天数
    start_date = '%s-%s-01' % (beginYear, beginMonth)  # 第一天
    end_date = '%s-%s-%s' % (endYear, endMonth, end)  # 最后一天
    print(start_date)
    print(end_date)
    return start_date,end_date
def round_dec(n, d=2):
    s = '0.' + '0' * d
    return Decimal(str(n)).quantize(Decimal(s), ROUND_HALF_UP)

def checkProduct(data,districtIds,uid):
    '''
    校验某区域接口下发业绩额/销售额与计算比对
    :param productItems:
    :return:
    '''
    #接口返回值
    productItems = data['items']
    count = data['count']
    # count = 84
    if count == 0:
        c = 0
    else:
        productData = []
        for i in productItems:
            item = []
            item.append(i['id'])
            item.append(round(float(i['saleSum']), 2))   #销售额
            item.append(round(float(i['grossProfitSum']), 2))   #毛利额
            item.append(round(float(i['grossProfitRatio']), 2))   #毛利率
            item.append(round(float(i['saleSumPercent']), 2))  # 销售额占比
            item.append(round(float(i['grossProfitSumPercent']), 2))  # 毛利额占比
            productData.append(item)

        #筛选区域
        if districtIds[0] == -1:
            #仅看自己
            productDistrictId = 0
            uid = uid
        else:
            productDistrictId = districtIds[0]
            uid = 0

        #获取区域
        if productDistrictId == 0:
            #公司和个人
            districtId = 0
            districtPid = 0

        else:
            district = get_districtId_districtPid(productDistrictId)
            districtId = district[0]
            districtPid = district[1]

        #获取营销年时间范围
        sale_cycle = get_beginTime_and_endTime()
        beginTime = sale_cycle[0]
        endTime = sale_cycle[1]

        #计算值

        #销售额倒叙
        print(districtId,districtPid,beginTime,endTime,uid)
        perfAndProf = perform_and_profit(districtId,districtPid,beginTime,endTime,uid)
        print(perfAndProf)
        grossprofitRatioList = []
        for i in range(0, count):
            if float(perfAndProf[i][1]) <= 0:
                grossprofitRatio = 0
            else:
                grossprofitRatio = round(perfAndProf[i][3] / float(perfAndProf[i][1]) * 100, 2)
            grossprofitRatioList.append(grossprofitRatio)

        for i in perfAndProf:
            # i[1] = round(float(i[1]) / 10000, 2)
            i[1] = float(round_dec(float(i[1]) / 10000))
            i[3] = float(round_dec(i[3] / 10000))

        #校验
        sale = 0
        prof = 0
        ratio = 0
        saleRatio = 0
        profitRatio = 0
        for i in range(0,count):

            # print("------------------- %s",i)
            # print(productData[i][2])
            # print(perfAndProf[i][3])
            if productData[i][1] == perfAndProf[i][1]:  #业绩额
                sale = sale + 1

            if productData[i][2] == perfAndProf[i][3]:  #毛利额
                prof = prof + 2

            # print(grossprofitRatioList[i])
            if productData[i][3] == grossprofitRatioList[i]:   #毛利率
                ratio = ratio + 3
            if productData[i][4] == perfAndProf[i][4]:   #销售额占比
                saleRatio = saleRatio + 4

            # print(productData[i][5])
            # print(perfAndProf[i][5])
            if productData[i][5] == perfAndProf[i][5]:   #毛利额占比
                profitRatio = profitRatio + 5


        c = sale + prof + ratio + saleRatio + profitRatio
    print(c)

    if c == 15 * count:
        msg = "ok"
    else:
        msg = "fail"
    print(msg)
    return msg







if __name__ == "__main__":
#     # get_beginTime_and_endTime()
        get_product_district_db('3252348558521088')
#     data = [{"id":3668422952550400,"name":"素华千耶豆腐2kg*6包","status":1,"tags":[],"saleSumPercent":"9.57","grossProfitSum":"16.17","saleSum":"39.6","grossProfitSumPercent":"14.72","grossProfitRatio":"40.83"},{"id":3668422955155456,"name":"素天下果蔬串(混合味)825g*15串*10包","status":1,"tags":[],"saleSumPercent":"8.91","grossProfitSum":"8.35","saleSum":"36.89","grossProfitSumPercent":"7.6","grossProfitRatio":"22.64"},{"id":3668422953959424,"name":"福临天下百叶大四喜串1.32kg*30串*10包","status":1,"tags":[],"saleSumPercent":"8.42","grossProfitSum":"11.36","saleSum":"34.87","grossProfitSumPercent":"10.34","grossProfitRatio":"32.57"},{"id":3668422955270144,"name":"素天下南瓜饼串600g*10串*10包","status":1,"tags":[],"saleSumPercent":"5.35","grossProfitSum":"3.17","saleSum":"22.16","grossProfitSumPercent":"2.88","grossProfitRatio":"14.29"},{"id":3303937416740864,"name":"素天下素牛板筋800g*20包","status":1,"tags":[],"saleSumPercent":"4.78","grossProfitSum":"1.11","saleSum":"19.79","grossProfitSumPercent":"1.01","grossProfitRatio":"5.61"},{"id":3668422952599552,"name":"素华千耶豆腐400g*30包","status":1,"tags":[],"saleSumPercent":"4.68","grossProfitSum":"7.92","saleSum":"19.39","grossProfitSumPercent":"7.21","grossProfitRatio":"40.83"},{"id":3668422957383680,"name":"福美鲜食品豆腐丝2.5kg*4包","status":1,"tags":[],"saleSumPercent":"4.25","grossProfitSum":"3.55","saleSum":"17.58","grossProfitSumPercent":"3.23","grossProfitRatio":"20.19"},{"id":3668422953041920,"name":"素华千耶大四喜1.32kg*30串*10包","status":1,"tags":[],"saleSumPercent":"4.08","grossProfitSum":"5.14","saleSum":"16.87","grossProfitSumPercent":"4.68","grossProfitRatio":"30.47"},{"id":3668422952665088,"name":"素华千耶豆腐(加长)2kg*6包","status":1,"tags":[],"saleSumPercent":"2.9","grossProfitSum":"4.9","saleSum":"12","grossProfitSumPercent":"4.46","grossProfitRatio":"40.83"},{"id":4111096275681280,"name":"素天下大南瓜饼40片*4包","status":1,"tags":[],"saleSumPercent":"2.37","grossProfitSum":"1.69","saleSum":"9.79","grossProfitSumPercent":"1.54","grossProfitRatio":"17.27"},{"id":3668422955483136,"name":"素华米果串(混合味)825g*15串*10包","status":1,"tags":[],"saleSumPercent":"2.35","grossProfitSum":"2.17","saleSum":"9.71","grossProfitSumPercent":"1.97","grossProfitRatio":"22.31"},{"id":3668422952747008,"name":"素华千耶豆腐(三角形)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"2.31","grossProfitSum":"0.73","saleSum":"9.58","grossProfitSumPercent":"0.66","grossProfitRatio":"7.63"},{"id":3668422955810816,"name":"素天下豆腐丝(五香)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"2.13","grossProfitSum":"2.33","saleSum":"8.83","grossProfitSumPercent":"2.12","grossProfitRatio":"26.41"},{"id":3668422954287104,"name":"标餐工坊千耶豆腐2.5kg*4包","status":1,"tags":[],"saleSumPercent":"1.62","grossProfitSum":"0.8","saleSum":"6.7","grossProfitSumPercent":"0.73","grossProfitRatio":"11.94"},{"id":3303937415200768,"name":"素天下手撕素牛肉(孜然味)72g*50包","status":1,"tags":[],"saleSumPercent":"1.6","grossProfitSum":"2.53","saleSum":"6.64","grossProfitSumPercent":"2.31","grossProfitRatio":"38.16"},{"id":3668422953353216,"name":"福临天下百叶豆腐400g*30包","status":1,"tags":[],"saleSumPercent":"1.54","grossProfitSum":"2.99","saleSum":"6.37","grossProfitSumPercent":"2.72","grossProfitRatio":"46.97"},{"id":3755362714288128,"name":"素天下什锦素包300g*12包","status":1,"tags":[],"saleSumPercent":"1.5","grossProfitSum":"0.91","saleSum":"6.21","grossProfitSumPercent":"0.83","grossProfitRatio":"14.72"},{"id":3668422953877504,"name":"福临天下百叶豆腐串960g*30串*10包","status":1,"tags":[],"saleSumPercent":"1.37","grossProfitSum":"2.5","saleSum":"5.65","grossProfitSumPercent":"2.28","grossProfitRatio":"44.27"},{"id":3303937417117696,"name":"素天下素毛肚(奥尔良味)78g*50包","status":1,"tags":[],"saleSumPercent":"1.32","grossProfitSum":"2.14","saleSum":"5.46","grossProfitSumPercent":"1.94","grossProfitRatio":"39.1"},{"id":3829252351033344,"name":"素天下包浆豆腐串20串*10包","status":1,"tags":[],"saleSumPercent":"1.32","grossProfitSum":"1.03","saleSum":"5.45","grossProfitSumPercent":"0.94","grossProfitRatio":"18.9"},{"id":3668422952091648,"name":"素天下百叶豆腐(加长)2kg*6包","status":1,"tags":[],"saleSumPercent":"1.31","grossProfitSum":"2.4","saleSum":"5.44","grossProfitSumPercent":"2.18","grossProfitRatio":"44.12"},{"id":3668422953140224,"name":"聚味园千耶豆腐400g*30包","status":1,"tags":[],"saleSumPercent":"1.3","grossProfitSum":"1.85","saleSum":"5.4","grossProfitSumPercent":"1.68","grossProfitRatio":"34.26"},{"id":4197150335172608,"name":"素天下酱卤豆腐丝(5cm)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"1.3","grossProfitSum":"1.14","saleSum":"5.4","grossProfitSumPercent":"1.04","grossProfitRatio":"21.11"},{"id":3668422953926656,"name":"福临天下百叶豆腐(原味)(正方形)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"1.17","grossProfitSum":"1.38","saleSum":"4.86","grossProfitSumPercent":"1.26","grossProfitRatio":"28.4"},{"id":3668422954369024,"name":"福美鲜食品百叶豆腐(正方形)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"1.13","grossProfitSum":"0.31","saleSum":"4.66","grossProfitSumPercent":"0.28","grossProfitRatio":"6.6"},{"id":3668422952714240,"name":"素华千耶豆腐(正方形)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"1.01","grossProfitSum":"0.51","saleSum":"4.17","grossProfitSumPercent":"0.46","grossProfitRatio":"12.24"},{"id":3303937416953856,"name":"素天下素毛肚(奥尔良味)180g*30包","status":1,"tags":[],"saleSumPercent":"0.98","grossProfitSum":"0.22","saleSum":"4.04","grossProfitSumPercent":"0.2","grossProfitRatio":"5.56"},{"id":3303937415233536,"name":"素天下手撕素牛肉(黑胡椒味)72g*50包","status":1,"tags":[],"saleSumPercent":"0.95","grossProfitSum":"1.52","saleSum":"3.95","grossProfitSumPercent":"1.38","grossProfitRatio":"38.45"},{"id":3303937417068544,"name":"素天下素毛肚(香辣味)78g*50包","status":1,"tags":[],"saleSumPercent":"0.87","grossProfitSum":"1.35","saleSum":"3.59","grossProfitSumPercent":"1.23","grossProfitRatio":"37.52"},{"id":3668422958366720,"name":"福临天下素切花海参串(原味)(大)1.05kg*20串*6包","status":1,"tags":[],"saleSumPercent":"0.75","grossProfitSum":"0.81","saleSum":"3.1","grossProfitSumPercent":"0.73","grossProfitRatio":"26"},{"id":3668422955843584,"name":"素天下酱卤豆腐丝280g*30包","status":1,"tags":[],"saleSumPercent":"0.74","grossProfitSum":"1.23","saleSum":"3.07","grossProfitSumPercent":"1.12","grossProfitRatio":"40"},{"id":3303937418067968,"name":"惠宜素毛肚(香辣味)180g*20包","status":1,"tags":[],"saleSumPercent":"0.66","grossProfitSum":"0.16","saleSum":"2.71","grossProfitSumPercent":"0.15","grossProfitRatio":"5.91"},{"id":3303937418182656,"name":"惠宜素卤百叶(五香味)200g*20包","status":1,"tags":[],"saleSumPercent":"0.64","grossProfitSum":"0.96","saleSum":"2.65","grossProfitSumPercent":"0.88","grossProfitRatio":"36.43"},{"id":3914211418357760,"name":"素天下素荔枝肉(蛋奶素)230g*20包","status":1,"tags":[],"saleSumPercent":"0.63","grossProfitSum":"0.63","saleSum":"2.62","grossProfitSumPercent":"0.57","grossProfitRatio":"23.91"},{"id":3668422954696704,"name":"素天下日式福棉豆腐350g*20包","status":1,"tags":[],"saleSumPercent":"0.63","grossProfitSum":"0.93","saleSum":"2.62","grossProfitSumPercent":"0.85","grossProfitRatio":"35.5"},{"id":3668422953172992,"name":"聚味园千耶豆腐2kg*6包","status":1,"tags":[],"saleSumPercent":"0.6","grossProfitSum":"0.73","saleSum":"2.5","grossProfitSumPercent":"0.66","grossProfitRatio":"29"},{"id":3668422952157184,"name":"素天下百叶豆腐(原味)(商超)200g*36包","status":1,"tags":[],"saleSumPercent":"0.6","grossProfitSum":"0.88","saleSum":"2.49","grossProfitSumPercent":"0.8","grossProfitRatio":"35.44"},{"id":3668422953222144,"name":"聚味园千耶豆腐(原味)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"0.54","grossProfitSum":"0.19","saleSum":"2.26","grossProfitSumPercent":"0.17","grossProfitRatio":"8.43"},{"id":3303937413840896,"name":"素天下竹耳露800g*12罐","status":1,"tags":[],"saleSumPercent":"0.53","grossProfitSum":"0.83","saleSum":"2.2","grossProfitSumPercent":"0.76","grossProfitRatio":"37.82"},{"id":3668422954958848,"name":"素华千耶豆腐(0.5片)2.5kg*4","status":1,"tags":[],"saleSumPercent":"0.52","grossProfitSum":"0.3","saleSum":"2.16","grossProfitSumPercent":"0.27","grossProfitRatio":"13.89"},{"id":3374700302991360,"name":"素华素毛肚(原味)1kg*10包","status":1,"tags":[],"saleSumPercent":"0.51","grossProfitSum":"0.5","saleSum":"2.1","grossProfitSumPercent":"0.46","grossProfitRatio":"23.81"},{"id":3668422955352064,"name":"素天下紫薯饼串600g*10串*10包","status":1,"tags":[],"saleSumPercent":"0.51","grossProfitSum":"0.33","saleSum":"2.1","grossProfitSumPercent":"0.3","grossProfitRatio":"15.71"},{"id":3668422954319872,"name":"餐库千耶豆腐(0.5片)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"0.5","grossProfitSum":"0.24","saleSum":"2.07","grossProfitSumPercent":"0.22","grossProfitRatio":"11.59"},{"id":3303937414234112,"name":"素天下素卤百叶(香辣味)400g*20包","status":1,"tags":[],"saleSumPercent":"0.48","grossProfitSum":"0.31","saleSum":"1.98","grossProfitSumPercent":"0.29","grossProfitRatio":"15.83"},{"id":3668422954156032,"name":"鸿创嘉品千耶豆腐(正方形)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"0.46","grossProfitSum":"0.12","saleSum":"1.92","grossProfitSumPercent":"0.11","grossProfitRatio":"6.25"},{"id":3303937417199616,"name":"素天下素毛肚(奥尔良味)1kg*10包","status":1,"tags":[],"saleSumPercent":"0.46","grossProfitSum":"0.28","saleSum":"1.89","grossProfitSumPercent":"0.25","grossProfitRatio":"14.76"},{"id":3668422954237952,"name":"余老师千耶豆腐2kg*6包","status":1,"tags":[],"saleSumPercent":"0.43","grossProfitSum":"0.36","saleSum":"1.8","grossProfitSumPercent":"0.33","grossProfitRatio":"20"},{"id":3820721089773568,"name":"素天下老坛酸菜包300g*12包","status":1,"tags":[],"saleSumPercent":"0.43","grossProfitSum":"0.35","saleSum":"1.79","grossProfitSumPercent":"0.32","grossProfitRatio":"19.44"},{"id":3979142891438080,"name":"素天下红油素毛肚150g*20包","status":1,"tags":[],"saleSumPercent":"0.41","grossProfitSum":"0.34","saleSum":"1.71","grossProfitSumPercent":"0.31","grossProfitRatio":"19.79"},{"id":3668422952894464,"name":"素华千耶豆腐串960g*30串*10包","status":1,"tags":[],"saleSumPercent":"0.41","grossProfitSum":"0.65","saleSum":"1.69","grossProfitSumPercent":"0.59","grossProfitRatio":"38.46"},{"id":3668422954123264,"name":"鸿创嘉品千耶豆腐2kg*6包","status":1,"tags":[],"saleSumPercent":"0.4","grossProfitSum":"0.24","saleSum":"1.66","grossProfitSumPercent":"0.22","grossProfitRatio":"14.46"},{"id":3303937418264576,"name":"惠宜手撕素牛肉(黑胡椒味)150g*20包","status":1,"tags":[],"saleSumPercent":"0.39","grossProfitSum":"0.38","saleSum":"1.6","grossProfitSumPercent":"0.34","grossProfitRatio":"23.71"},{"id":3668422954663936,"name":"素天下日式翡翠豆腐350g*20包","status":1,"tags":[],"saleSumPercent":"0.36","grossProfitSum":"0.49","saleSum":"1.5","grossProfitSumPercent":"0.44","grossProfitRatio":"32.42"},{"id":3668422955450368,"name":"素华南瓜饼串600g*10串*10包","status":1,"tags":[],"saleSumPercent":"0.35","grossProfitSum":"0.27","saleSum":"1.45","grossProfitSumPercent":"0.25","grossProfitRatio":"18.62"},{"id":3708781655228416,"name":"素天下素三杯鸡(蛋奶素) 200g*20包","status":1,"tags":[],"saleSumPercent":"0.33","grossProfitSum":"0.49","saleSum":"1.35","grossProfitSumPercent":"0.45","grossProfitRatio":"36.23"},{"id":3303937418215424,"name":"惠宜手撕素牛肉(孜然味)150g*20包","status":1,"tags":[],"saleSumPercent":"0.3","grossProfitSum":"0.28","saleSum":"1.25","grossProfitSumPercent":"0.25","grossProfitRatio":"22.44"},{"id":3303937416658944,"name":"素天下精品素百页350g*20包","status":1,"tags":[],"saleSumPercent":"0.3","grossProfitSum":"0.66","saleSum":"1.22","grossProfitSumPercent":"0.6","grossProfitRatio":"53.92"},{"id":3303937417871360,"name":"聚味园素天府毛肚2.3kg*5包","status":1,"tags":[],"saleSumPercent":"0.29","grossProfitSum":"0.26","saleSum":"1.2","grossProfitSumPercent":"0.24","grossProfitRatio":"21.67"},{"id":3303937414070272,"name":"素天下素卤百叶(五香味)200g*30包","status":1,"tags":[],"saleSumPercent":"0.27","grossProfitSum":"0.31","saleSum":"1.11","grossProfitSumPercent":"0.28","grossProfitRatio":"28.05"},{"id":3668422958284800,"name":"素天下素海参200g*10包","status":1,"tags":[],"saleSumPercent":"0.27","grossProfitSum":"0.52","saleSum":"1.1","grossProfitSumPercent":"0.47","grossProfitRatio":"47.27"},{"id":3303937414709248,"name":"素天下手撕素牛肉(孜然味)1kg*10包","status":1,"tags":[],"saleSumPercent":"0.25","grossProfitSum":"0.16","saleSum":"1.05","grossProfitSumPercent":"0.14","grossProfitRatio":"14.76"},{"id":3668422958465024,"name":"福临天下清水面筋串1.05kg*30串*6包","status":1,"tags":[],"saleSumPercent":"0.25","grossProfitSum":"0.23","saleSum":"1.04","grossProfitSumPercent":"0.21","grossProfitRatio":"22.5"},{"id":3668422955991040,"name":"素天下卤百叶(五香片)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"0.24","grossProfitSum":"0.28","saleSum":"0.98","grossProfitSumPercent":"0.26","grossProfitRatio":"28.92"},{"id":3708759395811328,"name":"素天下什锦烤麸 200g*20包","status":1,"tags":[],"saleSumPercent":"0.23","grossProfitSum":"0.13","saleSum":"0.94","grossProfitSumPercent":"0.12","grossProfitRatio":"14"},{"id":3708769106132992,"name":"素天下茶油香菇200g*20包","status":1,"tags":[],"saleSumPercent":"0.2","grossProfitSum":"0.08","saleSum":"0.82","grossProfitSumPercent":"0.07","grossProfitRatio":"10"},{"id":3668422955565056,"name":"素华紫薯饼串(有馅)10串*10包","status":1,"tags":[],"saleSumPercent":"0.18","grossProfitSum":"0.16","saleSum":"0.75","grossProfitSumPercent":"0.15","grossProfitRatio":"21.33"},{"id":3303937417707520,"name":"聚味园素天山毛肚(白色)(新)500g*20包","status":1,"tags":[],"saleSumPercent":"0.18","grossProfitSum":"0.07","saleSum":"0.73","grossProfitSumPercent":"0.06","grossProfitRatio":"9.18"},{"id":3681006486175744,"name":"素天下百叶豆腐2kg*6包","status":1,"tags":[],"saleSumPercent":"0.16","grossProfitSum":"0.3","saleSum":"0.68","grossProfitSumPercent":"0.27","grossProfitRatio":"44.12"},{"id":3668422958546944,"name":"聚味园素日式深海鲍鱼210g*10包","status":1,"tags":[],"saleSumPercent":"0.16","grossProfitSum":"0.31","saleSum":"0.67","grossProfitSumPercent":"0.28","grossProfitRatio":"45.99"},{"id":3303937413988352,"name":"素天下素卤百叶(五香味)(空白袋不干胶)400g*30包","status":1,"tags":[],"saleSumPercent":"0.15","grossProfitSum":"0.14","saleSum":"0.64","grossProfitSumPercent":"0.13","grossProfitRatio":"22.53"},{"id":3914219409522688,"name":"素天下素姜母鸭(蛋奶素)200g*20包","status":1,"tags":[],"saleSumPercent":"0.15","grossProfitSum":"0.23","saleSum":"0.62","grossProfitSumPercent":"0.21","grossProfitRatio":"37.68"},{"id":3303937414283264,"name":"素天下素卤百叶(五香味)400g*20包","status":1,"tags":[],"saleSumPercent":"0.13","grossProfitSum":"0.1","saleSum":"0.54","grossProfitSumPercent":"0.09","grossProfitRatio":"19.17"},{"id":3303937416691712,"name":"素天下素羊肚丝210g*20包","status":1,"tags":[],"saleSumPercent":"0.13","grossProfitSum":"0.29","saleSum":"0.52","grossProfitSumPercent":"0.27","grossProfitRatio":"56.41"},{"id":3759640118820864,"name":"素天下素卤百叶(香辣味)(单层彩袋)200g*40包","status":1,"tags":[],"saleSumPercent":"0.1","grossProfitSum":"0.04","saleSum":"0.42","grossProfitSumPercent":"0.04","grossProfitRatio":"9.74"},{"id":3303937417756672,"name":"聚味园素天山毛肚(白色)(旧)2.5kg*5包","status":1,"tags":[],"saleSumPercent":"0.08","grossProfitSum":"-0.07","saleSum":"0.33","grossProfitSumPercent":"-0.06","grossProfitRatio":"-20"},{"id":3668422953304064,"name":"聚味园千耶豆腐串(长签)960g*30串*10包","status":1,"tags":[],"saleSumPercent":"0.07","grossProfitSum":"0.1","saleSum":"0.31","grossProfitSumPercent":"0.09","grossProfitRatio":"33"},{"id":3303937414119424,"name":"素天下素卤百叶(香辣味)200g*30包","status":1,"tags":[],"saleSumPercent":"0.07","grossProfitSum":"0.04","saleSum":"0.29","grossProfitSumPercent":"0.04","grossProfitRatio":"13.68"},{"id":4192862269685760,"name":"素天下素牛板筋(7MM)800g*20包","status":1,"tags":[],"saleSumPercent":"0.04","grossProfitSum":"-0.01","saleSum":"0.17","grossProfitSumPercent":"-0.01","grossProfitRatio":"-6"},{"id":4192917060960256,"name":"素华包浆素鸡串20串*15包","status":1,"tags":[],"saleSumPercent":"0.04","grossProfitSum":"0.02","saleSum":"0.15","grossProfitSumPercent":"0.02","grossProfitRatio":"14"},{"id":3668422955614208,"name":"素天下玉米饼串10串*10包","status":1,"tags":[],"saleSumPercent":"0.03","grossProfitSum":"0.02","saleSum":"0.14","grossProfitSumPercent":"0.02","grossProfitRatio":"12.86"},{"id":3668422957039616,"name":"素华千耶豆腐(三角形/油炸)2.5kg*4包","status":1,"tags":[],"saleSumPercent":"0.02","grossProfitSum":"0.02","saleSum":"0.1","grossProfitSumPercent":"0.02","grossProfitRatio":"23"},{"id":3691848280211456,"name":"素天下素卤百叶(香辣味)400g*30包","status":1,"tags":[],"saleSumPercent":"0.02","grossProfitSum":"0.01","saleSum":"0.09","grossProfitSumPercent":"0.01","grossProfitRatio":"16.13"},{"id":3719997510860800,"name":"素天下三鲜素饺 300g*14包","status":1,"tags":[],"saleSumPercent":"0.01","grossProfitSum":"0.01","saleSum":"0.03","grossProfitSumPercent":"0.01","grossProfitRatio":"28.15"},{"id":3719999874121728,"name":"素天下菌菇素饺300g*14包","status":1,"tags":[],"saleSumPercent":"0.01","grossProfitSum":"0.01","saleSum":"0.03","grossProfitSumPercent":"0","grossProfitRatio":"20"}]
#     checkProduct(data,[37],'3208804147757824')
#
#
#     # get_product_district_db('3208804147757824')