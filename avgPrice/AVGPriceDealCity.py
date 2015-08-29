#coding:gbk

dic = {}

with open('ds.txt','r') as dsFile:
    for details in dsFile:
        city, district, street = details.split('\t')
        #print city, district, street
        street = street[:-1]
        #print city, district, street
        if city not in dic:
            dic[city] = {}
            dic[city]['1'] = ''
            dic[city]['2'] = ''
            dic[city]['3'] = ''
            dic[city]['share'] = ''
            
with open('rent.txt','r') as rentFile:
    for details in rentFile:
        try:
            city, huxing_shi, avgPrice, times = details.split('\t')
            
            dic[city][huxing_shi] = str(avgPrice) + '\t' + str(times)
        except Exception, e:
            #print e
            #print city, district, street
            pass
for city in dic:
    print city, dic[city]
    