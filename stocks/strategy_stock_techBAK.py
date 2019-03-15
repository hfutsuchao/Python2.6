#coding:utf-8
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
#import time,datetime,comfunction
import talib

DB_CONNECT_STRING = 'sqlite:///stock_US_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

codes = session.execute('select distinct(code) from day_k_data;').fetchall()

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
    #df = ts.get_k_data(code)
    df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
    buy_val   = {}
    buy_date  = {}
    sell_val  = {}
    sell_date = {}
    is_buy = {}
    ma5 = talib.MA(df['close'].values,5)
    ma10 = talib.MA(df['close'].values,10)
    ma20 = talib.MA(df['close'].values,20)
    ma30 = talib.MA(df['close'].values,30)
    K, D = talib.STOCH(df['high'].values,df['low'].values,df['close'].values, fastk_period=9, slowk_period=3)
    atr = talib.ATR(df['high'].values,df['low'].values,df['close'].values)
    natr = talib.NATR(df['high'].values,df['low'].values,df['close'].values)
    trange = talib.TRANGE(df['high'].values,df['low'].values,df['close'].values)
    print atr
    print natr
    print trange
    exit()
    cci = talib.CCI(df['high'].values,df['low'].values,df['close'].values,14)
    #macd, macdsignal, macdhist = talib.MACDFIX(df['close'].values)
    close = df['close']
    dif = dif_calc(df)
    dea = dea_calc(df)
    bar = bar_calc(df)
    for idx in range(len(ma10)):
        ma10_buy = 0
        ma10_sell = 0
        bar_buy = 0
        bar_sell = 0
        cci_buy = 0
        cci_sell = 0
        dif_buy = 0
        dif_sell = 0
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

        if idx>=1:
            bar_val_y = bar.iloc[idx-1][0]
            dif_val_y = dif.iloc[idx-1][0]
            dea_val_y = dea.iloc[idx-1][0]
            cci_val_y = cci[idx-1]
        
        #print close_val, ma10_val, cci_val, cci_val_y, dif_val, dif_val_y, dea_val, dea_val_y, bar_val, bar_val_y

        if close_val > ma10_val: #估价>=ma10
            ma10_buy = 1

        if bar_val>0:
            #bar由-转+
            bar_buy = 1

        if cci_val>=100:  #CCI突破100
            cci_buy = 1

        if dif_val>dif_val_y: #dif上穿dea
            dif_buy = 1

        if close_val<ma10_val: #估价<=ma10
            ma10_sell = 1

        if bar_val<0:
            #bar由+转-
            bar_sell = 1

        if cci_val<=100:  #CCI跌出100
            cci_sell = 1

        if dif_val<dif_val_y: #dif下穿dea
            dif_sell = 1

        #print ma10_buy*bar_buy*cci_buy*dif_buy

        for ih in (0,1):
            for ij in (0,1):
                for ik in (0,1):
                    for il in (0,1):
                        ma10_buy_t = ma10_buy
                        bar_buy_t = bar_buy
                        cci_buy_t = cci_buy
                        dif_buy_t = dif_buy

                        if ih == 1:
                            ma10_buy_t = ih
                        if ij == 1:
                            bar_buy_t = ij
                        if ik == 1:
                            cci_buy_t = ik
                        if il == 1:
                            dif_buy_t = il

                        for ihs in (0,1):
                            for ijs in (0,1):
                                for iks in (0,1):
                                    for ils in (0,1):                        
                                        bar_sell_t = bar_sell
                                        cci_sell_t = cci_sell
                                        dif_sell_t = dif_sell
                                        ma10_sell_t = ma10_sell
                                        if ihs == 1:
                                            ma10_sell_t = ihs
                                        if ijs == 1:
                                            bar_sell_t = ijs
                                        if iks == 1:
                                            cci_sell_t = iks
                                        if ils == 1:
                                            dif_sell_t = ils

                                        s_type = str(ih)+str(ij)+str(ik)+str(il)+'b|s'+str(ihs)+str(ijs)+str(iks)+str(ils)

                                        if s_type not in buy_val:
                                            buy_val[s_type] = []
                                            buy_date[s_type] = []
                                            sell_val[s_type] = []
                                            sell_date[s_type] = []
                                            is_buy[s_type] = 0

                                        if ma10_buy_t*bar_buy_t*cci_buy_t*dif_buy_t == 1:
                                            if is_buy[s_type] == 0:
                                                is_buy[s_type] = 1
                                                buy_val[s_type].append(close_val)
                                                buy_date[s_type].append(close.keys()[idx])
                                                
                                                

                                        if ma10_sell_t*bar_sell_t*cci_sell_t*dif_sell_t == 1: 
                                            if is_buy[s_type] == 1:
                                                is_buy[s_type] = 0
                                                sell_val[s_type].append(close_val)
                                                sell_date[s_type].append(close.keys()[idx])

    print "stock number: %s" %code
    #print "buy count   : %d" %len(buy_val)
    #print "sell count  : %d" %len(sell_val)

    rate = {}

    rate['based'] = close[len(close)-1] * (1 - 0.002) / close[0]
    for s_type in sell_val:
        rate[s_type] = 1.0 
        for i in range(len(sell_val[s_type])):
            rate[s_type] = rate[s_type] * (sell_val[s_type][i] * (1 - 0.002) / buy_val[s_type][i])
            #print "buy date : %s, buy price : %.2f, sell price: %.2f" %(buy_date[s_type][i], buy_val[s_type][i], sell_val[s_type][i])
    
    rate = sorted(rate.items(),key=lambda x:x[1],reverse=True)
    return rate

def parse_or(code):
    '''process stock'''
    #df = ts.get_k_data(code)
    df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
    buy_val   = {}
    buy_date  = {}
    sell_val  = {}
    sell_date = {}
    is_buy = {}
    ma5 = talib.MA(df['close'].values,5)
    ma10 = talib.MA(df['close'].values,10)
    ma20 = talib.MA(df['close'].values,20)
    ma30 = talib.MA(df['close'].values,30)
    K, D = talib.STOCH(df['high'].values,df['low'].values,df['close'].values, fastk_period=9, slowk_period=3)
    
    close = df['close']
    cci = talib.CCI(df['high'].values,df['low'].values,df['close'].values,14)
    #macd, macdsignal, macdhist = talib.MACDFIX(df['close'].values)
    dif = dif_calc(df)
    dea = dea_calc(df)
    bar = bar_calc(df)
    for idx in range(len(ma10)):
        ma10_buy = 0
        ma10_sell = 0
        bar_buy = 0
        bar_sell = 0
        cci_buy = 0
        cci_sell = 0
        dif_buy = 0
        dif_sell = 0
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

        if idx>=1:
            bar_val_y = bar.iloc[idx-1][0]
            dif_val_y = dif.iloc[idx-1][0]
            dea_val_y = dea.iloc[idx-1][0]
            cci_val_y = cci[idx-1]
        
        #print close_val, ma10_val, cci_val, cci_val_y, dif_val, dif_val_y, dea_val, dea_val_y, bar_val, bar_val_y

        if close_val > ma10_val: #估价>=ma10
            ma10_buy = 1

        if bar_val>0:
            #bar由-转+
            bar_buy = 1

        if cci_val>=100:  #CCI突破100
            cci_buy = 1

        if dif_val>dif_val_y: #dif上穿dea
            dif_buy = 1

        if close_val<ma10_val: #估价<=ma10
            ma10_sell = 1

        if bar_val<0:
            #bar由+转-
            bar_sell = 1

        if cci_val<=100:  #CCI跌出100
            cci_sell = 1

        if dif_val<dif_val_y: #dif下穿dea
            dif_sell = 1

        #print ma10_buy*bar_buy*cci_buy*dif_buy

        for ih in (0,1):
            for ij in (0,1):
                for ik in (0,1):
                    for il in (0,1):
                        ma10_buy_t = ma10_buy
                        bar_buy_t = bar_buy
                        cci_buy_t = cci_buy
                        dif_buy_t = dif_buy

                        if ih == 1:
                            ma10_buy_t = 0
                        if ij == 1:
                            bar_buy_t = 0
                        if ik == 1:
                            cci_buy_t = 0
                        if il == 1:
                            dif_buy_t = 0

                        for ihs in (0,1):
                            for ijs in (0,1):
                                for iks in (0,1):
                                    for ils in (0,1):                        
                                        bar_sell_t = bar_sell
                                        cci_sell_t = cci_sell
                                        dif_sell_t = dif_sell
                                        ma10_sell_t = ma10_sell
                                        if ihs == 1:
                                            ma10_sell_t = 0
                                        if ijs == 1:
                                            bar_sell_t = 0
                                        if iks == 1:
                                            cci_sell_t = 0
                                        if ils == 1:
                                            dif_sell_t = 0

                                        s_type = str(ih)+str(ij)+str(ik)+str(il)+'b|s'+str(ihs)+str(ijs)+str(iks)+str(ils)

                                        if s_type not in buy_val:
                                            buy_val[s_type] = []
                                            buy_date[s_type] = []
                                            sell_val[s_type] = []
                                            sell_date[s_type] = []
                                            is_buy[s_type] = 0

                                        if ma10_buy_t or bar_buy_t or cci_buy_t or dif_buy_t:
                                            if is_buy[s_type] == 0:
                                                is_buy[s_type] = 1
                                                buy_val[s_type].append(close_val)
                                                buy_date[s_type].append(close.keys()[idx])
                                                
                                                

                                        if ma10_sell_t or bar_sell_t or cci_sell_t or dif_sell_t: 
                                            if is_buy[s_type] == 1:
                                                is_buy[s_type] = 0
                                                sell_val[s_type].append(close_val)
                                                sell_date[s_type].append(close.keys()[idx])

    print "stock number: %s" %code
    #print "buy count   : %d" %len(buy_val)
    #print "sell count  : %d" %len(sell_val)

    rate = {}

    rate['based'] = close[len(close)-1] * (1 - 0.002) / close[0]
    for s_type in sell_val:
        rate[s_type] = 1.0 
        for i in range(len(sell_val[s_type])):
            rate[s_type] = rate[s_type] * (sell_val[s_type][i] * (1 - 0.002) / buy_val[s_type][i])
            #print "buy date : %s, buy price : %.2f, sell price: %.2f" %(buy_date[s_type][i], buy_val[s_type][i], sell_val[s_type][i])
    
    rate = sorted(rate.items(),key=lambda x:x[1],reverse=True)
    return rate


rate = {}
strategy = {}
for code in codes[1:2]:
    code = code[0]
    print code
    rate[code] = parse(code)
    strategy[rate[code][0][0]] = 0

for code in rate:
    strategy[rate[code][0][0]] = strategy[rate[code][0][0]] + 1
    for i in range(len(rate[code])):
        print code, rate[code][i][0], rate[code][i][1]

for key in strategy:
    print key, strategy[key]