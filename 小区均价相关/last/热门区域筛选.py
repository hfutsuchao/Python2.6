#coding:gbk
import random
#xiaoquIn58 = open('jiedao.txt','r').readlines()
cds = open('jiedao.txt','r').readlines()

dic={}

for c in cds:
    #print c
    cityName,districtName,streetName,count = c.split('\t')
    #cityName,districtName,streetName = c.split('\t')
    count = count[:-1]
    if cityName in dic:
        if districtName in dic[cityName]:
            if streetName in dic[cityName][districtName]:
                pass
            else:
                dic[cityName][districtName][streetName] = count
        else:
            dic[cityName][districtName]={}
            dic[cityName][districtName][streetName] = count
    else:
        dic[cityName]={}
        dic[cityName][districtName] = {}
        dic[cityName][districtName][streetName] = count

for city in dic:
    for district in dic[city]:
        x = 1
        for i in sorted(dic[city][district].iteritems(), key = lambda asd:int(str(asd[1])),reverse = True):
            if i[0] == "" or i[0] == "其他" :
                continue
            if "remen" in dic[city][district]:
                dic[city][district]["remen"] = str(dic[city][district]["remen"]) + "," + i[0]
            else:
                dic[city][district]["remen"] = i[0]
            #print city,district,i[0],i[1]
            x = x + 1
            if x >= 7:
                break
            #result.write(city+","+district+","+street+","+str(i)+"\n")
for city in dic:
    for district in dic[city]:
        if "remen" in dic[city][district]:
            print city,district,dic[city][district]["remen"]