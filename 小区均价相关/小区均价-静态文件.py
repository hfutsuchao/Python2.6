#coding: gbk
import os,MySQLdb,time
#conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="GBK")

#conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")

cds = open('cds.txt','r').readlines()

rents = open('C:\\Users\\suchao\\Desktop\\rent.txt','r').readlines()

result = open('resultRent.txt','w')

dic = {}

for i in cds:
    city_id,city,district_id,disttrict_name,street_id,street_name = i.split('\t')
    street_name = street_name[:-1]
    dic[str(city_id)+'_'+str(disttrict_name)+'_'+street_name] = {}

for i in cds:
    city_id,city,district_id,disttrict_name,street_id,street_name = i.split('\t')
    street_name = street_name[:-1]
    for rent in rents:
        city_ids,district_ids,disttrict_names,street_ids,street_names,xiaoqu_ids,xiaoqu_names,huxing_shis,prices = rent.split('\t')
        prices = prices[:-1]
        #print city_id,city_ids,disttrict_name,disttrict_names,street_name,street_name
        if (city_id == city_ids) and (disttrict_name == disttrict_names) and (street_name == street_names):
            if xiaoqu_names not in dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names]:
                dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names] = {}
                dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['price'] = int(prices)
                dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['houses'] = 1
            else:
                dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['price'] = dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['price'] + int(prices)
                dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['houses'] = dic[str(city_ids)+'_'+str(disttrict_names)+'_'+street_names][xiaoqu_names]['houses'] + 1
for loc in dic.keys():
    #print loc,dic[loc]
    for xiaoqu in dic[loc].keys():
        #print xiaoqu,dic[loc]
        try:
            result.write(loc+'\t'+xiaoqu+'\t'+str(int(dic[loc][xiaoqu]['price'])/int(dic[loc][xiaoqu]['houses']))+'\t'+str(dic[loc][xiaoqu]['houses'])+'\n')
            #print loc+'\t'+xiaoqu+'\t'+str(int(dic[loc][xiaoqu]['price'])/int(dic[loc][xiaoqu]['houses']))+'\t'+str(dic[loc][xiaoqu]['houses'])+'\n'
        except:
            print loc,xiaoqu,dic[loc][xiaoqu]['houses']