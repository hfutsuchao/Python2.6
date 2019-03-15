#coding:utf-8
import hashlib
import pandas as pd
df = pd.read_csv('./text.txt')
df['p'] = df['p'].apply(str).apply(hashlib.md5)
df['p'] = pd.Series([i.hexdigest() for i in df['p']])
df.to_csv('./md5.txt')

md5file=open('./md5.txt','rb')
md5=hashlib.md5(md5file.read()).hexdigest()
md5file.close()
print(md5)