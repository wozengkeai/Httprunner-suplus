# -*- coding: utf-8 -*-
# @Time : 2021/4/19 17:36
# @Author : zengxiaoyan
# @File : customer_list.py
'''
各区域分配的客户列表
一级大区：一级区域为该区域的（包含零星客户，匹配一级区域id）+分配给一级业务员的(只匹配uid）
二级区域：业务员下发分配的客户(只匹配uid）
'''
import pymysql

from auto_py import gol,config
db_config3 = gol.get_value('db_config3')
def customerList(districtId,districtPid,uid):
    '''
    根据业务区域查询该区域分配的客户，pid为0时查询二级
    :param districtId:
    :param districtPid:
    :return:
    '''

    db = pymysql.connect(**db_config3)
    cursor = db.cursor()
    sqlC = "SELECT DISTINCT customerId FROM customerAssignment WHERE  salesmanId = %s AND deletedAt is NULL" % (uid)
    sqlP = "SELECT DISTINCT customerId FROM customerAssignment WHERE companyId = 1 AND salesmanId = %s  " \
           "AND deletedAt is NULL" % (uid)
    sqlP_contain = "SELECT customerId FROM customer WHERE serviceAreaPid = %s AND isLock = 0 AND status = 1" % (districtPid)
    customerList = []
    if districtId == 0:
        # sql = sqlP
        customerP = []
        cursor.execute(sqlP)
        customerDataP = cursor.fetchall()
        for i in customerDataP:
            customerP.append(i)

        customerP_contain = []
        cursor.execute(sqlP_contain)
        customerDataP_contain = cursor.fetchall()
        for i in customerDataP_contain:
            customerP_contain.append(i)

        customer = customerP + customerP_contain
        customerList = list(set(customer))
        # print(customerList)
    else:
        sql = sqlC
        cursor.execute(sql)
        customerData = cursor.fetchall()
        c = 0
        for i in customerData:
            customerList.append(i)
            c = c + 1
        print(c)
    # else:
    #     customerP = []
    #     cursor.execute(sqlP)
    #     customerDataP = cursor.fetchall()
    #     for i in customerDataP:
    #         customerP.append(i)
    #
    #     customerP_contain = []
    #     cursor.execute(sqlP_contain)
    #     customerDataP_contain = cursor.fetchall()
    #     for i in customerDataP_contain:
    #         customerP_contain.append(i)
    #
    #     customer = customerP + customerP_contain
    #     customerList = list(set(customer))
    print(len(customerList))
    print(customerList)
    return customerList

if __name__ == "__main__":
    customerList(226,225,'3247228580575744')