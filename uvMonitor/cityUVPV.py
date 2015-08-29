#coding:utf-8
import html,hive,time

dts = ["2014-01-"+(''+str(i),str(i))[len(str(i))-1] for i in range(20,21)]

dyn = globals()

cats = ['1|3','5','6','8']

for day in dts:
    for cat in cats:
        dyn['hive'+day+cat] = hive.Hive()
        sql = 'select dt,city,city,count(distinct(uuid)),sum(1) as pv,count(1)/count(distinct(uuid)) as dv,sum(if(gjch regexp "@ad_type=0" and gjch regexp "@agent=0",1,0)) as mianfei_geren,sum(if(gjch regexp "@ad_type=0" and not gjch regexp "@agent=0",1,0)) as mainfei_zhongjie,sum(if(gjch regexp "@ad_type=(2|10|16)(@|$)" and gjch regexp "@agent=0",1,0)) as zhiding_person, sum(if(gjch regexp "@ad_type=(2|10|16)(@|$)" and not gjch regexp "@agent=0",1,0)) as zhiding_zhongjie, sum(if(gjch regexp "@ad_type=7(@|$)",1,0)) as mianfei_jingping,sum(if(gjch regexp "@ad_type=1(@|$)",1,0)) as jingping,sum(if(gjch regexp "@ad_type=6(@|$)",1,0)) as jingjia, sum(if(gjch regexp "@ad_type=17(@|$)",1,0)) as fangxinfang from web_pv_log_detail3 where dt>="' + day + '" and dt<="' + day + '" and cat regexp "^/fang/fang(' + cat + ')/detail" group by dt,city order by dt,pv desc;'
        desc = day + cat[:1] + 'cityUVPV'
        session_name = day + cat[:1] + 'cityUVPV'
        print desc
        dyn['hive'+day+cat].select(sql, desc, session_name)
        time.sleep(1)
    '''
    dyn['hive'+day].desc = day + 'fwsd'
    dyn['hive'+day].session_name = day + 'fwsd'
    '''
    
for day in dts:
    for cat in cats:
        print dyn['hive'+day+cat]
        print dyn['hive'+day+cat].getData()
    