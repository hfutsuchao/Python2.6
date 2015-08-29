# coding: utf-8
import os,MySQLdb,hashlib
tmp = open('tmp.txt','w')

cats = ['fang1/','fang3/','fang5/','fang6/','fang7/','fang8/','fang9/','fang10/','fang11/','fang12/','fang2/','fang4/']

UvPv = {}
UvPv['all'] = {}
UvPv['all']["uv"] = 0
UvPv['all']["pv"] = 0

count = 0

uuidShown = {}

uuidShown['click'] = {}
uuidShown['show'] = {}

with open("F:\\kuaipan\\MyTools\\Python2.6\\uvMonitor\\data\\12.1-7seoshow_click.txt",'r') as source:
    for userCase in source:
            dt,uuid_shown,type,pos,related_house,is_tg,show_type,tag,atype = userCase.split('\t')
            atype = atype[:-1]
            if uuid_shown == "-":
                continue
            uuidShown[atype][dt + "_" + uuid_shown] = dt + "_" + type + "_" + pos + "_" + related_house + "_" + is_tg + "_" + show_type

print len(uuidShown['show']),len(uuidShown['click'])

for day in range(1,8):
    with open("F:\\kuaipan\\MyTools\\Python2.6\\uvMonitor\\data\\2013-12-0" + str(day) + "fwsd.txt",'r') as source:
        for userCase in source:
            try:
                access_at,cat,ca_source,ca_kw,refer,url,uuid,list_pv,search_pv,detail_pv,index_pv,pv = userCase.split('\t')
                if int(pv[:-1]) >= 200 or uuid == "-":
                    continue
                dt = access_at.split(' ')[0]
            except:
                continue
            
            #pso&&type
            
            try:
                #dt,type,pos,related_house,is_tg,show_type = uuidShown['show'][dt + "_" + uuid]
                pos = uuidShown['show'][dt + "_" + uuid]
            except Exception,e:
                continue
            
            if cat.find('detail') != -1:
                #print pos
                if pos in UvPv:
                    UvPv[pos]["uv"] = UvPv[pos]["uv"] + 1
                    UvPv[pos]["pv"] = UvPv[pos]["pv"] + int(pv[:-1])
                else:
                    UvPv[pos] = {}
                    UvPv[pos]["uv"] = 1
                    UvPv[pos]["pv"] = int(pv[:-1])
                
                '''#各个频道详情页访问深度
                for c in cats:
                    if cat.find(c) != -1:
                        if c in UvPv:
                            UvPv[c]["uv"] = UvPv[c]["uv"] + 1
                            UvPv[c]["pv"] = UvPv[c]["pv"] + int(pv[:-1])
                        else:
                            UvPv[c] = {}
                            UvPv[c]["uv"] = 1
                            UvPv[c]["pv"] = int(pv[:-1])'''
            
            for c in cats:
                if cat.find(c) != -1 and cat.find('detail') != -1:
                    c = c + '_' + pos
                    if c in UvPv:
                        UvPv[c]["uv"] = UvPv[c]["uv"] + 1
                        UvPv[c]["pv"] = UvPv[c]["pv"] + int(pv[:-1])
                    else:
                        UvPv[c] = {}
                        UvPv[c]["uv"] = 1
                        UvPv[c]["pv"] = int(pv[:-1])
            '''            
            pvDivUv = pv[:-1]
            if pvDivUv in UvPv:
                UvPv[pvDivUv]["uv"] = UvPv[pvDivUv]["uv"] + 1
                UvPv[pvDivUv]["pv"] = UvPv[pvDivUv]["pv"] + int(pv[:-1])
            else:
                UvPv[pvDivUv] = {}
                UvPv[pvDivUv]["uv"] = 1
                UvPv[pvDivUv]["pv"] = int(pv[:-1])
            '''
            
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

for cat in UvPv:
    #print cat,"UV:",UvPv[cat]["uv"],"PV:",UvPv[cat]["pv"],"PV/UV:",float(UvPv[cat]["pv"])/UvPv[cat]["uv"]
    #tmp.write(cat+'\t'+"UV:"+'\t'+UvPv[cat]["uv"]+'\t'+"PV:"+'\t'+UvPv[cat]["pv"]+'\t'+"PV/UV:"+'\t'+float(UvPv[cat]["pv"])/UvPv[cat]["uv"]+'\n')
    #print UvPv[cat]["uv"],UvPv[cat]["pv"]
    if UvPv[cat]["uv"] == 0:
        UvPv[cat]["uv"] = 1
    print str(cat)+'\t'+str(UvPv[cat]["uv"])+'\t'+str(UvPv[cat]["pv"])+'\t'+str(float(UvPv[cat]["pv"])/UvPv[cat]["uv"])
    try:
        tmp.write(str(cat)+'\t'+str(UvPv[cat]["uv"])+'\t'+str(UvPv[cat]["pv"])+'\t'+str(float(UvPv[cat]["pv"])/UvPv[cat]["uv"])+'\n')
    except Exception,e:
        print e
        pass