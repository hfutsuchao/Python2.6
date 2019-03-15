#coding:utf-8
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
import talib
import matplotlib.pyplot as plt
import itertools

strategy_count = 5
y = [0] * strategy_count + [1] * strategy_count
container = list(set(itertools.permutations(y,5)))

DB_CONNECT_STRING = 'sqlite:///stock_US_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

codes = session.execute('select distinct(code) from day_k_data;').fetchall()

def parse(code,start_date='0'):
    df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
    buy_price   = {}
    buy_date  = {}
    sell_price  = {}
    sell_date = {}
    is_buy = {}
    rate = {}
    profit = {}
    profit['based'] = {}
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
    close = df['close']
    start_date_open = 0
    for idx in range(len(ma10)):
        if df.date[idx] < start_date:
            continue
        ma10_buy = 0
        ma10_sell = 0
        bar_buy = 0
        bar_sell = 0
        cci_buy = 0
        cci_sell = 0
        dif_buy = 0
        dif_sell = 0
        K_buy = 0
        K_sell = 0
        close_val = close[idx]
        ma10_val = ma10[idx]
        ma20_val = ma20[idx]
        ma5_val = ma5[idx]
        cci_val = cci[idx]
        dif_val = dif[idx]
        dea_val = dea[idx]
        bar_val = bar[idx]
        K_val = K[idx]
        D_val = D[idx]
        J_val = J[idx]
        if start_date_open == 0:
            start_date_open = close_val
        if idx>=1:
            bar_val_y = bar[idx-1]
            dif_val_y = dif[idx-1]
            dea_val_y = dea[idx-1]
            cci_val_y = cci[idx-1]
            K_val_y = K[idx-1]
            if df.date[idx-1] not in profit['based']:
                profit['based'][df.date[idx-1]] = 1.0
            profit['based'][df.date[idx]] = profit['based'][df.date[idx-1]] * close[idx] / close[idx-1]
        else:
            bar_val_y = 0
            dif_val_y = 0
            dea_val_y = 0
            cci_val_y = 0
            K_val_y = 0

        if close_val > ma10_val:
            ma10_buy = 1

        if bar_val>0 and bar_val>bar_val_y:
            bar_buy = 1

        if cci_val>=100 and cci_val>cci_val_y:
            cci_buy = 1

        if dif_val>dea_val and dif_val>dif_val_y:
            dif_buy = 1

        if K_val>D_val and K_val>K_val_y:
            K_buy = 1

        if close_val<ma10_val:
            ma10_sell = 1

        if bar_val<0 and bar_val<bar_val_y:
            bar_sell = 1

        if cci_val<=100 and cci_val<cci_val_y:
            cci_sell = 1

        if dif_val<dea_val and dif_val<dif_val_y:
            dif_sell = 1

        if K_val<D_val and K_val<K_val_y:
            K_sell = 1
            
        for elm1 in container:

            ih, ij, ik, il, im = elm1
            ma10_buy_t = ma10_buy
            bar_buy_t = bar_buy
            cci_buy_t = cci_buy
            dif_buy_t = dif_buy
            K_buy_t = K_buy

            temp = 1

            if ih == 0:
                ma10_buy_t = temp
            if ij == 0:
                bar_buy_t = temp
            if ik == 0:
                cci_buy_t = temp
            if il == 0:
                dif_buy_t = temp
            if im == 0:
                K_buy_t = temp

            for elm2 in container:
                ihs, ijs, iks, ils, ims = elm2
                bar_sell_t = bar_sell
                cci_sell_t = cci_sell
                dif_sell_t = dif_sell
                ma10_sell_t = ma10_sell
                K_sell_t = K_sell
                temp = 0
                if ihs == 0:
                    ma10_sell_t = temp
                if ijs == 0:
                    bar_sell_t = temp
                if iks == 0:
                    cci_sell_t = temp
                if ils == 0:
                    dif_sell_t = temp
                if ims == 0:
                    K_sell_t = temp                                            

                s_type = str(ih)+str(ij)+str(ik)+str(il)+str(im)+'b|s'+str(ihs)+str(ijs)+str(iks)+str(ils)+str(ims)

                if s_type not in buy_price:
                    buy_price[s_type] = []
                    buy_date[s_type] = []
                    sell_price[s_type] = []
                    sell_date[s_type] = []
                    is_buy[s_type] = 0

                if ma10_buy_t * bar_buy_t * cci_buy_t * dif_buy_t * K_buy_t:
                    if is_buy[s_type] == 0:
                        is_buy[s_type] = 1
                        buy_price[s_type].append(close_val)
                        buy_date[s_type].append(df.date[idx])
                        continue

                if ma10_sell_t or bar_sell_t or cci_sell_t or dif_sell_t or K_sell_t: 
                    if is_buy[s_type] == 1:
                        is_buy[s_type] = 0
                        sell_price[s_type].append(close_val)
                        sell_date[s_type].append(df.date[idx])
    
    rate['based'] = close[len(close)-1] * (1 - 0.002) / start_date_open
    for s_type in sell_price:
        rate[s_type] = 1.0 
        profit[s_type] = {}
        for i in range(len(buy_price[s_type])):
            try:
                rate[s_type] = rate[s_type] * (sell_price[s_type][i] * (1 - 0.002) / buy_price[s_type][i])
                profit[s_type][buy_date[s_type][i]] = rate[s_type]
                #print s_type,"buy date : %s, buy price : %.2f, sell date : %s, sell price: %.2f" %(buy_date[s_type][i], buy_price[s_type][i], sell_date[s_type][i], sell_price[s_type][i])
            except:
                rate[s_type] = rate[s_type] * (close[len(close)-1] * (1 - 0.002) / buy_price[s_type][len(buy_price[s_type])-1])
                profit[s_type][buy_date[s_type][i]] = rate[s_type]
    rate = sorted(rate.items(),key=lambda x:x[1],reverse=True)
    return rate,profit

rate = {}
profit = {}
strategy = {}
for code in codes[4:5]:
    code = code[0]
    print code
    rate[code], profit[code] = parse(code,'2017-01-01')
    strategy[rate[code][0][0]] = 0

for code in rate:
    strategy[rate[code][0][0]] = strategy[rate[code][0][0]] + 1
    #print code, rate[code][0][0], rate[code][0][1]
    #print code, rate[code][1][0], rate[code][1][1]
    based_profit = pd.DataFrame(profit[code])['based']
    if rate[code][0][0] == 'based':
        best_strategy_profit = pd.DataFrame(profit[code])[rate[code][1][0]].fillna(method='pad')
    else:
        best_strategy_profit = pd.DataFrame(profit[code])[rate[code][0][0]].fillna(method='pad')
    profit_all = pd.concat([based_profit, best_strategy_profit], axis=1)
    plt.plot(profit_all)
    plt.legend(('based_profit', 'best_strategy_profit'), loc='upper center')
    plt.title(code)
    plt.savefig(code+'.jpg')
    plt.close('all')

print 'Best strategy:'
for key in strategy:
    print key, strategy[key]
