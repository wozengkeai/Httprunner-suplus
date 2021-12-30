# -*- coding: utf-8 -*-
# @Time : 2020/11/3 16:11
# @Author : zengxiaoyan
# @File : header.py
import hashlib
import uuid,time

def get_uuid():
    #获取随机uuid
    uuid1 = str(uuid.uuid1())
    return uuid1

def get_time():
    #生成时间戳
    return str(round(time.time() * 1000))

def get_sign(time,uuid,accessstoken):
    #生成sign
    sign = 'v!(MmM%s%s%s' %(time, uuid,accessstoken) +'MmM)i^'
    sign = hashlib.sha256(sign.encode("utf-8",errors='strict'))
    encrypts = sign.hexdigest()
    return encrypts

# print(get_sign("1604470566700","c687978fc1dd4ca295553f67999aef1",""))