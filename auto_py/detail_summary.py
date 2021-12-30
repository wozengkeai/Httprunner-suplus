# -*- coding: utf-8 -*-
# @Time : 2021/3/9 9:53
# @Author : zengxiaoyan
# @File : detail_summary.py
from auto_py.get_token import get_token
from auto_py.header import get_time,get_uuid,get_sign
import requests
import pymysql
import datetime
from auto_py import gol,config
from auto_py.sum_correspond import company_resSale,company_resCost,company_resProfit
db_config = gol.get_value('db_config')
db_config1 = gol.get_value('db_config1')
db_config2 = gol.get_value('db_config2')
db_config3 = gol.get_value('db_config3')
host_app = gol.get_value('host_app')
companyId = gol.get_value('companyId')

year = datetime.datetime.now().year
month = datetime.datetime.now().month

def get_userInfo():
    '''
    获取用户信息
    :return:
    '''
    url = host_app + "/v2/user/userInfo"
    uuid = get_uuid()
    time = get_time()
    token = get_token()
    # print(token)
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
    print(idList,uid)
    return idList,uid

def detail_summary(n):
    '''
    获取详情页
    :return:
    '''
    user = get_userInfo()
    districtId = user[0]
    uid = user[1]

    url = host_app + "/v2/sale/main/detail"
    uuid = get_uuid()
    time = get_time()
    token = get_token()
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

    body = {"districtId":districtId[0],"uid":uid[0],"year":year,"month":month}
    re = requests.post(url, headers=header, json=body)
    cost = re.json()['data']['summary']['cost']
    performance = re.json()['data']['summary']['performance']
    profit = re.json()['data']['summary']['profit']
    # print(costDetail)

    sameTermPerf = company_resSale(n,year)
    # comp_sameTermP = "{:.2f}".format(float(sameTermPerf) / 10000)
    comp_sameTermP = round(float(sameTermPerf) / 10000 , 2)
    print(comp_sameTermP)
    sameTermYearSum = round(float(performance['sameTermYearSum']) , 2)
    assert (comp_sameTermP == sameTermYearSum)

    sameTermCost = company_resCost(n,year)
    comp_sameTermC = round(float(sameTermCost) / 10000 , 2)
    sameTermYearSum = round(float(cost['sameTermYearSum']), 2)
    assert (comp_sameTermC == sameTermYearSum)




if __name__ == "__main__":
    # get_userInfo()
    detail_summary(3)