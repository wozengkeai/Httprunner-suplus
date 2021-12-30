# -*- coding: utf-8 -*-
# @Time : 2021/3/8 10:44
# @Author : zengxiaoyan
# @File : config.py
from auto_py import gol
'''
上传时保持在仿真环境
'''
gol._init()  #先必须在主模块初始化（只在Main模块需要一次即可）

#定义跨模块全局变量
db_config_test ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config1_test ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config2_test ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config3_test ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

#正式
db_config ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config2 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}
db_config3 ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

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

# gol.set_value('companyId',382)
# gol.set_value('db_config',db_config_test)
# gol.set_value('db_config2',db_config2_test)
# gol.set_value('db_config1',db_config1_test)
# gol.set_value('db_config3',db_config3_test)
gol.set_value('chance_ratio',0.3)
gol.set_value('perf_ratio',0.1)
gol.set_value('profit_ratio',0.1)

gol.set_value('host_ucenter','http://public-interface-test.fjmaimaimai.com')
gol.set_value('host_app','http://suplus-app-gateway-test.fjmaimaimai.com')

gol.set_value('phone','13800000032')
gol.set_value('psw','')

#正式
# gol.set_value('companyId',8)
# gol.set_value('db_config',db_config)
# gol.set_value('db_config2',db_config2)
# gol.set_value('db_config3',db_config3)

# 仿真
gol.set_value('companyId',1)
gol.set_value('db_config',db_config_preonline)
gol.set_value('db_config2',db_config2_preonline)
gol.set_value('db_config3',db_config3_preonline)