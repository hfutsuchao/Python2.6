#coding:utf-8
import pandas as pd

'''fo = open('./search.csv','r').read()
fw = open('./search1.csv','w')
fo = fo.replace('\\\\','').replace('\\\"','')
fw.write(fo)
fw.close()
exit()
'''

df = pd.read_csv('./search.csv')

def get_keyword(url):
    if '=' in url:
    	kw = url.split('=')[1].split('&')[0]
    else:
    	kw = ''
    return kw

df['url'] = df['url'].apply(get_keyword)
df['tck'] = df['terminal'] + df['cityId'] + df['url']

df = df.groupby('tck').count()[['cityId']].sort_values('cityId',ascending=False)
df.to_csv('./result.csv')
