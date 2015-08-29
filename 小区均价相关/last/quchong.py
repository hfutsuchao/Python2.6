#coding:gbk
import random
xiaoquIn58 = open('all.txt','r').readlines()
cds = open('cds.txt','r').readlines()

ganjixiaoqu = open("xqpinyin.txt",'r').readlines()

dic={}

xqpy = {}

for py in ganjixiaoqu:
    try:
        domain,city,d,s,name,pinyin = py.split('\t')
    except:
        print py
    if city in xqpy:
        xqpy[city][name] = domain+"\t"+pinyin[:-1]
        
    else:
        xqpy[city] = {}
        xqpy[city][name] = domain+"\t"+pinyin[:-1]
for c in cds:
    cityId,cityName,districtId,districtName,streetId,streetName = c.split('\t')
    cityName = cityName[:4]
    streetName = streetName[:-1]
    if cityName in dic:
        if districtName in dic[cityName]:
            if streetName in dic[cityName][districtName]:
                pass
            else:
                dic[cityName][districtName][streetName]={}
        else:
            dic[cityName][districtName]={}
    else:
        dic[cityName]={}

for xiaoqu in xiaoquIn58:
    try:
        #city,district,street,xiaoqu_name,rent1,rent2,rent3,avgShare,year,buildingType,subway = xiaoqu.split('\t')
        city,district,street,xiaoqu_name,rent1,year,buildingType,subway = xiaoqu.split('\t')
    except:
        print xiaoqu
    subway = subway[:-1]
    try:
        if xiaoqu_name in dic[city][district][street]:
            print "小区重复",xiaoqu[:-1]
            #dic[city][district][street][xiaoqu_name] = rent1 + ',' + rent2 + ',' + rent3 + ',' + avgShare + ',' + year + ',' + buildingType + ',' + subway
        else:
            #dic[city][district][street][xiaoqu_name] = rent1 + ',' + rent2 + ',' + rent3 + ',' + avgShare + ',' + year + ',' + buildingType + ',' + subway
            dic[city][district][street][xiaoqu_name] = rent1 + ',' + year + ',' + buildingType + ',' + subway
    except:
        #print 'error',xiaoqu[:-1]
        pass
    #print xiaoqu[:-1]
    #print city,district,street,xiaoqu_name,year,buildingType,subway,sellAvg,sellCount,rent1,rent2,rent3,renCount

result = open("jieguo3.txt",'w')
for city in dic:
    for district in dic[city]:
        for street in dic[city][district]:
            x = 1
            for xiaoqu_name in dic[city][district][street].keys():
                #print xiaoqu_name,xqpy[city][xiaoqu_name]
                if xiaoqu_name in xqpy[city]:
                    domain = xqpy[city][xiaoqu_name].split("\t")[0]
                    pinyin = xqpy[city][xiaoqu_name].split("\t")[1]
                    #result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name] + ',' + "http://"+domain+".ganji.com/xiaoqu/"+pinyin+"/chuzufang/"+'\n')
                    result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name] + ',' + "http://"+domain+".ganji.com/xiaoqu/"+pinyin+"/ershoufang/"+'\n')
                    x= x + 1
                    if x>=6:
                        break