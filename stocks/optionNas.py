#!/usr/bin/python
#coding:utf-8
import requests,time
import BeautifulSoup
import mySQLClass,sys
import datetime
from utc2local import local2utc
from random import random

t = open('t.txt','a')
t.write(str(time.time())+'\n')
t.close()

dic = {}

cur = mySQLClass.MySQLClass('localhost',3306,'root','814155356Mysql')
cur.connectDB()
cur.selectDB('optionAna')

with open('stocks.txt','r') as stocks:
    for kw in stocks:
        kw = kw[:-1]
        if kw == '':
            break
        try:
            url = 'http://www.nasdaq.com/symbol/' + kw  + '/option-chain/most-active'
            print url
            content = requests.get(url)
            content = BeautifulSoup.BeautifulSoup(content.text)
            datas = content.findAll('div',{'class':'OptionsChain-chart borderAll thin'})
            tdDatas = datas[0].findAll('td',{'class':'most-active-col1'})
            for tdElm in tdDatas[1:]:

                ctime = int(time.time())
                date = datetime.datetime.today()
                date = str(local2utc(date,-9.5)).split(' ')[0] + ' 00:00:00'

                try:
                    tds = tdElm.parent.findAll('td')
                    name = tds[0].a['href'].split('option-chain/')[1]
                    dic[name] = {}
                    dic[name]['optionType'] = tds[1].contents[0]
                    dic[name]['stockName'] = tds[2].contents[0]
                    dic[name]['strike'] = tds[3].contents[0]
                    dic[name]['vol'] = tds[7].contents[0]
                    dic[name]['openInt'] = tds[8].contents[0]
                    dic[name]['bid'] = tds[9].contents[0]
                    dic[name]['ask'] = tds[10].contents[0]
                    expiredAt = name.split('C')[0].split('P')[0]
                    dic[name]['expired'] = '20' + expiredAt[:2] + '-' + expiredAt[2:4] + '-' + expiredAt[4:6] + ' 00:00:00'
                except Exception,e:
                    print e
                    continue

                sqlSelect = 'select vol from option_most_active where date=\'' + date +'\' and optionSymbol=\'' + name +'\';'
                isIn = cur.selectData(sqlSelect)
                #print sqlSelect,isIn,isIn[0][0]
                if len(isIn)==0:
                    sql = 'insert into option_most_active (stockName,optionSymbol,expired,strike,optionType,ask,bid,vol,openInt,date,ctime) values(\'' + dic[name]['stockName'] + '\',\'' + name + '\',\'' + dic[name]['expired'] + '\',' + dic[name]['strike'] + ',\'' + dic[name]['optionType'] + '\',' + dic[name]['ask'] + ',' + dic[name]['bid'] + ',' + dic[name]['vol'] + ',' + dic[name]['openInt'] + ',\'' + date + '\',' + str(ctime) + ');'
                elif isIn[0][0]==int(dic[name]['vol']):
                    continue
                else:
                    sql = 'UPDATE option_most_active SET vol=' + dic[name]['vol'] + ',ask=' + dic[name]['ask'] + ',bid=' + dic[name]['bid'] + ',openInt=' + dic[name]['openInt'] + ',ctime=' + str(ctime) + ' WHERE date=\'' + date +'\' and optionSymbol=\'' + name +'\';'
                #print sql
                cur.executeDB(sql) 
            time.sleep(random()*2)
        except Exception,e:
            print e
