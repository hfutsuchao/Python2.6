#coding:utf-8
import pandas as pd

df = pd.read_csv('./uvpv2.csv')
df = df.drop('Unnamed: 0',axis=1)
df = df[['date','keywordId','uid','url']]
df['date_uid'] = df['date']+df['keywordId'].apply(str) + df['uid']
df_pv = df.groupby(['date_uid']).count()[['uid']]
df_pv.columns = ['pv']
df = df.groupby('date_uid').first()
result = pd.concat([df,df_pv], axis=1, join='inner')
result.to_csv('./result2.csv')