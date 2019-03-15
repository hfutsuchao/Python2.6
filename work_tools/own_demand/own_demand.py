#coding:utf-8
import pandas as pd
sales = pd.read_csv('sales.txt')
count = pd.read_csv('count.txt')

sales_count = sales[['director_id','id']].groupby('director_id').count()
own_count = count[['director_id','count']].groupby('director_id').sum()
sales_count.to_csv('sales_count.csv')
own_count.to_csv('own_count.csv')
