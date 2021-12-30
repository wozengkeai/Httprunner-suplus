# -*- coding: utf-8 -*-
# @Time : 2021/3/8 10:44
# @Author : zengxiaoyan
# @File : config.py
from auto_py import gol

gol._init()  #先必须在主模块初始化（只在Main模块需要一次即可）

#定义跨模块全局变量

#仿真
db_config_preonline ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config2_preonline ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config3_preonline ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}


gol.set_value('chance_ratio',0.3)
gol.set_value('perf_ratio',0.1)
gol.set_value('profit_ratio',0.1)

gol.set_value('host_ucenter','http://public-interface-test.fjmaimaimai.com')
gol.set_value('host_app','http://suplus-app-gateway-test.fjmaimaimai.com')

gol.set_value('phone','13800000032')
gol.set_value('psw','')



# 仿真
gol.set_value('companyId',1)
gol.set_value('db_config',db_config_preonline)
gol.set_value('db_config_preonline',db_config2_preonline)
gol.set_value('db_config3',db_config3_preonline)