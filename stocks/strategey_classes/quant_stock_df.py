#coding:utf-8
import pandas as pd
import numpy as np
import talib
import cral_CNstock_order_ana

class GetStockDf(object):
    def __init__(self,code,start_date='0',end_date='9'):
        self.__code = code
        self.__start_date = start_date
        self.__end_date = end_date
        
    def get_quota(self):
        #stock_amount = cral_CNstock_order_ana.main()
        close = self.__df['close']
        high_prices = self.__df['high'].values
        low_prices = self.__df['low'].values
        close_prices = close.values
        ma5 = talib.MA(close_prices,5)
        ma10 = talib.MA(close_prices,10)
        ma20 = talib.MA(close_prices,20)
        ma30 = talib.MA(close_prices,30)
        K, D = talib.STOCH(high_prices,low_prices,close_prices, fastk_period=9, slowk_period=3)
        J = K * 3 - D * 2
        sar = talib.SAR(high_prices, low_prices, acceleration=0.05, maximum=0.2)
        sar = pd.DataFrame(sar-close)
        sar.index = self.__df.date
        atr = talib.ATR(high_prices,low_prices,close_prices)
        natr = talib.NATR(high_prices,low_prices,close_prices)
        trange = talib.TRANGE(high_prices,low_prices,close_prices)
        cci = talib.CCI(high_prices,low_prices,close_prices,14)
        dif, dea, bar = talib.MACDFIX(close_prices)
        bar = bar * 2
        df_all = self.__df.drop(['code','open','low', 'high','volume'],axis=1).set_index('date')
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
        #df_all = pd.concat([df_all,stock_amount],axis=1)
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
        return df_dif, df_dif_close_plus_one_day

    def get_normlized(self,df):
        df_norm = df.copy()
        if self.__norm_type == 'max':
            for column in df_norm.columns:
                df_norm[column] = df_norm[column] / abs(df_norm[column]).max()
        elif self.__norm_type == 'character':
            for column in df_norm.columns:
                df_norm[column].ix[df_norm[column] <= 0] = -1
                df_norm[column].ix[df_norm[column] > 0] = 1
        else:
            return None
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
        df_dif_norm = self.get_normlized(self.df,self.__norm_type)
        df_dif_norm_corr = self.df_dif_norm.corr().ix['close']
        start_date_open = 0
        end_date_open = 0

        for idx in range(len(self.df_dif_norm)):
            date_this = self.df_dif_norm.index[idx]
            close_val = self.close[idx]
            if date_this < self.__start_date:
                continue
            if date_this > self.__end_date:
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
    if self.__start_date:
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
