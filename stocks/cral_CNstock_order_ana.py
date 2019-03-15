#coding:utf-8
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker

class StockAmount(object):
    def __init__(self,datas,big_trade,mid_trade):
        '''
        datas shoud be a DataFrame inclouding date,code,amount,type.
        '''
        self.datas = datas
        self.big_trade = big_trade
        self.mid_trade = mid_trade
        self.dates = datas['date'].drop_duplicates()
        self.buy_datas = datas[datas['type']=='buy']
        self.sell_datas = datas[datas['type']=='sell']
        self.equal_datas = datas[datas['type']=='equal']
        self.big_buy_amount = {}
        self.big_sell_amount = {}
        self.buy_total_amount = {}
        self.sell_total_amount = {}
        self.equal_total_amount = {}
        self.bs_total_amount = {}
        self.total_total_amount = {}

    def big_buy(self):
        for date in self.dates:
            self.big_buy_amount[date] = self.buy_datas['amount'][(self.buy_datas['date']==date) & (self.buy_datas['amount']>=self.big_trade)].sum()
        return self.big_buy_amount

    def big_sell(self):
        for date in self.dates:
            self.big_sell_amount[date] = self.sell_datas['amount'][(self.sell_datas['date']==date) & (self.sell_datas['amount']>=self.big_trade)].sum()
        return self.big_sell_amount

    def buy_amount(self):
        for date in self.dates:
            self.buy_total_amount[date] = self.buy_datas['amount'][self.buy_datas['date']==date].sum()
        return self.buy_total_amount

    def sell_amount(self):
        for date in self.dates:
            self.sell_total_amount[date] = self.sell_datas['amount'][self.sell_datas['date']==date].sum()
        return self.sell_total_amount

    def equal_amount(self):
        for date in self.dates:
            self.equal_total_amount[date] = self.equal_datas['amount'][self.equal_datas['date']==date].sum()
        return self.equal_total_amount

    def bs_amount(self):
        if not self.buy_total_amount:
            self.buy_total_amount = self.buy_amount()
        if not self.sell_total_amount:
            self.sell_total_amount = self.sell_amount()
        for date in self.dates:
            self.bs_total_amount[date] = self.buy_total_amount[date] - self.sell_total_amount[date]
        return self.bs_total_amount
    
    def total_amount(self):
        if not self.buy_total_amount:
            self.buy_total_amount = self.buy_amount()
        if not self.sell_total_amount:
            self.sell_total_amount = self.sell_amount()
        if not self.equal_total_amount:
            self.equal_total_amount = self.equal_amount()
        for date in self.dates:
            self.total_total_amount[date] = self.buy_total_amount[date] + self.sell_total_amount[date] + self.equal_total_amount[date]
        return self.total_total_amount

    def __getattr__(self,attr):
        if attr == 'big_buy_df':
            return pd.DataFrame(pd.Series(self.big_buy()).T,columns=['big_buy'])
        if attr == 'big_sell_df':
            return pd.DataFrame(pd.Series(self.big_sell()).T,columns=['big_sell'])
        if attr == 'buy_amount_df':
            return pd.DataFrame(pd.Series(self.buy_amount()).T,columns=['buy_amount'])
        if attr == 'sell_amount_df':
            return pd.DataFrame(pd.Series(self.sell_amount()).T,columns=['sell_amount'])
        if attr == 'equal_amount_df':
            return pd.DataFrame(pd.Series(self.equal_amount()).T,columns=['equal_amount'])
        if attr == 'bs_amount_df':
            return pd.DataFrame(pd.Series(self.bs_amount()).T,columns=['bs_amount'])
        if attr == 'total_amount_df':
            return pd.DataFrame(pd.Series(self.total_amount()).T,columns=['total_amount'])
        if attr == 'all':
            return pd.concat([self.big_buy_df,self.big_sell_df,self.buy_amount_df,self.sell_amount_df,self.equal_amount_df,self.bs_amount_df,self.total_amount_df],axis=1)

def main():
    DB_CONNECT_STRING = 'sqlite:///stock_CN_data.db'
    engine = create_engine(DB_CONNECT_STRING,echo=False)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    df = pd.read_sql('select date,`type`,amount,code from day_order_data where code = "002230";',engine)
    b_r = 0.00005
    mp = 446.74*100000000
    s = StockAmount(df,b_r*mp,0)
    return s.all

if __name__ == '__main__':
    print main()