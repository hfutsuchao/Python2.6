# coding: utf-8
import os,MySQLdb,hashlib,time

dateToday = time.strftime('%Y-%m-%d',time.localtime(time.time() - 86400))

dateEarly = time.strftime('%Y-%m-%d',time.localtime(time.time() - 86400*2))

cats = ['fang1/','fang3/','fang5/','fang6/','fang7/','fang8/','fang9/','fang10/','fang11/','fang12/','fang2/','fang4/']

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

UvPv = {}
UvPv['all'] = {}
UvPv['all']["uv"] = 0
UvPv['all']["pv"] = 0
count = 0

import hive
#查询数据
sql = 'select topn(1,array(FROM_UNIXTIME(access_at),cat,ca_source,url_decoding(ca_kw),url_decoding(refer),url),array(access_at),array(true)),uuid,sum(if(instr(cat,"list")>0,1,0)), sum(if(instr(cat,"search")>0,1,0)) as search_pv, sum(if(instr(cat,"detail")>0,1,0)) as detail_pv, sum(if(instr(cat,"index")>0,1,0)) as index_pv, count(1) as pv from web_pv_log_detail3 where dt>="' + dateEarly + '" and dt<="' + dateToday  + '" and cat regexp "/fang/" group by uuid order by pv desc;'
desc = 'FangLastSevenDayPVUV'
session_name = 'FangLastSevenDayPVUV'

hive = hive.Hive()
hive.select(sql, desc, session_name)
hive.getData()

source = hive.outContent

for userCase in source:
    try:
        #print userCase
        access_at,cat,ca_source,ca_kw,refer,url,uuid,list_pv,search_pv,detail_pv,index_pv,pv = userCase.split('\t')
        '''if int(pv[:-1]) >= 100 or uuid == "-":
            continue'''
    except:
        continue
    
    h=hashlib.md5()
    h.update(uuid)
    pos = int(hex2dec(h.hexdigest()[0:3]))%3 + 1
    pos = access_at[:10] + "\t" + str(pos)
    cat = access_at[:10] + "\t" + cat
    
    if cat.find('detail') != -1:
        if pos in UvPv:
            UvPv[pos]["uv"] = UvPv[pos]["uv"] + 1
            UvPv[pos]["pv"] = UvPv[pos]["pv"] + int(pv[:-1])
        else:
            UvPv[pos] = {}
            UvPv[pos]["uv"] = 1
            UvPv[pos]["pv"] = int(pv[:-1])
    
    for c in cats:
        if cat.find(c) != -1:
            if c in UvPv:
                UvPv[c]["uv"] = UvPv[c]["uv"] + 1
                UvPv[c]["pv"] = UvPv[c]["pv"] + int(pv[:-1])
            else:
                UvPv[c] = {}
                UvPv[c]["uv"] = 1
                UvPv[c]["pv"] = int(pv[:-1])
    
    pvDivUv = pv[:-1]
    if pvDivUv in UvPv:
        UvPv[pvDivUv]["uv"] = UvPv[pvDivUv]["uv"] + 1
        UvPv[pvDivUv]["pv"] = UvPv[pvDivUv]["pv"] + int(pv[:-1])
    else:
        UvPv[pvDivUv] = {}
        UvPv[pvDivUv]["uv"] = 1
        UvPv[pvDivUv]["pv"] = int(pv[:-1])
    
    dt = access_at.split(' ')[0]
    if dt in UvPv:
        UvPv[dt]["uv"] = UvPv[dt]["uv"] + 1
        UvPv[dt]["pv"] = UvPv[dt]["pv"] + int(pv[:-1])
    else:
        UvPv[dt] = {}
        UvPv[dt]["uv"] = 1
        UvPv[dt]["pv"] = int(pv[:-1])
    
    if cat in UvPv:
        UvPv[cat]["uv"] = UvPv[cat]["uv"] + 1
        UvPv[cat]["pv"] = UvPv[cat]["pv"] + int(pv[:-1])
    else:
        UvPv[cat] = {}
        UvPv[cat]["uv"] = 1
        UvPv[cat]["pv"] = int(pv[:-1])
    
    UvPv['all']["uv"] = UvPv['all']["uv"] + 1
    UvPv['all']["pv"] = UvPv['all']["pv"] + int(pv[:-1])

try:
    tmp = open('FangLastSevenDayPVUV.txt','w')
except Exception,e:
    print e
for cat in UvPv:
    #print cat,"UV:",UvPv[cat]["uv"],"PV:",UvPv[cat]["pv"],"PV/UV:",float(UvPv[cat]["pv"])/UvPv[cat]["uv"]
    #tmp.write(cat+'\t'+"UV:"+'\t'+UvPv[cat]["uv"]+'\t'+"PV:"+'\t'+UvPv[cat]["pv"]+'\t'+"PV/UV:"+'\t'+float(UvPv[cat]["pv"])/UvPv[cat]["uv"]+'\n')
    print UvPv[cat]["uv"],UvPv[cat]["pv"]
    try:
        tmp.write(str(cat)+'\t'+str(UvPv[cat]["uv"])+'\t'+str(UvPv[cat]["pv"])+'\t'+str(float(UvPv[cat]["pv"])/UvPv[cat]["uv"])+'\n')
    except:
        pass