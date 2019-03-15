#coding:utf-8
import pandas as pd
import re

def url_replace(url):
    regex = ['\?.*','\d', '.*?//', '\.haozu.com/\w{2}', '\.haozu.com']
    for i in regex:
        url = re.sub(i, '', url)
    return url

df = pd.read_csv('./channel')
df_min = df[df['min']==1]
print df_min
exit()
df_1 = df_min.concat(df,join='inner')


result1 = pd.concat([df_op.groupby(['url']).count(),df_op.drop_duplicates().groupby(['url']).count()],axis=1)
result2 = pd.concat([df_mt[['url','pv']].groupby(['url']).count(),df_mt[['url','uid']].drop_duplicates().groupby(['url']).count()],axis=1)
result = pd.concat([result1,result2],axis=1,join='outer')
result.to_csv('./cr.txt')