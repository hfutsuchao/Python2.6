#coding:utf-8
import pandas as pd
import re

def url_replace(url):
    regex = ['\?.*','\d', '.*?//', '\.haozu.com/\w{2}', '\.haozu.com']
    for i in regex:
        url = re.sub(i, '', url)
    return url

df = pd.read_csv('../sem_roi_ana/result2.csv')
df_op = df[df['pv']==1]
df_mt = df[df['pv']>=2]
df_op = df_op[['url','uid']]
df_mt = df_mt[['url','uid','pv']]

df_op['url'] = df_op['url'].apply(url_replace)
df_mt['url'] = df_mt['url'].apply(url_replace)

result1 = pd.concat([df_op.groupby(['url']).count(),df_op.drop_duplicates().groupby(['url']).count()],axis=1)
result2 = pd.concat([df_mt[['url','pv']].groupby(['url']).count(),df_mt[['url','uid']].drop_duplicates().groupby(['url']).count()],axis=1)
result = pd.concat([result1,result2],axis=1,join='outer')
result.to_csv('./bounce_rate1.csv')