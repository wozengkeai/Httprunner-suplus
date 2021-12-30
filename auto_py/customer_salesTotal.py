# -*- coding: utf-8 -*-
# @Time : 2021/1/20 14:35
# @Author : zengxiaoyan
# @File : customer_salesTotal.py
from auto_py.get_token import get_token
from auto_py.header import get_time,get_uuid,get_sign
import requests
import pymysql
import datetime
from auto_py import gol,config
db_config = gol.get_value('db_config')
db_config1 = gol.get_value('db_config1')
db_config2 = gol.get_value('db_config2')
db_config3 = gol.get_value('db_config3')
host_app = gol.get_value('host_app')
companyId = gol.get_value('companyId')


"""
1.获取全部大区
2.循环进入每个大区
3.查询每个大区客户列表第一位客户的累计业绩
"""
def get_userInfo():
    '''
    获取用户信息
    :return:
    '''
    url = host_app + "/v2/user/userInfo"
    uuid = get_uuid()
    time = get_time()
    token = get_token()
    print(token)
    header = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "okhttp/3.12.3",
        "X-MMM-DeviceType": '1',
        "X-MMM-AppProject": "ability",
        "X-MMM-Sign": get_sign(time, uuid, token),
        "X-MMM-Timestamp": time,
        "X-MMM-Uuid": uuid,
        "X-MMM-AccessToken": token,
        "X-MMM-AppName": "com.mmm.ability"
    }
    body3 = {}
    re = requests.post(url, headers=header, json=body3)
    districts = re.json()['data']['user']['districts']
    idList = []
    uid = []
    for i in districts:
        if i['id'] == 0:
            idList.append(i['id'])
            uid.append(i['uid'])
        else:
            for y in i['users']:
                idList.append(y['id'])
                uid.append(y['uid'])
            # idList.append(i['users'][])
    print(idList)
    return idList,uid

def get_customer(pid,uid):
    '''
    获取客户列表
    :return:
    '''
    url = host_app + "/v1/sale/customer/list"
    uuid = get_uuid()
    time = get_time()
    token = get_token()
    month = datetime.datetime.now().month
    print(token)
    header = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "okhttp/3.12.3",
        "X-MMM-DeviceType": '1',
        "X-MMM-AppProject": "ability",
        "X-MMM-Sign": get_sign(time, uuid, token),
        "X-MMM-Timestamp": time,
        "X-MMM-Uuid": uuid,
        "X-MMM-AccessToken": token,
        "X-MMM-AppName": "com.mmm.ability"
    }
    body4 = {"districtId":pid,"lastId":0,"orderDesc":1,"orderType":1,"uid":uid,"year":2021,"filterRangeEnd":30,"month":month,"pageSize":10,"filterRangeStart":0}
    re = requests.post(url, headers=header, json=body4)

    customerId = re.json()['data']['items'][0]['customerId']
    performanceSum = re.json()['data']['items'][0]['performanceSum']
    print(customerId)
    return customerId,performanceSum

def get_saleSum(customerId,beginTime,endTime):
    '''
    数据库查询某客户的销售总额
    与大区无关
    :return:
    '''

    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    sql = "SELECT cast(IFNULL(SUM(total),0) as CHAR) FROM sale_source_data WHERE companyId = %s  and customerId = '%s' AND expressDate >= '%s' " \
          "AND expressDate < '%s'  " % (companyId,customerId,beginTime,endTime)
    cursor.execute(sql)
    total = cursor.fetchall()
    saleSum = []
    for i in total:
        saleSum.append(i[0])
    performanceSum = round(float(saleSum[0]) / 10000 ,2)
    print(performanceSum)
    return performanceSum

def check_performanceSum(beginTime,endTime):
    #登陆获取所有大区
    districtPid = get_userInfo()[0]
    uid = get_userInfo()[1]
    i = 0
    for pid in districtPid:
        #取第一位客户
        print(uid[i])
        customerId = get_customer(pid,uid[i])[0]
        performanceSum = get_customer(pid,uid[i])[1]
        print(customerId)
        saleSum = get_saleSum(customerId,beginTime,endTime)

        assert (performanceSum == saleSum)
        i = i+1



if __name__ == "__main__":
    # get_userInfo()
    # get_customer()
    # get_saleSum('3946559539544064','2021-03-01','2021-03-09')
    check_performanceSum('2021-03-01','2021-03-09')