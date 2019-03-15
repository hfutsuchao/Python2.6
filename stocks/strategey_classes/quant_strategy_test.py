#coding:utf-8
import pandas as pd
from quants import QuantS
from trade_point_corr_pm import GetTradePoint
from trade_point import GetTradePoint as GP
from stock_df import GetDf

def main():
    df = GetDf('MOMO',db_file='../stock_US_data.db').df.set_index('date')[['open','close','high','low','volume']]
    t = GetTradePoint(df,'2017-01-04','2017-06-15',norm_type='max')
    trade_types = t.trade_point
    end_date_open = t.end_date_open
    rate = t.rate
    end_date = t.end_date
    s = QuantS()
    rs = {}
    rs['WB'] = s.trade_records_C(trade_types,rate,end_date,end_date_open)
    sn = s.strategy_choose(rs)[0][0][0]
    s.strategy_profit(rs,sn)

if __name__ == '__main__':
    main()