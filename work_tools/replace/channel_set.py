#coding:utf-8
import pandas as pd
import re

def url_replace(url):
    regex = ['^.{1,10}$', '^.{1,7} (.{1,10} )?[\.\d]+平米( ((.{1,2}装修)|(毛坯)))?$']
    for i in regex:
        url = re.sub(i, '', url)
        print url,len(url),len('哈哈 1\n')
    return url

df = pd.read_csv('./ht.csv')
print df['house_title'].head().apply(url_replace)
exit()
result = pd.concat([result1,result2],axis=1,join='outer')
result.to_csv('./cr.txt')