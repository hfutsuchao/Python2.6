#coding:utf-8
#!/usr/bin/python
import pandas as pd
house=pd.read_table('house')
h_pv=pd.read_table('house_pvlog')
p_demand=pd.read_table('demand')
r = pd.merge(house,h_pv,on='id',how='inner')
def slice_100(num):
	return int(num/100)
r['area'] = r['area'].apply(slice_100)
ta = r.groupby(['city_id','area']).sum()[['pv']]
tc = r.groupby(['city_id','district_name','street_name']).sum()[['pv']]

p_demand['area'] = p_demand['area'].apply(slice_100)
p_demand.insert(3,'new',0)
pa = p_demand.groupby(['city_name','area']).count()
pc = p_demand.groupby(['city_name','district_name','street_name']).count()
ta.to_csv('ta.csv')
tc.to_csv('tc.csv')
pa.to_csv('pa.csv')
pc.to_csv('pc.csv')