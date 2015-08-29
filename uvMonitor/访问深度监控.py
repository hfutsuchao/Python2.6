#coding:utf-8
import html,hive,time

dts = ["2013-12-"+('0'+str(i),str(i))[len(str(i))-1] for i in range(1,8)]

dyn = globals()

for day in dts:
    dyn['hive'+day] = hive.Hive()
    sql = 'select topn(1,array(FROM_UNIXTIME(access_at),cat,ca_source,ca_kw,refer,url),array(access_at),array(true)),uuid,sum(if(instr(cat,"list")>0,1,0)), sum(if(instr(cat,"search")>0,1,0)) as search_pv, sum(if(instr(cat,"detail")>0,1,0)) as detail_pv, sum(if(instr(cat,"index")>0,1,0)) as index_pv, count(1) as pv from web_pv_log_detail3 where dt="' + day + '" and cat regexp "/fang/" group by uuid order by pv desc;'
    #sql = 'select topn(1,array(FROM_UNIXTIME(access_at),cat,ca_source,ca_kw,refer,url),array(access_at),array(true)),uuid,sum(if(instr(cat,"list")>0,1,0)), sum(if(instr(cat,"search")>0,1,0)) as search_pv, sum(if(instr(cat,"detail")>0,1,0)) as detail_pv, sum(if(instr(cat,"index")>0,1,0)) as index_pv, count(1) as pv from web_pv_log_detail3 where dt="' + day + '" and cat regexp "/fang/" and ca_name regexp "edm_job-post" group by uuid order by pv desc;'
    #sql = 'select topn(1,array(FROM_UNIXTIME(access_at),cat,url),array(access_at),array(true)),count(distinct uuid), count(1) as pv from web_pv_log_detail3 where dt="' + day + '" and cat regexp "/fang/" and ca_name regexp "edm_job-post" group by uuid order by pv desc;'
    #sql = "select dt,count(distinct uuid) from web_pv_log_detail3 where dt = '" + day + "' and cat regexp '/fang/' and (ca_name regexp 'fang-yjjl' or ca_name regexp ' fang-yjxg' or ca_name regexp 'fang-szjl' or ca_name regexp 'fang-szxg') group by dt;"
    desc = day + 'fwsd'
    session_name = day + 'fwsd'
    print desc
    dyn['hive'+day].select(sql, desc, session_name)
    time.sleep(1)
    '''
    dyn['hive'+day].desc = day + 'fwsd'
    dyn['hive'+day].session_name = day + 'fwsd'
    '''
    
for day in dts:
    print dyn['hive'+day]
    print dyn['hive'+day].getData()
    