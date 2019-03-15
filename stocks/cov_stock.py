#coding:utf-8
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
import talib
from commfunction import *

DB_CONNECT_STRING = 'sqlite:///stock_US_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

codes = session.execute('select distinct(code) from day_k_data;').fetchall()

def corr_calc(code):
    df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
    ma5 = talib.MA(df['close'].values,5)
    ma10 = talib.MA(df['close'].values,10)
    ma20 = talib.MA(df['close'].values,20)
    ma30 = talib.MA(df['close'].values,30)
    K, D = talib.STOCH(df['high'].values,df['low'].values,df['close'].values, fastk_period=9, slowk_period=3)
    J = K * 3 - D * 2
    atr = talib.ATR(df['high'].values,df['low'].values,df['close'].values)
    natr = talib.NATR(df['high'].values,df['low'].values,df['close'].values)
    trange = talib.TRANGE(df['high'].values,df['low'].values,df['close'].values)
    cci = talib.CCI(df['high'].values,df['low'].values,df['close'].values,14)
    dif, dea, bar = talib.MACDFIX(df['close'].values)
    bar = bar * 2
    df = df.drop(['code','open','low', 'high'],axis=1).set_index('date')
    #df = df.drop(['code'],axis=1).set_index('date')
    df.insert(0,'ma5',ma5)
    df.insert(0,'ma10',ma10)
    df.insert(0,'ma20',ma20)
    df.insert(0,'ma30',ma30)
    df.insert(0,'K',K)
    df.insert(0,'D',D)
    df.insert(0,'J',J)
    df.insert(0,'cci',cci)
    df.insert(0,'bar',bar)
    df.insert(0,'dif',dif)
    df.insert(0,'dea',dea)
    print df.corr()
    
def corr_rate_calc(code):
    df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
    ma5 = talib.MA(df['close'].values,5)
    ma10 = talib.MA(df['close'].values,10)
    ma20 = talib.MA(df['close'].values,20)
    ma30 = talib.MA(df['close'].values,30)
    K, D = talib.STOCH(df['high'].values,df['low'].values,df['close'].values, fastk_period=9, slowk_period=3)
    J = K * 3 - D * 2
    atr = talib.ATR(df['high'].values,df['low'].values,df['close'].values)
    natr = talib.NATR(df['high'].values,df['low'].values,df['close'].values)
    trange = talib.TRANGE(df['high'].values,df['low'].values,df['close'].values)
    cci = talib.CCI(df['high'].values,df['low'].values,df['close'].values,14)
    dif, dea, bar = talib.MACDFIX(df['close'].values)
    bar = bar * 2
    df = df.drop(['code','open','low', 'high'],axis=1).set_index('date')
    df.insert(0,'ma5',ma5)
    df.insert(0,'ma10',ma10)
    df.insert(0,'ma20',ma20)
    df.insert(0,'ma30',ma30)
    df.insert(0,'K',K)
    df.insert(0,'D',D)
    df.insert(0,'J',J)
    df.insert(0,'cci',cci)
    df.insert(0,'bar',bar)
    df.insert(0,'dif',dif)
    df.insert(0,'dea',dea)
    df_yesterday = df.T
    index_c = df.index
    added = [0] * len(df.columns)
    df_yesterday.insert(0, len(df_yesterday.columns), added)
    df_yesterday = df_yesterday.T
    df_yesterday = df_yesterday.drop(df.index[len(df.index)-1])
    df_yesterday.insert(0, 'index_c', index_c)
    df_yesterday = df_yesterday.set_index('index_c')
    dfd = df - df_yesterday
    return dfd.corr()
    
corr_tech = []
for code in codes[:1]:
    code = code[0]
    print code
    corr_tech.append(corr_rate_calc(code))
corr = (sum(corr_tech)/len(corr_tech)).ix['close']
print corr