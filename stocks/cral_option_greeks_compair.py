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
import matplotlib.pyplot as plt

date_today = today()
record = 'greeks\t'+date_today+'\n'

stocks = open('stocks.txt','r').readlines()
stocks = [code.replace('\n','').replace('\r','') for code in stocks]

DB_CONNECT_STRING = 'sqlite:///stock_option_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def get_origin_option_datas(url,datasAll=[]):
    time.sleep(random()*20)
    content = BeautifulSoup.BeautifulSoup(requests.get(url).text)
    nextpage = content.findAll('a',{'id':'quotes_content_left_lb_NextPage'})
    datasAll.append(content.findAll('div',{'class':'OptionsChain-chart borderAll thin'})[0])
    if nextpage:
        get_origin_option_datas(nextpage[0]['href'])
    return datasAll

def to_dataframe(options_info):
    df_back = pd.DataFrame()
    for code in options_info:
        for date in options_info[code]:
            dfop = pd.DataFrame(options_info[code][date])
            dfop.insert(0,'date',date_today)
            if df_back.empty:
                df_back = dfop
            df_back = pd.concat([df_back,dfop], axis=0)
    for c in df_back.columns:
        try:   
            df_back[c] = df_back[c].astype('float64')
        except Exception,e:
            print e
    return df_back.drop_duplicates()

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

for stock in stocks:
    stock='YY'
    options_info = get_option_pg_datas([stock],pre='http://www.nasdaq.com/symbol/',tail='/option-chain/greeks?dateindex=-1')
    option_price_history = pd.read_sql('select * from option_greeks where `16Root`="'+stock+'" order by date asc;',engine)
    options_info = to_dataframe(options_info)
    for d in options_info['18Puts']:
        if date_today_delta(d) <= 0:
            continue
        for s in list(options_info[options_info['18Puts']==d]['17Strike']):
            t_price = options_info[options_info['18Puts']==d]
            t_price = t_price[t_price['17Strike']==s].set_index('date')
            h_prices = option_price_history[option_price_history['18Puts']==d]
            h_prices = h_prices[h_prices['17Strike']==s].set_index('date')  
            iv = pd.concat([h_prices[['15IV','24IV']],t_price[['15IV','24IV']]],axis=0)
            print stock, d, s
            print iv
            try:
                iv.plot()
                plt.legend(('Calls_IV', 'PUTS_IV'), loc='upper left')
                plt.title(stock+'_'+str(d)+'_'+str(s))
                plt.savefig('option_iv_pic/' + stock + '_' + str(d) + '_' + str(s) + '.jpg')
                plt.close('all')
            except Exception,e:
                print e
    exit()