#coding:utf-8
import pandas as pd
import numpy as np
import talib
#import cral_CNstock_order_ana
from stock_df import GetDf

class GetQuotas(object):
    def __init__(self,df):
        self.__df = df
        
    def __get_quotas(self):
        #stock_amount = cral_CNstock_order_ana.main()
        greeks = GetDf('MOMO',db_file='../stock_option_data.db')
        greeks = greeks.greeks
        greeks['15IV'] = greeks['15IV'].apply(float)
        greeks['24IV'] = greeks['24IV'].apply(float)
        #volume = self.__df['volume'].values
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
        sar.index = self.__df.index
        atr = talib.ATR(high_prices,low_prices,close_prices)
        natr = talib.NATR(high_prices,low_prices,close_prices)
        trange = talib.TRANGE(high_prices,low_prices,close_prices)
        cci = talib.CCI(high_prices,low_prices,close_prices,14)
        dif, dea, bar = talib.MACDFIX(close_prices)
        bar = bar * 2

        #ma5_volume = talib.MA(volume,5)
        #ma10_volume = talib.MA(volume,10)
        #ma20_volume = talib.MA(volume,20)
        #ma30_volume = talib.MA(volume,30)
        #dif_volume, dea_volume, bar_volume = talib.MACDFIX(volume)
        #bar_volume = bar_volume * 2

        df_all = self.__df[['close','volume','high','low']]
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

        #df_all.insert(0,'ma5_volume',ma5_volume)
        #df_all.insert(0,'ma10_volume',ma10_volume)
        #df_all.insert(0,'ma20_volume',ma20_volume)
        #df_all.insert(0,'ma30_volume',ma30_volume)
        #df_all.insert(0,'bar_volume',bar_volume)
        #df_all.insert(0,'dif_volume',dif_volume)
        #df_all.insert(0,'dea_volume',dea_volume)
        
        #df_all = pd.concat([df_all,stock_amount],axis=1)
        
        df_all = pd.concat([df_all,greeks],axis=1)



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
        return df_dif, df_dif_close_plus_one_day,df_all

    def __get_quotas_buy_cmp_sign(self,quotas_elm,cmps=''):
        quotas_elm_tmp = quotas_elm.copy()
        if cmps:
            cmp_g_num, cmp_l_num, cmp_g_each, cmp_l_each = cmps
        else:
            cmp_g_num = {'bar':0, 'cci':100}
            cmp_l_num = {'J':-100}
            cmp_g_each = {'dea':'dif', 'K':'D'}
            cmp_l_each = {'sar':'close', 'ma5':'close', 'ma10':'close', 'ma20':'close', 'ma30':'close'}
            ignore = ['volume']
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

    def __get_quotas_buy_dif_sign(self,quotas_elm):
        keys = list(quotas_elm.keys())
        for k in keys:
            if quotas_elm[k] > 0:
                quotas_elm[k] = 1
            else:
                quotas_elm[k] = 0
        return quotas_elm


    def get_quotas_signs(self,quotas='',type=1):
        if quotas.empty:
            quotas = self.quotas[0].T
        if type == 1:
            quotas.apply(self.__get_quotas_buy_dif_sign)
        elif type == 2:
            quotas.apply(self.__get_quotas_buy_cmp_sign)
        return pd.DataFrame(quotas)


    def __getattr__(self,attr):
        if attr == 'quotas':
            return self.__get_quotas()
        if attr == 'quotas_origin':
            return self.__get_quotas()[2].dropna()

def main():
    from stock_df import GetDf
    t = GetQuotas(GetDf('WB',db_file='../stock_US_data.db').df.set_index('date'))
    s = t.quotas
    print s[1].corr()['close']
    exit()
    r1 = t.get_quotas_signs(s[0].T)
    r2 = t.get_quotas_signs(s[2].T,type=2)
    r = r1.T*r2.T
    corr = s[0].corr()[['close']]
    for k in list(corr.index):
        r[k] = r[k]*corr.loc[k]['close']
    rr = pd.DataFrame(r.dropna().T.sum())
    rr.columns = ['sign']
    print rr[rr['sign']>=3]

if __name__ == '__main__':
    main()
