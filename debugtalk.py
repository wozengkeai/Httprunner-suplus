import datetime
import random
import string
from urllib import parse
import urllib3
from helpfunc.header_func import *
from helpfunc.login_func import *
from helpfunc.db_func import *
# from helpfunc.fileimport import *
from helpfunc.select_func import *
from auto_py.calculatorPreonlineData import *
from auto_py.productPreonlineData import *

import time

def get_dis():
    data = [{"districtIds": [0]},{"districtIds": [177]}]
    return data

def get_muid(data,cid):
    # print(data)
    for i in data:
        if i['cid'] == cid:
            muid = i['muid']
    return muid

#获取secret用于子系统单点登录
def get_secret(url):
    urllist = url.split('code=',1)
    code = urllist[1]
    de_code = parse.unquote(code)
    return de_code

#判断公司是否是8公司
def skip_company(id):
    if id == 8:
        return True
    else:
        return False

def sleep(n_secs):
    time.sleep(n_secs)

def get_randomstring(n):
    """
    随机生成n位数字符串
    :param n:
    :return:
    """
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return ran_str

def get_file(filePath="testcases_excel/salary.xlsx"):
    return open(filePath, "rb")

def get_year():
    y = datetime.datetime.now().year
    return y

def get_month():
    m = datetime.datetime.now().month
    # m = time.strftime('%m', time.localtime(time.time()))
    return m

def get_time(type):
    ymd = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    ym = time.strftime('%Y-%m', time.localtime(time.time()))
    ym1 = time.strftime('%Y%m', time.localtime(time.time()))
    ym2 = time.strftime('%Y/%m', time.localtime(time.time()))
    y = datetime.datetime.now().year
    m1 = datetime.datetime.now().month
    m2 = time.strftime('%m', time.localtime(time.time()))
    if type == 'ymd':
        return ymd
    elif type == 'ym':
        return ym
    elif type == 'ym1':
        return ym1
    elif type == 'ym2':
        return ym2
    elif type == 'y':
        return y
    elif type == 'm1':
        return m1
    elif type == 'm2':
        return m2


def str_to_float(string):
    i = float(string)
    return i

def int_to_str(int):
    i = string(int)
    return i

def get_isNull(data,s,t):
    a = data[s]
    if t in a:
        x = len(data[s][t])
        return x
    else:
        return 0






def get_childAchievements(data,uid,incremental):
    #二级业务员--已知二级业务员UID--业绩、利润、毛利额一级
    x = len(data['list'])
    for i in range(x):
        # print(i)
        if uid == int(data['list'][i]['children'][0]['salesman']['id']):
            sy = i
            # print(sy)
            break
    Achievements = float(data['list'][sy]['children'][0][incremental])
    print(Achievements)
    return Achievements


def get_Achievements(data,uid,incremental):
    #大区经理--已知二级业务员UID--业绩、利润、毛利额一级
    x = len(data['list'])
    for i in range(x):
        # print(i)
        if uid == int(data['list'][i]['children'][0]['salesman']['id']):
            sy = i
            # print(sy)
            break
    Achievements = float(data['list'][sy][incremental])
    print(Achievements)
    return Achievements

def get_m_achievements(data,uid,achievements):
    #已知经理UID---业绩、利润、毛利额一级
    x = len(data['list'])
    for i in range(x):
        if uid == int(data['list'][i]['salesman']['id']):
            sy = i
            break
    achievements = float(data['list'][sy][achievements])
    return achievements


def get_grossprofit(data,uid,grossprofit,type):
    #已知二级业务员UID，获取毛利额二级数据
    x = len(data['list'])
    for i in range(x):
        # print(i)
        if uid == int(data['list'][i]['children'][0]['salesman']['id']):
            sy = i
            # print(sy)
            break
    grossprofit = float(data['list'][sy]['children'][0][grossprofit][type])
    return grossprofit

def get_m_grossprofit(data,uid,grossprofit,type):
    #已知区域经理UID，获取毛利额二级数据
    x = len(data['list'])
    for i in range(x):
        # print(i)
        if uid == int(data['list'][i]['salesman']['id']):
            sy = i
            # print(sy)
            break
    grossprofit = float(data['list'][sy][grossprofit][type])
    return grossprofit


def get_data(data,income,perf,com):
    a = data[income][perf][com]
    return a



# print(get_time('m1'))



