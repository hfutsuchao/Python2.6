#!/usr/bin/python
#coding:utf-8
import requests,time
import BeautifulSoup
import sys
import datetime
from random import random
import pandas as pd
from commfunction import today,date_add,date_today_delta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

date_today = date_add(today(),-1)
record = 'option_price\t'+date_today+'\n'

try:
    t = open('t.txt','r').readlines()
    if record in t:
        exit()
except Exception,e:
    pass
t = open('t.txt','a')
t.write(record)
t.close()

DB_CONNECT_STRING = 'sqlite:///stock_option_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

stocks = open('stocks.txt','r').readlines()
stocks = [code.replace('\n','').replace('\r','') for code in stocks]

def get_origin_option_datas(url,datasAll=None):
    time.sleep(random()*20)
    if datasAll is None:
        datasAll = []
    content = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    nextpage = content.findAll('a',{'id':'quotes_content_left_lb_NextPage'})
    datasAll.append(content.findAll('div',{'class':'OptionsChain-chart borderAll thin'})[0])
    if nextpage:
        get_origin_option_datas(nextpage[0]['href'])
    return datasAll

def write_to_database(options_info):
    for code in options_info:
        for date in options_info[code]:
            if date_today_delta(date) <= 0:
                continue
            dfop = pd.DataFrame(options_info[code][date]).set_index('17Strike')
            dfop.insert(0,'date',date_today)
            dfop = dfop.drop_duplicates()
            dfop.to_sql('option_price',engine,if_exists='append')

def get_option_pg_datas(stocks=['MOMO'],pre='http://www.nasdaq.com/symbol/',tail='/option-chain?money=all&dateindex=-1'):
    options_info = {}
    for code in stocks:
        options_info[code] = {}
        url = pre + code  + tail
        print url
        datasAll = get_origin_option_datas(url)
        for datas in datasAll:
            head_name = []
            if datas.table.thead:
                head = datas.table.thead.tr.findAll('th')
            else:
                head = datas.table.tr.findAll('th')
            rows = datas.table.findAll('tr')
            for th in head:
                try:
                    head_name.append(th.a.contents[0].replace('\r','').replace('\n','').replace(' ',''))
                except:
                    head_name.append(th.contents[0])
            for row in rows[1:]:
                try:
                    tds = row.findAll('td')
                    if len(tds) == 1:
                        continue
                    date = tds[0].a.contents[0]
                    if date not in options_info[code]:
                        options_info[code][date] = {}
                except Exception,e:
                    print e
                    print 'line 55'
                for i in range(1,len(tds)):
                    try:
                        column_name = str(i+9)+head_name[i]
                        if column_name not in options_info[code][date]:
                            options_info[code][date][column_name] = []
                        if tds[i].a:
                            options_info[code][date][column_name].append(tds[i].a.contents[0])
                        elif tds[i].span:
                            options_info[code][date][column_name].append(tds[i].span.contents[0])
                        else:
                            options_info[code][date][column_name].append(tds[i].contents[0])
                    except:
                        options_info[code][date][column_name].append('')
    return options_info

date_today = date_add(today(),-1)
print date_today
for stock in stocks:
    try:
        options_info = get_option_pg_datas([stock])
    except Exception,e:
        print e
        continue
    write_to_database(options_info)

r = session.execute('select * from option_price;').fetchall()
print len(r)