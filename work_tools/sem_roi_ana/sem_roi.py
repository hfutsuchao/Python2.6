#coding:utf-8
import pandas as pd
import re

df = pd.read_csv('./result2.csv')
cost = pd.read_csv('./cost2.csv')
kwid = pd.read_csv('./kwid2.csv').groupby('keywordId').first().drop('terminal',axis=1).drop(0,axis=0)
cost = pd.concat([cost.groupby('keywordId').sum().drop(['avg(sr.position)','terminal','subcategory'],axis=1),cost.groupby('keywordId').mean()[['avg(sr.position)','terminal','subcategory']]],axis=1,join='inner')

df = df.drop('date_uid',axis=1)
df_sem = df[df['url'].str.contains('sem')]
#df_keyword = df[df['keywordId']!=0]

#keyword uvpv
df_sem_uv = df_sem.groupby(['keywordId']).count()[['pv']].drop(0,axis=0)
df_sem_uv.columns = ['uvc']
df_sem_pv = df_sem.groupby(['keywordId']).sum()[['pv']].drop(0,axis=0)
df_sem_pv.columns = ['pvc']
df_sem_uvpv = pd.concat([df_sem_uv,df_sem_pv],axis=1,join='inner')
print 1

#onepv
df_sem_onepv = df_sem[df_sem['pv']==1]
df_sem_onepv_uv = df_sem_onepv.groupby(['keywordId']).count()[['uid']].drop(0,axis=0)
df_sem_onepv_uv.columns = ['onepv_uvc']
print 2

#more than onepv
df_sem_mt_onepv = df_sem[df_sem['pv']>=2]
df_sem_mt_onepv_uv = df_sem_mt_onepv.groupby(['keywordId']).count()[['uid']].drop(0,axis=0)
df_sem_mt_onepv_uv.columns = ['mt_uvc']
df_sem_mt_onepv_pv = df_sem_mt_onepv.groupby(['keywordId']).sum()[['pv']].drop(0,axis=0)
df_sem_mt_onepv_pv.columns = ['mt_pvc']
df_sem_mt_onepv_uvpv = pd.concat([df_sem_mt_onepv_uv,df_sem_mt_onepv_pv],axis=1,join='inner')
print 3

#test
df_sem_onepv.to_csv('df_sem_onepv.csv')
df_sem_mt_onepv.to_csv('df_sem_mt_onepv.csv')

df_kw = pd.concat([df_sem_onepv_uv,df_sem_mt_onepv_uvpv],axis=1,join='outer')
df_sem = df_sem.groupby('keywordId').sum().drop('pv',axis=1)

df_sem_kw_uvpv_cost = pd.concat([df_sem,df_kw,df_sem_uvpv,cost,kwid],axis=1,join='inner')
df_sem_kw_uvpv_cost.to_csv('./df_sem_kw_uvpv_cost2.csv')
