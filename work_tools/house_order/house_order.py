#coding:utf-8
import pandas as pd
from random import random
houses = pd.read_csv('houses')
houses = houses[houses['house_id']>0]
c = list(houses.columns)
c.append('cdb')
cb = houses['city'] + houses['district'] + houses['build']
houses = pd.concat([houses,cb],axis=1)
houses.columns = c
#print houses.sort_values('b_score',ascending=False).head(10)
houses.groupby('cdb').count().groupby('city').count().to_csv('count')

#beijing
house_bj = houses[houses['city']=='北京']
s = (house_bj['b_score']-house_bj['b_score'].min())/(house_bj['b_score'].max()-house_bj['b_score'].min())
house_bj.insert(10,'b_score_a',s)
'''
builds = house_bj['cdb'].drop_duplicates()
for b in builds:
	s_min = house_bj[house_bj['cdb'] == b]['h_score'].min()
	s_max = house_bj[house_bj['cdb'] == b]['h_score'].max()
	house_bj.loc[house_bj['cdb'] == b]['h_score'] = house_bj[house_bj['cdb'] == b]['h_score'].apply(lambda x:(x-s_min)/(s_max-s_min))

'''
t = house_bj['b_score_a']*0.2+house_bj['h_score']*0.7+0.1*random()
house_bj.insert(10,'l_score',t)

#house_bj = house_bj.sort_values('l_score',ascending=False).groupby('cdb').head(100)
house_bj.to_csv('sales_count.csv')