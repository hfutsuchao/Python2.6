#coding:utf-8
from GJDB import GJDB
import time, os
from googleSMS import sendSMS

os.system("color f0")

db = GJDB()
db.ms()
db.selectData('set names utf8')


for i in range(1,1000):
    sql = "SELECT FROM_UNIXTIME(show_time),title,huxing_shi,price,person,phone FROM beijing.house_source_rent WHERE show_time >=UNIX_TIMESTAMP('2014-09-18') AND show_time <UNIX_TIMESTAMP('2014-09-19') AND agent=0 AND xiaoqu REGEXP '新龙城';"
    datas = db.selectData(sql)
    print datas
    if datas:
        sendSMS(str(datas))
    print 'waiting...'
    time.sleep(60)
    os.system("cls")
