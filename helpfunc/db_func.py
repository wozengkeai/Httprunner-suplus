# @Time : 2020/3/18 15:22
# @Author : zengxiaoyan
# @File : db_func.py

import pymysql
db_config ={"host": "",
            "port": 32306,
            "user": "",
            "password": "",
            "db": "",
            "charset": 'utf8'}

db_config1 ={"host": "",
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


def get_districtsid_from_database(company_id,phone):
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    company_id = str(company_id)
    phone = str(phone)
    sql = "select id from  cfg_district where company_id= " + company_id + " and  charge_uids = (select uid from  user_info  where phone =" + phone +")"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]
    except Exception as err:
        # 发生错误时回滚
        print(err)
        db.rollback()
    db.close()


def get_uid_from_database(phone):
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    phone = str(phone)
    sql = "select uid from user_info where  enabled = 1 and phone =" + phone
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        return result[0]
    except Exception as err:
        # 发生错误时回滚
        print(err)
        db.rollback()
    db.close()


def get_salaryrecordId_from_database(uid):
    db = pymysql.connect(**db_config1)
    cursor = db.cursor()
    uid = str(uid)
    sql = "select id from salary_record where uid =" + uid
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        return result[0]
    except Exception as err:
        # 发生错误时回滚
        print(err)
        db.rollback()
    db.close()


def setup_hook_clean_db(companyid):
    """
    初始化时清理数据库中对应公司目标管理的历史数据
    :return:
    """
    db = pymysql.connect(**db_config)
    cursor = db.cursor()
    companyid = str(companyid)
    try:
        cursor.execute('delete from hotline where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from sale_cycle where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from product_price where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from sale_source_data where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from sale_goal_setting where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from profit_rate_setting where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from user_cost where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from correspond_sale_setting where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from correspond_profit_setting where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from cost_rate_setting where companyId=' + companyid)
        db.commit()
        cursor.execute('delete from monthly_plan where companyId=' + companyid)
        db.commit()
        print("delete OK")
    except Exception as err:
        #发生错误时回滚
        print("this is:", err)
        db.rollback()
    db.close()


def setup_hook_clean_db1(companyid):
    """
    初始化时清理数据库中对应公司薪资管理的历史数据
    :return:
    """
    db = pymysql.connect(**db_config1)
    cursor = db.cursor()
    companyid = str(companyid)
    try:
        # cursor.execute('delete from salary_group_user where company_id=' + companyid)
        # db.commit()
        # cursor.execute('delete from cfg_salary_group where company_id=' + companyid)
        # db.commit()
        # cursor.execute('delete from salary_month where company_id=' + companyid)
        # db.commit()
        cursor.execute('delete from salary_record where company_id=' + companyid)
        db.commit()
        # cursor.execute('delete from salary_group_income_rule where company_id=' + companyid)
        # db.commit()
        # cursor.execute('delete from salary_group_rule where company_id=' + companyid)
        # db.commit()
        print("delete OK")
    except Exception as err:
        #发生错误时回滚
        print("this is:", err)
        db.rollback()
    db.close()



def setup_hook_clean_db2(companyid):
    """
    初始化时清理数据库中对应公司薪资管理的历史数据
    :return:
    """
    db = pymysql.connect(**db_config2)
    cursor = db.cursor()
    companyid = str(companyid)
    try:
        cursor.execute('delete from role_menu where role_id = 942 and company_id=' + companyid)
        db.commit()
        cursor.execute('delete from role_permission where role_id = 942 and company_id=' + companyid)
        db.commit()
        print("delete OK")
    except Exception as err:
        # 发生错误时回滚
        print("this is:", err)
        db.rollback()
    db.close()



    # setup_hook_clean_db2(359)
    # get_salaryrecordId_from_database(3248637164036608)
    # get_uid_from_database(13700000205)
    # select_source_data()