#coding:utf-8
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
#import time,datetime,comfunction
import talib

#fw = open('stock_date.txt','w')
#todaydate = comfunction.date_today()
#todaydate = comfunction.date_delta(str(todaydate),-2)

#DB_CONNECT_STRING = 'sqlite:///stock_data.db'
#engine = create_engine(DB_CONNECT_STRING,echo=False)
#DB_Session = sessionmaker(bind=engine)
#session = DB_Session()

#r = session.execute('select * from day_k_data where code="000001" order by date asc;').fetchall()
#df = pd.read_sql('select * from day_k_data where code="000002" order by date asc;',engine)

df = ts.get_k_data('000002') #601212

def ma_calc(df,n=5):
    ma = {}
    for i in range(len(df)):
        if i <n:
            ma[df.iloc[i]['date']] = df[:(i+1)]['close'].mean()
        else:
            ma[df.iloc[i]['date']] = df[(i+1-n):(i+1)]['close'].mean()
    return pd.DataFrame([ma]).T

def ema_calc(df,n=12):
    ema = {}
    ema[df.iloc[0]['date']] = df.iloc[0]['close']
    for i in range(1,len(df)):
        ema[df.iloc[i]['date']] = 2.0/(n+1)*float(df.iloc[i]['close']) + (n-1.0)/(n+1)*ema[df.iloc[i-1]['date']]
    return pd.DataFrame([ema]).T

def dif_calc(df,m=12,n=26):
    ema1 = ema_calc(df,m)
    ema2 = ema_calc(df,n)
    return ema1 - ema2

def dea_calc(df,n=9):
    dea = {}
    dea[df.iloc[0]['date']] = 0
    dif = dif_calc(df)
    for i in range(1,len(df)):
        dea[df.iloc[i]['date']] = 2.0/(n+1)*(dif[0][df.iloc[i]['date']]) + (n-1.0)/(n+1)*dea[df.iloc[i-1]['date']]
    return pd.DataFrame([dea]).T

def bar_calc(df,n=9):
    return 2 * (dif_calc(df) - dea_calc(df))

def cci_calc(df,n=12):
    cci = {}
    typ = {}
    ma_typ = {}
    for i in range(len(df)):
        typ[df.iloc[i]['date']] = df[['high','close','low']][df['date']==df.iloc[i]['date']].T.mean()[i]
    typ = pd.DataFrame([typ]).T

    for i in range(len(df)):
        if i <n:
            ma_typ[df.iloc[i]['date']] = typ[:(i+1)].mean()[0]
        else:
            ma_typ[df.iloc[i]['date']] = typ[(i+1-n):(i+1)].mean()[0]
    ma_typ = pd.DataFrame([ma_typ]).T
    avedev = np.abs(typ - ma_typ)

    for i in range(len(df)):
        if i <n:
            cci[df.iloc[i]['date']] = (typ[0][i] - ma_typ[0][i])/(0.015*(avedev[0][:(i+1)].mean()))
        else:
            cci[df.iloc[i]['date']] = (typ[0][i] - ma_typ[0][i])/(0.015*(avedev[0][(i+1-n):(i+1)].mean()))
    return pd.DataFrame([cci]).T

def cci_calc_bak(df,n=12):
    cci = {}
    typ = {}
    md = {}
    ma = ma_calc(df)
    close_price = df[['date','close']].set_index('date')
    close_price.columns=[0]
    md_n = ma-close_price
    for i in range(len(df)):
        typ[df.iloc[i]['date']] = df[['high','close','low']][df['date']==df.iloc[i]['date']].T.mean()[i]
    typ = pd.DataFrame([typ]).T

    for i in range(len(df)):
        if i <n:
            md[df.iloc[i]['date']] = md_n[:(i+1)].mean()[0]
        else:
            md[df.iloc[i]['date']] = md_n[(i+1-n):(i+1)].mean()[0]
    md = pd.DataFrame([md]).T
    for i in range(len(df)):
        if i <n:
            #print np.abs(avedev)[0][:(i+1)].mean(),ma_typ[0][i]
            cci[df.iloc[i]['date']] = (typ[0][i] - ma[0][i])/(0.015*md[0][i])
        else:
            cci[df.iloc[i]['date']] = (typ[0][i] - ma[0][i])/(0.015*md[0][i])
    return pd.DataFrame([cci]).T

def kdj_calc(df,n=9):
    rsv = {}
    k = {}
    d = {}
    j = {}
    date_index = {}
    for i in range(len(df)):
        if i <n:
            h9 = df.iloc[:i+1]['high'].max()
            l9 = df.iloc[:i+1]['low'].min()
            c = df.iloc[i]['close']
            rsv[i] = (c-l9)/(h9-l9)*100
            date_index[i] = df.iloc[i]['date']
        else:
            h9 = df.iloc[i+1-n:i+1]['high'].max()
            l9 = df.iloc[i+1-n:i+1]['low'].min()
            c = df.iloc[i]['close']
            rsv[i] = (c-l9)/(h9-l9)*100
            date_index[i] = df.iloc[i]['date']
            #rsv[df.iloc[i]['date']] = (c-l9)/(h9-l9)*100
    rsv = pd.DataFrame([rsv]).T
    date_index = pd.DataFrame([date_index]).T
    rsv = pd.concat([rsv,date_index],axis=1)
    rsv.columns=['close','date']
    rsv = rsv.fillna(0.0)
    k = ema_calc(rsv,3)
    print k
    exit()

def parse(code):
    '''process stock'''
    df = ts.get_k_data(code)
    is_buy    = 0
    buy_val   = []
    buy_date  = []
    sell_val  = []
    sell_date = []
    ma10 = talib.MA(df['close'].values,10)
    close = df['close']
    rate = 1.0
    cci = talib.CCI(df['high'].values,df['low'].values,df['close'].values,14)
    #macd, macdsignal, macdhist = talib.MACDFIX(df['close'].values)
    dif = dif_calc(df)
    dea = dea_calc(df)
    bar = bar_calc(df)
    for idx in range(len(ma10)):
        close_val = close[idx]
        ma10_val = ma10[idx]
        cci_val = cci[idx]
        dif_val = dif.iloc[idx][0]
        dea_val = dea.iloc[idx][0]
        bar_val = bar.iloc[idx][0]
        bar_val_y = 0
        dif_val_y = 0
        dea_val_y = 0
        cci_val_y = 0
        ma10_buy = 0
        bar_buy = 0
        cci_buy = 0
        dif_buy = 0
        ma10_sell = 0
        bar_sell = 0
        cci_sell = 0
        dif_sell = 0
        if idx>=1:
            bar_var_y = bar.iloc[idx-1][0]
            dif_val_y = dif.iloc[idx-1][0]
            dea_val_y = dea.iloc[idx-1][0]
            cci_val_y = cci[idx-1]
        
        if (close_val > ma10_val): #估价>=ma10
            ma10_buy = 1

        if bar_val>0 and bar_val_y<=0:
            #bar由-转+
            bar_buy = 1

        if cci_val>=100 and cci_val>cci_val_y:  #CCI突破100
            cci_buy = 1

        if dif_val>dif_val_y and dif_val>dea_val and dif_val_y<=dea_val_y: #dif上穿dea
            dif_buy = 1

        if (close_val < ma10_val): #估价<=ma10
            ma10_sell = 1

        if bar_val<0 and bar_val_y>0:
            #bar由+转-
            bar_sell = 1

        if cci_val<=100 and cci_val<cci_val_y:  #CCI跌出100
            cci_sell = 1

        if dif_val<dif_val_y and dif_val<dea_val and dif_val_y>=dea_val_y: #dif下穿dea
            dif_sell = 1

        if ma10_buy*bar_buy*cci_buy*dif_buy == 1:
            if is_buy == 0:
                is_buy = 1
                buy_val.append(close_val)
                buy_date.append(close.keys()[idx])
        if ma10_sell*bar_sell*cci_sell*dif_sell == 1: 
            if is_buy == 1:
                is_buy = 0
            sell_val.append(close_val)
            sell_date.append(close.keys()[idx])

    print "stock number: %s" %code
    print "buy count   : %d" %len(buy_val)
    print "sell count  : %d" %len(sell_val)

    for i in range(len(sell_val)):
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])
        print "buy date : %s, buy price : %.2f" %(buy_date[i], buy_val[i])
        print "sell date: %s, sell price: %.2f" %(sell_date[i], sell_val[i])

    print "rate: %.2f" % rate

print parse('600959')