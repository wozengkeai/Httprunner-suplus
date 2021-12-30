# -*- coding: utf-8 -*-
# @Time : 2021/5/18 11:28
# @Author : zengxiaoyan
# @File : calculatorPreonlineData.py
'''
小工具区域业绩/利润，单客户业绩/利润，接口返回值校验
'''
from auto_py import gol,config
import pymysql
import calendar
from auto_py.customer_product import customerSt


db_config2_preonline ={"host": "",
            "port": 3306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config2 = gol.get_value('db_config2')
companyId = gol.get_value('companyId')



def get_current_month_start_and_end(year,month):
    # year, month = str(date).split('.')[0], str(date).split('.')[1]  #分割字符串，提取年月
    end = calendar.monthrange(int(year), int(month))[1]            #获取当前年月的当月天数
    start_date = '%s-%s-01' %(year,month)    #第一天
    end_date = '%s-%s-%s' %(year,month,end)  #最后一天
    return start_date,end_date

def get_phone(uid):
    '''
    根据uid获取账号
    :param uid:
    :return:
    '''
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    sql = "SELECT phone FROM user_info WHERE uid = '%s' and enabled = 1" % (uid)
    cursor.execute(sql)
    phoneData = cursor.fetchall()
    phoneData = [i[0] for i in phoneData]
    # print(phoneData[0])
    return phoneData[0]

def get_districtId_districtPid(districtId_actual):
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    sql = "SELECT cast(parent_id as CHAR) FROM cfg_district WHERE company_id = %s AND id = %s AND enabled = 1" % (companyId,districtId_actual)
    cursor.execute(sql)
    parentId = cursor.fetchall()
    parentId = [i[0] for i in parentId]
    if parentId[0] == '0':
        # 一级大区
        districtPid = districtId_actual
        districtId = 0
    else:
        districtPid = int(parentId[0])
        districtId = districtId_actual
    # print(districtId,districtPid)
    return districtId,districtPid


def checkCorrespond(data,uid):
    year = data['year']
    # year = data[0]['year']
    # print(year)
    month = data['month']
    # month = data[0]['month']
    yearSt = str(int(year) - 1)
    currentDate = get_current_month_start_and_end(year, month)
    sameTimeDate = get_current_month_start_and_end(yearSt, month)
    nowDate = currentDate[0]
    beginTime = sameTimeDate[0]
    endTime = sameTimeDate[1]

    districtId_actual = data['districtId']
    # districtId_actual = data[0]['districtId']
    district = get_districtId_districtPid(districtId_actual)
    districtId = district[0]
    districtPid = district[1]



    #接口下发的总业绩和总利润
    correspondProfit = round(float(data['scheme']['correspondProfit']),2)
    correspondSale = round(float(data['scheme']['correspondSale']),2)
    # correspondProfit = round(float(data[0]['scheme']['correspondProfit']), 2)
    # correspondSale = round(float(data[0]['scheme']['correspondSale']), 2)

    # 自己计算的总业绩/利润
    correspondSum_except = customerSt(0,beginTime,endTime,districtId,districtPid,uid,nowDate)
    sale_except = round(float(correspondSum_except[0]),2)
    profit_except = round(float(correspondSum_except[1]),2)

    #
    sales = data['scheme']['sales']
    # sales = data[0]['scheme']['sales']
    onepersonCount = 0
    if sales:
        # no = len(sales)
        no = 0
        for i in sales:


            customerId = i['customerId']
            #不统计未挂在具体客户下的变动费用，接口有下发
            if customerId != 0:
                no = no + 1
                cor_sale = round(float(i['sale']['correspond']),2)
                cor_profit = round(float(i['profit']['correspond']),2)

                #自己计算单客户业绩/利润
                correspondOne_except = customerSt(customerId,beginTime,endTime,districtId,districtPid,uid,nowDate)
                oneSale_except = round(float(correspondOne_except[0]),2)
                oneProfit_except = round(float(correspondOne_except[1]),2)

                if cor_sale <= oneSale_except+1 and cor_sale >= oneSale_except-1 and cor_profit <= oneProfit_except+1 and cor_profit >= oneProfit_except-1:
                    onepersonCount = onepersonCount + 3
    else:
        # onepersonCount = 0
        no = 0

    # 校验

    count = onepersonCount
    if correspondSale <= sale_except+1 and correspondSale >= sale_except-1:
        count = count + 1
    if correspondProfit <= profit_except+1 and correspondProfit >= profit_except-1:
        count = count + 2
    if count == no * 3 + 3:
        msg = "ok"
    else:
        msg = 'fail'
    print(msg)
    print(count)
    return msg

# if __name__ == "__main__":
#     # get_phone('3247228580772352')
#     # get_districtId_districtPid(126)
#
#
#     data = [{"year":2021,"month":12,"districtId":178,"scheme":{"sales":[{"customerId":3865697253408768,"sale":{"correspond":"30000","current":"30000"},"profit":{"correspond":"0","current":"0"},"products":[{"productId":4092509320986624,"productNumber":{"correspond":"3000","current":"3000"},"productPrice":"0","promotionCost":{"type":1,"percent":"0","amount":0},"correspondInfo":{"number":"3000","price":"10","gift":{"number":"0","amount":"0","baseNum":"1","giftNum":"0"}},"number":"3000","price":"10","gift":{"number":"0","amount":"0","baseNum":"0","giftNum":"0"},"giftCost":{"correspond":{"number":"0","amount":"0"},"current":{"number":"0","amount":"0"}},"saleIncrement":"0","profitIncrement":"0","saleAmount":"30000","costPrice":"","productName":"鸡翅30","grossProfitRate":"-","recentMonthly":{"number":"3333","price":"10","gift":{"number":"500","amount":"0"},"costPrice":"0","saleAmount":"33330","profitAmount":"0"}}]},{"customerId":0,"sale":{"correspond":"0","current":"0"},"profit":{"correspond":"-200","current":"-200"},"products":[]}],"variableCost":[{"customerId":0,"costs":[{"costId":32,"costName":"物流费用","baseRate":"-","costAmount":200}]}],"regularCost":[{"costId":14,"costName":"工资福利","baseRate":"-","costAmount":200},{"costId":15,"costName":"奖金","baseRate":"-","costAmount":50}],"correspondSale":"30000","currentSale":"30000","correspondProfit":"-450","currentProfit":"-450","promotionCostSubject":'',"customers":[{"customerId":3865697253408768,"customerName":"客户6","type":1},{"customerId":3706128421945344,"customerName":"一级客户1","type":1},{"customerId":3707539039420416,"customerName":"一级客户3","type":1},{"customerId":3782269705584640,"customerName":"一级客户5","type":1},{"customerId":3905271874371584,"customerName":"客户7","type":1},{"customerId":3913816845402112,"customerName":"零星客户32","type":1},{"customerId":3918095220834304,"customerName":"零星－32","type":1},{"customerId":3939539609894912,"customerName":"小苏客户","type":1},{"customerId":3943956149764096,"customerName":"客户15新增","type":1},{"customerId":3946559539544064,"customerName":"客户-55","type":1},{"customerId":4027329750646784,"customerName":"再测一下","type":1}]}}]
#     checkCorrespond( data,'3252348558521088')