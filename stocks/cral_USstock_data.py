#coding:utf-8
from sqlalchemy import create_engine
import requests
from sqlalchemy.orm import sessionmaker
import time,datetime,commfunction
from random import random
import pandas as pd
import numpy as np
#exit()
stocks = open('stocks.txt','r').readlines()
stocks = [code.replace('\n','').replace('\r','') for code in stocks]
today = commfunction.today('%Y_%m_%d').replace('_0','_')

DB_CONNECT_STRING = 'sqlite:///stock_US_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

def get_origin_ustock_datas(code,today):
    time.sleep(random()*20)
    code = code.lower()
    url = 'http://stock.finance.sina.com.cn/usstock/api/jsonp_v2.php/var%20_'+code+today+'=/US_MinKService.getDailyK?symbol='+code+'&_='+today+'&___qn=3'
    contents = requests.get(url).text[:-2].split('=(')[1]
    try:
        df = pd.DataFrame(eval(contents))
        df.rename(columns={'o': 'open', 'c': 'close', 'h': 'high', 'l': 'low', 'v': 'volume', 'd': 'date'}, inplace=True)
        df['close'] = df['close'].astype(np.float64)
        df['open'] = df['open'].astype(np.float64)
        df['low'] = df['low'].astype(np.float64)
        df['high'] = df['high'].astype(np.float64)
        df['volume'] = df['volume'].astype(np.int)
        df.insert(0,'code',code.upper())
    except:
        return pd.DataFrame()
    return df.set_index('date')

for code in stocks:
    print code
    df = get_origin_ustock_datas(code,today)
    if not df.empty:
        df.to_sql('day_k_data',engine,if_exists='append')

r = session.execute('select count(1) from day_k_data;').fetchall()
print r