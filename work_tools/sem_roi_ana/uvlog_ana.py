#coding:utf-8
import pandas as pd

#df = pd.read_csv('./query_result.csv')
df = pd.read_csv('./uvlog.csv')
#df = df.drop('Unnamed: 0',axis=1)
#df = df[['date','keywordId','uid','url']]
#df['date_uid'] = df['date']+df['keywordId'].apply(str) + df['uid']
df_uv_pv = df.groupby(['dt','uid'])[['uid']].count()
uv = df_uv_pv.groupby('dt').count()
uv_1 = df_uv_pv[df_uv_pv['uid']==1].groupby('dt').count()
uv_2 = df_uv_pv[df_uv_pv['uid']==2].groupby('dt').count()
uv_3_more = df_uv_pv[df_uv_pv['uid']>2].groupby('dt').count()

#print uv,uv_3_more
#df_pv.columns = ['pv']
#df = df.groupby('date_uid').first()
result = pd.concat([uv,uv_1,uv_2,uv_3_more], axis=1, join='inner')
print result
result.to_csv('./result_uv.csv')