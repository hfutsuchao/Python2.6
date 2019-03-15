#coding:utf-8
from sqlalchemy import create_engine
import requests
from sqlalchemy.orm import sessionmaker
from commfunction import date_add
import pandas as pd
import numpy as np
from datetime import datetime,date

stocks = open('stocks.txt','r').readlines()
stocks = [code.replace('\n','').replace('\r','') for code in stocks]

DB_CONNECT_STRING = 'sqlite:///stock_US_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

for code in stocks:
    print code
    df = pd.read_sql('select * from day_k_data where code="'+code+'";',engine)
    start = df['date'][0]
    lastday = df['date'].values[-1]
    df_w = pd.DataFrame(columns=df.columns).T
    inFormat='%Y-%m-%d'
    wd = datetime.strptime(start, inFormat).weekday()
    end = date_add(start,4-wd)
    while end <= lastday:
        print start,end
        high = pd.DataFrame(df[(df['date']>=start) & (df['date']<=end)][['date','high']].max()).T.set_index('date')
        low = pd.DataFrame(df[(df['date']>=start) & (df['date']<=end)][['date','low']].min()).T.set_index('date')
        open_ = df[['date','open']][(df['date']==start)].set_index('date')
        close = df[['date','close']][(df['date']==end)].set_index('date')
        volume = pd.DataFrame(df[(df['date']==end)][['date','volume']].sum()).T.set_index('date')
        print high
        print low
        print open_
        print close
        print volume
        print pd.concat([high,low,open_,close],ignore_index=True,axis=1)
        #pd.concat((df_w,,axis=0)
        #print pd.concat([high,low,open_,close])
        start = date_add(end,2)
        end = date_add(start,4)
        print df_w
        break
    break

session.close()

#r = session.execute('select count(1) from day_k_data;').fetchall()
#print r