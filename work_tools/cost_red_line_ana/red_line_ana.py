#coding:utf-8
#!/usr/bin/python

import pandas as pd

#city_detail=pd.read_table('city_detail')
demands=pd.read_table('demands')
done_detail=pd.read_table('done_detail')
source_detail=pd.read_table('source_detail')

#source_second_type or source_name
'''def get_result(group_type=['city_name','source_name']):
	global city_detail,demands,done_detail,source_detail
	demands = pd.merge(demands,source_detail,on='source_id',how='inner')
	done_detail = pd.merge(done_detail,city_detail,on='city_id',how='inner')
	done_detail = pd.merge(done_detail,source_detail,on='source_id',how='inner')
	done_count = done_detail.groupby(group_type).count()[['id']].reset_index()
	done_fee = done_detail.groupby(group_type).sum()[['fee']].reset_index()
	demands = demands.groupby(group_type).sum()[['count']].reset_index()
	demands_total = pd.merge(done_count,demands,on=group_type,how='outer')
	demands_total = pd.merge(demands_total,done_fee,on=group_type,how='outer')
	return demands_total'''


def get_result(group_type=['city_name','source_name']):

	global city_detail,demands,done_detail,source_detail
	demands = pd.merge(demands,source_detail,on='source_id',how='inner')
	done_detail = pd.merge(done_detail,demands,on='id',how='inner')
	
	done_count = done_detail.groupby(group_type).count()[['id']].reset_index()
	done_fee = done_detail.groupby(group_type).sum()[['fee']].reset_index()
	
	demands = demands.groupby(group_type).count()[['id']].reset_index()
	
	demands_total = pd.merge(done_count,demands,on=group_type,how='outer')
	demands_total = pd.merge(demands_total,done_fee,on=group_type,how='outer')
	
	return demands_total

#group_type = ['source_second_type']
#group_type = ['city_name','source_second_type']
#group_type = ['city_name','area','source_second_type']
group_type = ['city_name','area']

demands_total = get_result(group_type)
demands_total.to_csv('demands_total.csv')