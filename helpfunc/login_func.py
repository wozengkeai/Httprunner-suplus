# @Time : 2020/3/11 10:47
# @Author : zengxiaoyan
# @File : login_func.py
import json


def teardown_hook_get_m_accesstoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        access_token = jsondata['data']['access']['token']
        print(access_token)
    try:
        # 保存token到文件
        with open('config/m_access_token.csv','w') as f:
            f.write(access_token)
            print('写入成功，access_token：{}'.format(access_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return access_token

def teardown_hook_get_m_refreshtoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        m_refresh_token =jsondata['data']['access']['refreshtoken']
    try:
        # 保存token到文件
        with open('config/m_refresh_token.csv','w') as f:
            f.write(m_refresh_token)
            print('写入成功，m_refresh_token：{}'.format(m_refresh_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return m_refresh_token

def get_m_accesstoken():
    try:
        with open('config/m_access_token.csv','r') as f:
            accseetoken_value = f.read()
            print('读取accseetoken_value成功：{}'.format(accseetoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    accseetoken_value = str(accseetoken_value)
    authorization = 'Bearer ' + accseetoken_value
    return authorization

def get_m_refreshtoken():
    try:
        with open('config/m_refresh_token.csv','r') as f:
            m_refreshtoken_value = f.read()
            print('读取m_refreshtoken_value成功：{}'.format(m_refreshtoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    m_refreshtoken_value = str(m_refreshtoken_value)
    authorization = 'bear ' + m_refreshtoken_value
    return authorization

def get_authcode():
    try:
        with open('config/authCode.csv','r') as f:
            authcode_value = f.read()
            print('读取authcode_value成功：{}'.format(authcode_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    authcode_value = str(authcode_value)
    return authcode_value

def teardown_hook_get_authcode(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        auth_code = jsondata['data']['authCode']
    try:
        # 保存token到文件
        with open('config/authCode.csv','w') as f:
            f.write(auth_code)
            print('写入成功，authCode：{}'.format(auth_code))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return auth_code

def teardown_hook_get_accesstoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        access_token =jsondata['data']['accessToken']
    try:
        # 保存token到文件
        with open('config/accessToken.csv','w') as f:
            f.write(access_token)
            print('写入成功，access_token：{}'.format(access_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return access_token

def get_accesstoken():
    try:
        with open('config/accessToken.csv','r') as f:
            accseetoken_value = f.read()
            print('读取accseetoken_value成功：{}'.format(accseetoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    accseetoken_value = str(accseetoken_value)
    return accseetoken_value


def teardown_hook_get_b_accesstoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        access_token = jsondata['data']['access']['token']
        print(access_token)
    try:
        # 保存token到文件
        with open('config/b_access_token.csv','w') as f:
            f.write(access_token)
            print('写入成功，access_token：{}'.format(access_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return access_token

def get_b_accesstoken():
    try:
        with open('config/b_access_token.csv','r') as f:
            accseetoken_value = f.read()
            print('读取accseetoken_value成功：{}'.format(accseetoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    accseetoken_value = str(accseetoken_value)
    authorization = 'Bearer ' + accseetoken_value
    return authorization


def teardown_hook_get_anonymous_accesstoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        access_token = jsondata['data']['access']['token']
        print(access_token)
    try:
        # 保存token到文件
        with open('config/anonymous_access_token.csv','w') as f:
            f.write(access_token)
            print('写入成功，access_token：{}'.format(access_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return access_token


def get_anonymous_accesstoken():
    try:
        with open('config/anonymous_access_token.csv','r') as f:
            accseetoken_value = f.read()
            print('读取accseetoken_value成功：{}'.format(accseetoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    accseetoken_value = str(accseetoken_value)
    authorization = 'Bearer ' + accseetoken_value
    return authorization


def teardown_hook_get_admin_accesstoken(response):
    if response.status_code == 200:
        jsondata = json.loads(response.text)
        access_token = jsondata['data']['access_token']
        print(access_token)
    try:
        # 保存token到文件
        with open('config/admin_access_token.csv','w') as f:
            f.write(access_token)
            print('写入成功，access_token：{}'.format(access_token))
            f.close()
    except Exception as e:
        print('写入失败', e)
    return access_token


def get_admin_accesstoken():
    try:
        with open('config/admin_access_token.csv','r') as f:
            accseetoken_value = f.read()
            print('读取accseetoken_value成功：{}'.format(accseetoken_value))
            f.close()
    except Exception as e:
        print('读取失败', e)
    accseetoken_value = str(accseetoken_value)
    authorization = 'Bearer ' + accseetoken_value
    return authorization