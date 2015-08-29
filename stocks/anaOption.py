#coding:utf-8
import requests,time
import BeautifulSoup
import mySQLClass,sys
import datetime
from utc2local import local2utc

dic = {}

cur = mySQLClass.MySQLClass('localhost',3306,'root','814155356Mysql')
cur.connectDB()
cur.selectDB('optionAna')

date = datetime.datetime.today()
date = str(local2utc(date,-9.5)).split(' ')[0] + ' 00:00:00'

expired = str(datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=5))

sql = 'select stockName,sum(if(optionType="CALL",vol,0)),sum(if(optionType="PUT",vol,0)),sum(if(optionType="CALL",vol,0))/sum(if(optionType="PUT",vol,0))-1 from option_most_active where date>="' + date + '" and expired>="' + expired + '" group by stockName;'
result = cur.selectData(sql)
for line in result:
    stockName,callVol,putVol,div = line
    print stockName,callVol,putVol,div
