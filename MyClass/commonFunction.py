#coding:utf-8
import os
import time
import sys

import mySQLClass, html
import re, urllib2, urllib, cookielib, json
from config import gjname,gjpwd

def CRMLogin():
    params = {"UserName":gjname,"Domain":"@ganji.com","Password":gjpwd}
    url = "http://sso.ganji.com/Account/LogOn"
    crm = html.Html()
    crm.post(url,params,"")
    return crm

def sleep(t=0):
    time.sleep(float(t))

def compSleep(t=0):
    time.sleep(float(t))
    os.system('shutdown -h')

def dateVal(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        try:
            time.strptime(str, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

def getAccountId(name,crm):
    params = {'[Equal]Email':name,'accountListType':'2','page':'1','pagesize':'20','sortname':'CreatedTime','sortorder':'desc','unnamed':'none'}
    url = "http://gcrm.ganji.com/HousingAccount/Items?listType=ForManagers"
    accountId = json.loads(crm.post(url,params,""))['Rows'][0]['Id']
    return accountId

'''for i in [i for i in range(1,109)]:
    print '售楼部一康经理'+str(i), getAccountId('售楼部一康经理'+str(i),crm)
'''

def dateToday():
    dateToday = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return dateToday

def  replaceSign(str, mode = 0):
    hard = ['\t',' ','~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', ',', '.', '/', ':', '"', ';', '\\', '\'', '[', ']', '{', '}', '|', '<', '>', '?', '，', '。', '、', '《', '》', '？', '，', '；', '‘', '：', '“', '”', '【', '】', '、', '￥', '（', '）', '·', '！', '\n']
    easy = ['\t','~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '/', '\\', '\'', '[', ']', '{', '}', '<', '>', '、', '《', '》', '，', '‘', '：', '“', '”', '【', '】', '、', '￥', '（', '）', '·', '\n']
    modeType = (easy, hard)
    for sign in modeType[mode]:
        str = str.replace(sign,'')
    return str

'''
if __name__ == '__main__':
    try:
        compSleep(sys.argv[1])
    except:
        compSleep(5)'''