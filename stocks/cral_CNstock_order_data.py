#coding:utf-8
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
import time,datetime
from commfunction import today,date_add

today_date = date_add(str(today()),-2)

DB_CONNECT_STRING = 'sqlite:///stock_CN_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

codeDatas = session.execute('select * from publish_date where code in ("002230");').fetchall()

for data in codeDatas:
    mp = 446.74*100000000
    b_r = 0.0002
    m_r = b_r/2
    code, time_to_market = data
    time_to_market = '20170104'
    lastdate = date_add(str(time_to_market),0,'%Y%m%d')
    while lastdate<=today_date:
        print lastdate
        try:
            open_price, close_price = session.execute('select open,close from day_k_data where code in ("002230") and date="' + lastdate + ' 00:00:00.000000";').fetchall()[0]
        except:
            lastdate = date_add(lastdate,1,'%Y-%m-%d')
            continue
        df = ts.get_tick_data(code,date=lastdate,pause=2)
        df.insert(0,'date',lastdate)
        df.insert(0,'code',code)
        df = df.set_index('date')
        fq = round(df.iloc[0]['price']/close_price,3)
        df['change'][df['change']=='--'] = 0.0
        df['change'] = df['change'].apply(float)
        df['type'][df['change'] == 0.0] = 'equal'
        df['type'][df['change'] > 0] = 'buy'
        df['type'][df['change'] < 0] = 'sell'
        df['price'] = (df['price']/fq).apply(round,args=(3,))
        df['change'] = df['change']/fq
        df['change'] = df['change'].apply(round,args=(3,))
        df_count = {}
        print b_r*mp
        df_count['big_buy'] = df['amount'][(df['type']=='buy') & (df['amount']>=b_r*mp)].sum()
        df_count['big_sell'] = df['amount'][(df['type']=='sell') & (df['amount']>=b_r*mp)].sum()
        df_count['big_buy'] = df['amount'][(df['type']=='buy') & (df['amount']>=b_r*mp)].sum()
        print df_count['big_buy']
        #df.to_sql('day_order_data',engine,if_exists='append')
        exit()
        lastdate = date_add(lastdate,1,'%Y-%m-%d')

r = session.execute('select code,count(1) from day_order_data group by code order by date desc;').fetchall()
'''for line in r:
    fw.write(str(line) + '\n')'''
print r