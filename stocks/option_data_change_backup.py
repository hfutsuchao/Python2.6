#!/usr/bin/python
#coding:utf-8
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

DB_CONNECT_STRING = 'sqlite:///stock_option_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)

DB_CONNECT_STRING2 = 'sqlite:///stock_option_data2.db'
engine2 = create_engine(DB_CONNECT_STRING2,echo=False)

data = pd.read_sql('select * from option_greeks;',engine)

for c in data.columns:
	try:   
		data[c] = data[c].astype('float64')
	except Exception,e:
		print e
data = data.drop_duplicates()
data = data.set_index('17Strike')
data.to_sql('option_greeks',engine2,if_exists='append')
#price

#data = pd.read_sql('select * from option_price where date<"2017-06-01";',engine)
data = pd.read_sql('select * from option_price;',engine)
for c in data.columns:
	#data[c][data[c]==''] = np.nan
	try:   
		data[c] = data[c].astype('float64')
	except Exception,e:
		print e
data = data.drop_duplicates()
data = data.set_index('17Strike')
data.to_sql('option_price',engine2,if_exists='append')
