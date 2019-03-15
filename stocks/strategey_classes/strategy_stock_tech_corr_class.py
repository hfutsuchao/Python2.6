#coding:utf-8
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
import talib
import matplotlib.pyplot as plt
from  sklearn import preprocessing
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import time
from commfunction import date_add,today,date_today_delta
import cral_CNstock_order_ana

DB_CONNECT_STRING = 'sqlite:///stock_CN_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

class StockTeckCorrStrategy(object):
    def __init__(self,df,start_date='0',date_delta=60,norm_type='character',quota_index=0,lost=1.0):
        self.df = df
        self.start_date = start_date
        self.date_delta = date_delta
        self.norm_type = norm_type
        self.quota_index = quota_index
        self.lost = lost

    def get_quota(self):
        stock_amount = cral_CNstock_order_ana.main()
        close = self.df['close']
        ma5 = talib.MA(self.df['close'].values,5)
        ma10 = talib.MA(self.df['close'].values,10)
        ma20 = talib.MA(self.df['close'].values,20)
        ma30 = talib.MA(self.df['close'].values,30)
        K, D = talib.STOCH(self.df['high'].values,self.df['low'].values,self.df['close'].values, fastk_period=9, slowk_period=3)
        J = K * 3 - D * 2
        sar = talib.SAR(self.df['high'].values, self.df['low'].values, acceleration=0.05, maximum=0.2)
        sar = pd.DataFrame(sar-close)
        sar.index = df.date
        atr = talib.ATR(self.df['high'].values,self.df['low'].values,self.df['close'].values)
        natr = talib.NATR(self.df['high'].values,self.df['low'].values,self.df['close'].values)
        trange = talib.TRANGE(self.df['high'].values,self.df['low'].values,self.df['close'].values)
        cci = talib.CCI(self.df['high'].values,self.df['low'].values,self.df['close'].values,14)
        dif, dea, bar = talib.MACDFIX(self.df['close'].values)
        bar = bar * 2
        df_all = df.drop(['code','open','low', 'high','volume'],axis=1).set_index('date')
        df_all.insert(0,'ma5',ma5)
        df_all.insert(0,'ma10',ma10)
        df_all.insert(0,'ma20',ma20)
        df_all.insert(0,'ma30',ma30)
        df_all.insert(0,'K',K)
        df_all.insert(0,'D',D)
        df_all.insert(0,'J',J)
        df_all.insert(0,'cci',cci)
        df_all.insert(0,'bar',bar)
        df_all.insert(0,'dif',dif)
        df_all.insert(0,'dea',dea)
        df_all.insert(0,'sar',sar)
        df_all = pd.concat([df_all,stock_amount],axis=1)
        df_yesterday = df_all.T
        index_c = df_all.index
        added = [np.nan] * len(df_all.columns)
        df_yesterday.insert(0, len(df_yesterday.columns), added)
        df_yesterday = df_yesterday.T
        df_yesterday = df_yesterday.drop(df_all.index[len(df_all.index)-1])
        df_yesterday.insert(0, 'index_c', index_c)
        df_yesterday = df_yesterday.set_index('index_c')
        df_dif = df_all - df_yesterday
        df_dif_close_plus_one_day = df_dif.copy()
        for i in range(len(df_dif_close_plus_one_day['close'])-1):
            df_dif_close_plus_one_day['close'][i] = df_dif_close_plus_one_day['close'][i+1]
        df_dif_close_plus_one_day['close'][len(df_dif_close_plus_one_day['close'])-1] = np.nan
        df_dif = df_dif.dropna(axis=0,how='any')
        df_dif_close_plus_one_day = df_dif_close_plus_one_day.dropna(axis=0,how='any')
        #print df_dif_close_plus_one_day.corr()['close']
        return df_dif, df_dif_close_plus_one_day

    def get_normlized(self):
        if self.norm_type == 'max':
            df_norm = self.df.copy()
            for column in self.df.columns:
                df_norm[column] = df_norm[column] / abs(df_norm[column]).max()
        elif norm_type == 'character':
            df_norm = self.df.copy()
            for column in df.columns:
                df_norm[column].ix[df_norm[column] <= 0] = -1
                df_norm[column].ix[df_norm[column] > 0] = 1
        return df_norm

    def get_trade_chance(self):
        #df,close,norm_type,start_date,end_date,lost
        rate = {}
        rate['based'] = {}
        rate['based']['profit'] = {}
        buy_price = {}
        buy_date = {}
        sell_price = {}
        sell_date = {}
        is_buy = {}
        is_sell = {}
        df_dif_norm = self.get_normlized(self.df,self.norm_type)
        df_dif_norm_corr = self.df_dif_norm.corr().ix['close']
        start_date_open = 0
        end_date_open = 0

        for idx in range(len(self.df_dif_norm)):
            date_this = self.df_dif_norm.index[idx]
            close_val = self.close[idx]
            if date_this < self.start_date:
                continue
            if date_this > self.end_date:
                end_date_open = close_val
                break
            
            sign = 0
            for key_name in df_dif_norm.drop('close',axis=1).columns:
                sign = sign + df_dif_norm.ix[date_this,key_name] * df_dif_norm_corr[key_name]

            if start_date_open == 0:
                start_date_open = close_val
                x = idx

            if idx>=1:
                lastdate = df_dif_norm.index[idx-1]
                if lastdate not in rate['based']['profit']:
                    rate['based']['profit'][lastdate] = 1.0
                rate['based']['profit'][date_this] = rate['based']['profit'][lastdate] * self.close[idx] / self.close[idx-1]
            
            for m in np.array(range(-100,200,5))/20.0:
                for n in np.array(range(-100,int(50*m+1),5))/20.0:
                    s_type = 'corr' + str(m) + '_' + str(n)
                    if s_type not in buy_price:
                        buy_price[s_type] = []
                        buy_date[s_type] = []
                        sell_price[s_type] = []
                        sell_date[s_type] = []
                        is_buy[s_type] = 0
                        #is_sell[s_type] = 0
                    if sign>=m:
                        if is_buy[s_type] == 0:
                            is_buy[s_type] = 1
                            buy_price[s_type].append(close_val)
                            buy_date[s_type].append(date_this)
                            #is_sell[s_type] = 0
                            continue

                    if sign<n or (len(buy_price[s_type]) and close_val * (1-0.002) / buy_price[s_type][-1] <= (1-self.lost)): 
                        if is_buy[s_type] == 1 : #and is_sell[s_type] == 0
                            is_buy[s_type] = 0
                            sell_price[s_type].append(close_val)
                            sell_date[s_type].append(date_this)
                            #is_sell[s_type] = 1
        if not end_date_open:
            end_date_open = close_val
        if not start_date_open:
            return []
        rate['based']['profit']['total'] = end_date_open * (1 - 0.002) / start_date_open
        return rate, date_this, buy_price, buy_date, sell_price, sell_date, start_date_open, end_date_open

def back_test(df,start_date='0',date_delta=60,norm_type='character',quota_index=0,lost=1.0):
    if start_date:
        end_date = date_add(start_date,date_delta)
    else:
        end_date = '9'
    if end_date > today():
        return []
    df_dif = get_quota(df)[quota_index]
    df_dif_norm = get_normlized(df_dif)
    df = pd.concat([df.set_index('date')['close'],df_dif_norm['sar']],axis=1).dropna(how='any')
    close = df['close']
    r = get_trade_chance(df_dif,close,norm_type,start_date,end_date,lost)
    if r:
        rate, date_this, buy_price, buy_date, sell_price, sell_date, start_date_open, end_date_open = r
    else:
        return []
    for s_type in sell_price:
        rate[s_type] = {}
        rate[s_type]['profit'] = {}
        rate[s_type]['profit']['total'] = 1.0
        rate[s_type]['trade'] = {}
        for i in range(len(buy_price[s_type])):
            try:
                #rate[s_type]['profit']['total'] = rate[s_type]['profit']['total'] * (sell_price[s_type][i] * (1 - 0.002) / buy_price[s_type][i])
                rate[s_type]['profit']['total'] = rate[s_type]['profit']['total'] * (sell_price[s_type][i] * (1 - 0.002) / buy_price[s_type][i]) * ((sell_price[s_type][i]) * (1 - 0.002) / buy_price[s_type][i+1])
                rate[s_type]['profit'][buy_date[s_type][i]] = rate[s_type]['profit']['total']
                rate[s_type]['trade'][buy_date[s_type][i]] = [buy_date[s_type][i], buy_price[s_type][i], sell_date[s_type][i], sell_price[s_type][i]]
            except Exception,e:
                if len(buy_price[s_type]) == len(sell_price[s_type]):
                    rate[s_type]['profit']['total'] = rate[s_type]['profit']['total'] * (end_date_open * (1 - 0.002) / sell_price[s_type][i])
                else:
                    rate[s_type]['profit']['total'] = rate[s_type]['profit']['total'] * (end_date_open * (1 - 0.002) / buy_price[s_type][i])
                rate[s_type]['profit'][date_this] = rate[s_type]['profit']['total']
                rate[s_type]['trade'][date_this] = [buy_date[s_type][i], buy_price[s_type][i], 'lastday', end_date_open]
    return sorted(rate.items(),key=lambda x:x[1]['profit']['total'],reverse=True)

def plot_profit(rate,s_type=''):
    for code in rate:
        best_strategy_code = rate[code][0][0]
        rate_dic = dict(rate[code])
        based_profit = pd.DataFrame(rate_dic['based']).drop('total',axis=0)
        if s_type:
            best_strategy_profit = pd.DataFrame(rate_dic[s_type]).fillna(method='pad').drop('total',axis=0)
            best_strategy_code = s_type
        else:
            if rate[code][0][0] == 'based':
                best_strategy_profit = pd.DataFrame(rate_dic[rate[code][1][0]]).fillna(method='pad').drop('total',axis=0)
            else:
                best_strategy_profit = pd.DataFrame(rate_dic[rate[code][0][0]]).fillna(method='pad').drop('total',axis=0)
        profit_all = pd.concat([based_profit['profit'], best_strategy_profit['profit']], axis=1).fillna(method='pad')
        profit_all.plot()
        plt.legend(('based_profit', 'best_strategy_profit'), loc='upper left')
        plt.title(code + '_' + best_strategy_code)
        plt.savefig('/Users/NealSu/Downloads/profit_pic/' + code + '_' + best_strategy_code + '.jpg')
        plt.close('all')
        try:
            print code
            print best_strategy_profit['trade']
        except:
            pass      

def strategy_choose(rate):
    strategy_sum = {}
    best_strategy = {}
    for code in rate:
        rate_dic = dict(rate[code])
        best_strategy_code = rate[code][0][0]
        if best_strategy_code not in best_strategy:
            best_strategy[best_strategy_code] = 1
        else:
            best_strategy[best_strategy_code] = best_strategy[best_strategy_code] + 1
        for s_type in rate_dic:
            if s_type not in strategy_sum:
                strategy_sum[s_type] = rate_dic[s_type]['profit']['total']
            else:
                strategy_sum[s_type] = strategy_sum[s_type] + rate_dic[s_type]['profit']['total']
    best_strategy = sorted(best_strategy.items(),key=lambda x:x[1],reverse=True)
    strategy_sum = sorted(strategy_sum.items(),key=lambda x:x[1],reverse=True)
    return (best_strategy,strategy_sum)

def single_test(df,start_dates,date_deltas,norm_type,quota_index):
    rate = {}
    for start_date in start_dates:
        for date_delta in date_deltas:
            r = back_test(df, start_date, date_delta, norm_type, quota_index)
            if r:
                rate[start_date+'_'+date_add(start_date,date_delta)] = r
    return rate

def main():
    #codes = session.execute('select distinct(code) from day_k_data;').fetchall()
    codes = [['002230']]
    rate = {}
    start_date = '2017-01-04'
    date_delta = -date_today_delta(start_date,'%Y-%m-%d')
    norm_type = 'character'
    quota_index = 0
    codes = [code[0] for code in codes]

    #date_deltas = range(50,200,20)
    #start_dates = [date_add(start_date,i) for i in range(10,50,10)]
    
    df = pd.read_sql('select * from day_k_data where code="MOMO" order by date asc;',engine)
    #rate = single_test(df,start_dates,date_deltas,norm_type,quota_index)
    #open_market_dates = session.execute('select distinct(code),date from day_k_data;').fetchall()

    for code in codes[:1]:
        print code
        try:
            df = pd.read_sql('select * from day_k_data where code="'+code+'" order by date asc;',engine)
            for i in range(len(df['date'])):
                df.date[i] = df.date[i].split(' ')[0]
            r = back_test(df, start_date, date_delta, norm_type, quota_index)
            if r:
                rate[code] = r
        except Exception,e:
            print e,'line 212'
            continue

    best_strategy, strategy_sum = strategy_choose(rate)
    plot_profit(rate,strategy_sum[0][0])
    #plot_profit(rate)

    print 'Best strategy:'
    for elm in best_strategy:
        print elm[0],elm[1]

    print 'The Best strategy:'
    print strategy_sum[0][0],strategy_sum[0][1]
    print strategy_sum[1][0],strategy_sum[1][1]

if __name__ == '__main__':
    main()
