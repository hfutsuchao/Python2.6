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
record = 'greeks\t'+date_today+'\n'

try:
    t = open('./tt.txt','r').readlines()
    if record in t:
        exit()
except Exception,e:
    pass
t = open('t.txt','a')
t.write(record)
t.close()

stocks = open('stocks.txt','r').readlines()
stocks = [code.replace('\n','').replace('\r','') for code in stocks]

DB_CONNECT_STRING = 'sqlite:///stock_option_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def get_origin_option_datas(url,datasAll=None):
    time.sleep(random()*10)
    if datasAll is None:
        datasAll = []
    content = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    nextpage = content.findAll('a',{'id':'quotes_content_left_lb_NextPage'})
    datasAll.append(content.findAll('div',{'class':'OptionsChain-chart borderAll thin'})[0])
    if nextpage:
        get_origin_option_datas(nextpage[0]['href'],datasAll)
    return datasAll

def write_to_database(options_info):
    df_back = pd.DataFrame()
    for date in options_info:
        if date_today_delta(date) <= 0:
            continue
        dfop = pd.DataFrame(options_info[date])
        dfop.insert(0,'date',date_today)
        if df_back.empty:
            df_back = dfop
        df_back = pd.concat([df_back,dfop], axis=0)
    df_back = df_back.set_index('17Strike')
    df_back.to_sql('option_greeks',engine,if_exists='append')

def get_option_pg_datas(code='MOMO',pre='http://www.nasdaq.com/symbol/',tail='/option-chain?money=all&dateindex=-1'):
    url = pre + code  + tail
    print url
    datasAll = get_origin_option_datas(url)
    options_info = {}
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
                if date not in options_info:
                    options_info[date] = {}
            except Exception,e:
                print e
                print 'line 55'
            for i in range(1,len(tds)):
                try:
                    column_name = str(i+9)+head_name[i]
                    if column_name not in options_info[date]:
                        options_info[date][column_name] = []
                    if tds[i].a:
                        options_info[date][column_name].append(tds[i].a.contents[0])
                    elif tds[i].span:
                        options_info[date][column_name].append(tds[i].span.contents[0])
                    else:
                        options_info[date][column_name].append(tds[i].contents[0])
                except:
                    options_info[date][column_name].append('')
    return options_info

sn = 0
if len(sys.argv) == 2:
    sn = int(sys.argv[1])
for code in stocks[sn:]:
    try:
        options_info_r = get_option_pg_datas(code,pre='http://www.nasdaq.com/symbol/',tail='/option-chain/greeks?dateindex=-1')
        write_to_database(options_info_r)
    except Exception,e:
        print e
        continue

r = session.execute('select * from option_greeks;').fetchall()
print len(r)
