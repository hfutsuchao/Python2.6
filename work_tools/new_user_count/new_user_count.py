#coding:utf-8
#!/usr/bin/python
import pandas as pd
pv=pd.read_csv('newUser')
nu=pd.read_csv('nu').set_index('date')
nud=dict(nu['user_id'])
pv=pv.drop_duplicates()
result = pd.DataFrame()
for key in nud:
	t = pv[pv['date']==key][pv['user_id']>=nud[key]].groupby('date').count()
	result = pd.concat([result,t],axis=0)
print result.sort()