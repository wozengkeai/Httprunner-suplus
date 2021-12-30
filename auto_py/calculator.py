# -*- coding: utf-8 -*-
# @Time : 2021/4/19 17:14
# @Author : zengxiaoyan
# @File : calculator.py
'''
业绩计算小工具

'''
from auto_py import gol,config
db_config3 = gol.get_value('db_config3')
perf_ratio = gol.get_value('perf_ratio')
profit_ratio = gol.get_value('profit_ratio')
chance_ratio = gol.get_value('chance_ratio')
from auto_py.sum_incrment import get_Increment,get_Pid_total
from auto_py.sum_profit import profit,pid_profit
from auto_py.customer_list import customerList
from auto_py.customer_product import costprice,customerPerf,customerProduct
from auto_py.customer_sumCost import customerCost,customerGift

def monthGoal(districtId,districtPid,uid,beginTime,endTime,nowdata):
    '''
    1.取所有客户列表
    2.遍历客户查所有的同期品项业绩之和
    3.增量提成，增利提成
    4.同期
    利润合计=(∑客户的品项数量×（价格-成本）-∑客户的变动费用-∑用户的固定费用)÷10000
    业绩合计=(∑客户的品项数量×价格）÷10000
    :return:
    '''
    #取所有分配的客户列表
    customerL = customerList(districtId,districtPid,uid)

    productPerfAll = 0  #同期业绩之和
    productProfitAll = 0  # 同期利润合计
    fixCost = customerCost(0, beginTime, endTime, 1, uid)  #固定费用
    for customer in customerL:
        customerId = customer[0]
        #单个客户的品项业绩之和
        productPerfOne = customerPerf(customerId,beginTime,endTime,districtId,districtPid,nowdata,uid)
        productPerfAll = productPerfAll + float(productPerfOne[0])


        # 某客户的同期产品列表
        productList = customerProduct(customerId,beginTime,endTime,districtId,districtPid,uid)

        changeCost = customerCost(customerId, beginTime, endTime,2,uid)  #变动费用
        giftcost = customerGift(districtId,districtPid,beginTime,endTime,customerId,uid,nowdata)  #搭赠费用
        for i in productList:
            productId = i[0]
            saleNum = float(i[2])
            salePrice = float(i[3])
            cost_price = costprice(districtPid, productId,nowdata)  #当前成本

            if cost_price != '-':
                productProfitOne = saleNum * (salePrice-float(cost_price))
            else:
                productProfitOne = 0  #无成本不统计利润
            productProfitAll = productProfitAll + productProfitOne
        productProfitAll =  productProfitAll - float(changeCost)  - float(giftcost)
    productProfit = productProfitAll - float(fixCost)


    print("客户端业绩合计")
    print(productPerfAll)
    print("客户端利润合计")
    print(productProfit)







def accruedPerf(districtPid,obj,nowDate):
    '''
    obj=[数量，价格，产品id]
    模拟客户的业绩额之和
    :return:
    '''
    #模拟业绩之和
    imitatePerf = 0
    cost = 0
    for i in obj:
        imitatePerf = imitatePerf + i[0]*i[1]

        productId = i[2]
        cost_price = costprice(districtPid, productId,nowDate)
        cost = cost + i[0]*float(cost_price)

    # 模拟业绩之和
    print(imitatePerf)

    #模拟利润之和
    imitateProfit = imitatePerf - cost
    print(imitateProfit)




if __name__ == "__main__":
    #districtId,districtPid,uid,beginTime,endTime,nowdata
    monthGoal(26,0,'3246374275117568','2020-05-01','2020-05-31','2021-05-13')