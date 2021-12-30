# -*- coding: utf-8 -*-
# @Time : 2021/2/7 15:08
# @Author : zengxiaoyan
# @File : get_token.py
import requests
from auto_py.header import get_sign,get_uuid,get_time
from auto_py import gol,config
host_ucenter = gol.get_value('host_ucenter')
host_app = gol.get_value('host_app')
phone = gol.get_value('phone')
psw = gol.get_value('psw')
def get_token():
    loginAggregate_url = host_ucenter + "/ucenter/v2/auth/loginAggregate"
    authorize_url = host_app + "/v1/auth/authorize"
    accessToken_url = host_app + "/v1/auth/accessToken"
    # userInfo_url = "http://suplus-app-gateway-test.fjmaimaimai.com/v2/user/userInfo"
    uuid = get_uuid()
    # print(uuid)
    time = get_time()
    token = ''
    # 获取cuid和muid
    header = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "okhttp/3.12.3",
        "X-MMM-DeviceType": '1',
        "X-MMM-AppProject": "ability",
        "X-MMM-Sign": get_sign(time, uuid, token),
        "X-MMM-Timestamp": time,
        "X-MMM-Uuid": uuid,
        "AccessToken": ""
    }
    # phone = '13800000052'
    # psw = '7c4a8d09ca3762af61e59520943dc26494f8941b'
    body = {"grantType": "signInPassword", "phone": phone, "clientId": "lks3Z8Ncn2j",
            "password": psw}
    # se = requests.session()
    re = requests.post(loginAggregate_url, headers=header, json=body)
    result = re.json()["data"]
    cuid = result["cuid"]
    muid = result["companys"][0]["muid"]
    credentials = result["credentials"]
    # print(cuid,muid,credentials)

    # 获取authcode
    uuid = get_uuid()
    # print(uuid)
    time = get_time()
    header1 = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "okhttp/3.12.3",
        "X-MMM-DeviceType": '1',
        "X-MMM-AppProject": "ability",
        "X-MMM-AppName": "com.mmm.ability",
        "X-MMM-Sign": get_sign(time, uuid, token),
        "X-MMM-Timestamp": time,
        "X-MMM-Uuid": uuid,
        "AccessToken": ""
    }
    body1 = {"cid": 382, "cuid": cuid, "muid": muid, "credentials": credentials, "clientId": "lks3Z8Ncn2j"}
    # print(body1)
    # se.headers.update(header1)
    # print(header1)
    re1 = requests.post(authorize_url, headers=header1, json=body1)
    authCode = re1.json()["data"]["authCode"]
    # print(authCode)

    # 获取token
    uuid = get_uuid()
    time = get_time()
    header2 = {
        "Content-Type": "application/json;charset=utf-8",
        "User-Agent": "okhttp/3.12.3",
        "X-MMM-DeviceType": '1',
        "X-MMM-AppProject": "ability",
        "X-MMM-AppName": "com.mmm.ability",
        "X-MMM-Sign": get_sign(time, uuid, token),
        "X-MMM-Timestamp": time,
        "X-MMM-Uuid": uuid,
        # "AccessToken": token
    }
    # requests.headers.update(h)
    body2 = {"clientSecret": "gtfhyjukiol3Qncbvmdwe67khh", "clientId": "lks3Z8Ncn2j", "authCode": authCode}
    re2 = requests.post(accessToken_url, headers=header2, json=body2)
    accessToken = re2.json()["data"]["accessToken"]
    # print(accessToken)
    return accessToken

if __name__ == "__main__":
    get_token()