#coding:utf-8
import pandas as pd
pv=pd.read_csv('portal_ref_pv')
#for i in range(len(pv)):
#	pv.loc[i]['pt'] = pv.loc[i]['pt'].split('=')[0]

print len(pv[['uuid']]),len(pv[['uuid']].drop_duplicates())
exit()
cat_d = pv[['pt','uuid']].groupby('pt').count()
cat_d_p = cat_d[cat_d['uuid']>=1]
cat_d = pv[['pt','uuid']].drop_duplicates().groupby('pt').count()
cat_d_u = cat_d[cat_d['uuid']>=1]
cat_d_u.columns = ['uv']
cat_d_p.columns = ['pv']
cat = pd.concat([cat_d_p,cat_d_u],axis=1)
print cat[cat['uv']>=20]
#print cat_d_p
#print cat_d_u
#print cat[cat['uuid']>=50]