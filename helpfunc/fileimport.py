# @Time : 2020/4/8 11:20
# @Author : zengxiaoyan
# @File : fileimport.py
# coding:utf-8
import requests

s = requests.session()  # 保持会话




# 上传文件地址
url1 = "http://suplus-salary-test.fjmaimaimai.com/salary-record-import"

f ={
    "localUrl": (None,"salary.xlsx"),
    "file": ("salary.xlsx", open("D:\suplus_api\\testcases_excel\salary.xlsx", "rb"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
  }
r = s.post(url1, files=f)
try:
    fileurl = r.json()["url"]
    print(u"上传文件后的url地址：%s"%fileurl)
except Exception as msg:
    print(u"返回值不是json格式：%s"%str(msg))
    print(r.content)