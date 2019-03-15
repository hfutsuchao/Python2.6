#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts

def get_all_price(code_list):
    '''process all stock'''
    df = ts.get_realtime_quotes(code_list)
    print df[['open','price','high','low']]
    df = ts.get_index()
    print df.ix[[0,12,17],['name','open','close','change']]

if __name__ == '__main__':
    STOCK = [
             '000651',
             '000333',
             '002230',
             '600036',
             ]

    get_all_price(STOCK)
