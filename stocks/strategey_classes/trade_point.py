#coding:utf-8
from normalized import GetNormalized
from getquotas import GetQuotas
import numpy as np
import pandas as pd

class GetTradePoint(object):
    def __init__(self,df,start_date,end_date,norm_type='max',quota_index=0,lost=1.0):
        self.__df = df
        self.__start_date = start_date
        self.__end_date = end_date
        self.__norm_type = norm_type
        self.__quota_index = quota_index
        self.__lost = lost
        self.__quotas = GetQuotas(self.__df).quotas[self.__quota_index]
        self.__close = self.__df['close']
        self.__close = pd.concat([self.__close,self.__quotas[['sar']]],axis=1).dropna()['close']
        self.__rate = {}
        self.__rate['based'] = {}
        self.__rate['based']['profit'] = {}

    def get_sign_score(self,quotas,close=''):
        signs = pd.DataFrame()
        if not close:
            close = self.__close
        quotas_corr = quotas.corr().ix['close']
        for idx in range(len(quotas)):
            date_this = quotas.index[idx]
            close_val = close[idx]
            sign = 0
            for key_name in quotas.drop('close',axis=1).columns:
                sign = sign + quotas.ix[date_this,key_name] * quotas_corr[key_name]
            signs.insert(0,date_this,pd.Series(sign))
        signs.index = ['sign']
        return signs.T.sort()


    def __get_quotas_cmp_sign(self,quotas_elm,cmps='',types=''):
        if cmps != '':
            cmp_g_num, cmp_l_num, cmp_g_each, cmp_l_each, ignore = cmps
        elif types == 'buy' or types == '':
            cmp_g_num = {'bar':0, 'cci':100}
            cmp_l_num = {'J':-100}
            cmp_g_each = {'dea':'dif', 'K':'D'}
            cmp_l_each = {'sar':'close', 'ma5':'close', 'ma10':'close', 'ma20':'close', 'ma30':'close'}
            ignore = ['volume']
        elif types == 'sell':
            cmp_l_num = {'bar':0, 'cci':0}
            cmp_g_num = {'J':100}
            cmp_l_each = {'dea':'dif', 'K':'D'}
            cmp_g_each = {'sar':'close', 'ma5':'close', 'ma10':'close', 'ma20':'close', 'ma30':'close'}
            ignore = ['volume']
        elif types == 'pm':
            cmp_g_num = {}
            cmp_l_num = {'bar':0, 'cci':0, 'J':0, 'sar':0, 'ma5':0, 'ma10':0, 'ma20':0, 'ma30':0, 'volume':0, 'dea':0, 'dif':0, 'K':0, 'D':0}
            cmp_g_each = {}
            cmp_l_each = {}
            ignore = []

        quotas_elm_tmp = quotas_elm.copy()
        for k in cmp_g_num:
            if quotas_elm_tmp[k] >= cmp_g_num[k]:
                quotas_elm[k] = 1
            else:
                quotas_elm[k] = 0
        
        for k in cmp_l_num:
            if quotas_elm_tmp[k] <= cmp_l_num[k]:
                quotas_elm[k] = 1
            else:
                quotas_elm[k] = 0

        for k in cmp_g_each:
            if quotas_elm_tmp[k] >= quotas_elm_tmp[cmp_g_each[k]]:
                quotas_elm[k] = 1
                quotas_elm[cmp_g_each[k]] = 1
            else:
                quotas_elm[k] = 0
                quotas_elm[cmp_g_each[k]] = 0

        for k in cmp_l_each:
            if quotas_elm_tmp[k] <= quotas_elm_tmp[cmp_l_each[k]]:
                quotas_elm[k] = 1
                quotas_elm[cmp_l_each[k]] = 1
            else:
                quotas_elm[k] = 0
                quotas_elm[cmp_l_each[k]] = 0

        for k in ignore:
            quotas_elm[k] = 1

        return quotas_elm

    def get_quotas_signs(self,quotas='',types=''):
        if quotas.empty:
            quotas = self.quotas.T
        quotas.apply(self.__get_quotas_cmp_sign)
        return pd.DataFrame(quotas)



    def __get_sign_corr_score(self,quotas,close='',type_=''):
        r1 = self.get_quotas_signs(quotas[0].T)
        r2 = self.get_quotas_signs(quotas[2].T)
        r = r1.T*r2.T
        corr = quotas[0].corr()[['close']]
        for k in list(corr.index):
            r[k] = r[k]*corr.loc[k]['close']
        rr = pd.DataFrame(r.dropna().T.sum())
        rr.columns = ['sign']
        return rr

    def get_trade_sign(self,signs,start_date='',end_date=''):
        if not start_date:
            start_date = self.__start_date
        if not end_date:
            end_date = self.__end_date
        
        trade_types = {}
        trade_types['buy'] = {}
        trade_types['sell'] = {}
        is_buy = {}
        is_sell = {}
        signs = signs.loc[start_date:end_date]
        close = self.__close.loc[start_date:end_date]
        self.__start_date_open = close[0]
        self.__end_date_open = close[-1]
        close = iter(close)
        for date_this in list(signs.index):
            close_val = close.next()
            sign = signs.ix[date_this,'sign']
            try:
                if lastdate not in self.__rate['based']['profit']:
                    self.__rate['based']['profit'][lastdate] = 1.0
                self.__rate['based']['profit'][date_this] = self.__rate['based']['profit'][lastdate] * close_val / close_val_lastday
            except:
                print 'get_trade_sign exception'
                pass

            for m in np.array(range(-100,200,5))/20.0:
                for n in np.array(range(-100,int(50*m+1),5))/20.0:
                    strategy_name = 'corr' + str(m) + '_' + str(n)
                    if strategy_name not in trade_types['buy']:
                        trade_types['buy'][strategy_name] = []
                        trade_types['sell'][strategy_name] = []
                        is_buy[strategy_name] = 0
                        #is_sell[strategy_name] = 0

                    if sign>=m:
                        if is_buy[strategy_name] == 0:
                            is_buy[strategy_name] = 1
                            trade_types['buy'][strategy_name].append({date_this:close_val})
                            #is_sell[strategy_name] = 0
                    elif sign<n or (len(trade_types['buy'][strategy_name]) and close_val * (1-0.002) / trade_types['buy'][strategy_name][-1].values()[0] <= (1-self.__lost)): 
                        if is_buy[strategy_name] == 1 : #and is_sell[strategy_name] == 0
                            is_buy[strategy_name] = 0
                            trade_types['sell'][strategy_name].append({date_this:close_val})
                            #is_sell[strategy_name] = 1
            lastdate = date_this
            close_val_lastday = close_val
        return trade_types

    def get_trade_point(self,quotas=''):
        buy_price = {}
        buy_date = {}
        sell_price = {}
        sell_date = {}
        is_buy = {}
        is_sell = {}
        if not quotas:
            quotas = self.__quotas
        quotas_norm = GetNormalized(quotas,self.__norm_type).norm[self.__norm_type]
        signs = self.get_sign_score(quotas_norm)
        trade_types = self.get_trade_sign(signs,self.__start_date,self.__end_date)
        self.__rate['based']['profit']['total'] = self.__end_date_open * (1 - 0.002) / self.__start_date_open
        return trade_types

    def __getattr__(self,attr):
        if attr == 'trade_sign':
            return self.get_trade_sign()
        elif attr == 'trade_point':
            return self.get_trade_point()
        elif attr == 'rate':
            return self.__rate
        elif attr == 'end_date_open':
            return self.__end_date_open
        elif attr == 'end_date':
            return self.__end_date

def main():
    from stock_df import GetDf
    df = GetDf('WB',db_file='../stock_US_data.db').df.set_index('date').drop(['code'],axis=1)
    t = GetTradePoint(df,'2016-01-04','2017-05-15',norm_type='pm')
    sr = t.trade_point
    for s in sr['sell']:
        if len(sr['sell'][s])>=10:
            print s,sr['sell'][s]

if __name__ == '__main__':
    main()
