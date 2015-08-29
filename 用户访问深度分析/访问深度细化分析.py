# coding: utf-8
import os,MySQLdb,hashlib
#import changeNum.py
#source = open('C:\\Users\\suchao\\Desktop\\7.1~4fangPV.txt').readlines()
tmp = open('C:\\Users\\suchao\\Desktop\\tmp.txt','w')


def hex2dec(string_num):  
    return str(int(string_num.upper(), 16))

UvPv = {}

# 
yd = open('C:\\Users\\suchao\\Desktop\\7.1~4zpdetailclick.txt').readlines()
#
uuidShown = {}
for u in yd:
    #dt,uuid_click,type,pos,tag = u.split('\t')
    click_at,uuid_click = u.split('\t')
    dt = click_at.split(' ')[0]
    #dt,click_at,uuid_click,t = u.split('\t')
    uuid_click = uuid_click[:-1]
    if uuid_click == "-":
        continue
    #uuidShown[dt[:-1].split(' ')[0] + "_" + uuid_click] = dt[:-1]
    uuidShown[dt + "_" + uuid_click] = click_at
print len(uuidShown)

with open("C:\\Users\\suchao\\Desktop\\7.1~4fangPV.txt",'r') as source:
    for userCase in source:
        try:
            access_at,cat,ca_source,ca_kw,refer,url,uuid,list_pv,search_pv,detail_pv,index_pv,pv = userCase.split('\t')
            if cat.find('list') == -1:
                continue
        except:
            continue
        try:
            #print uuidShown['2013-06-22    9210783060568053434949']
            click_at = uuidShown[access_at.split(' ')[0]+ '_' + uuid]
            key = click_at.split(' ')[0]
        except:
            #print uuid,"not exist"
            continue
        if click_at >= access_at:
            #print "click_at >= access_at"
            #print click_at,access_at
            continue
        try:
            UvPv[key]["uv"] = UvPv[key]["uv"] + 1
            UvPv[key]["pv"] = UvPv[key]["pv"] + int(pv[:-1])
        except:
            UvPv[key] = {}
            UvPv[key]["uv"] = 1
            UvPv[key]["pv"] = int(pv[:-1])

for cat in UvPv:
    #print UvPv[cat]["uv"],UvPv[cat]["pv"]
    #try:
    print str(cat)+'\t'+str(UvPv[cat]["uv"])+'\t'+str(UvPv[cat]["pv"])+'\t'+str(float(UvPv[cat]["pv"])/UvPv[cat]["uv"])
    tmp.write(str(cat)+'\t'+str(UvPv[cat]["uv"])+'\t'+str(UvPv[cat]["pv"])+'\t'+str(float(UvPv[cat]["pv"])/UvPv[cat]["uv"])+'\n')
    #except:
        #pass