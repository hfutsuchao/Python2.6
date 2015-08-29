#coding:gbk

dic = {}

with open('ds.txt','r') as dsFile:
    for details in dsFile:
        city, district, street = details.split('\t')
        #print city, district, street
        street = street[:-1]
        #print city, district, street
        if city in dic:
            if district in dic[city]:
                dic[city][district][street] = {}
                dic[city][district][street]['1'] = ''
                dic[city][district][street]['2'] = ''
                dic[city][district][street]['3'] = ''
                dic[city][district][street]['share'] = ''
            else:
                dic[city][district] = {}
                dic[city][district][street] = {}
                dic[city][district][street]['1'] = ''
                dic[city][district][street]['2'] = ''
                dic[city][district][street]['3'] = ''
                dic[city][district][street]['share'] = ''
                dic[city][district]['不限'] = {}
                dic[city][district]['不限']['1'] = ''
                dic[city][district]['不限']['2'] = ''
                dic[city][district]['不限']['3'] = ''
        else:
            dic[city] = {}
            dic[city][district] = {}
            dic[city][district][street] = {}
            dic[city][district][street]['1'] = ''
            dic[city][district][street]['2'] = ''
            dic[city][district][street]['3'] = ''
            dic[city][district][street]['share'] = ''
            
with open('rent.txt','r') as rentFile:
    for details in rentFile:
        try:
            city, district, street, huxing_shi, avgPrice, times = details.split('\t')
            
            if street == '其他' or district == '':
                #print city, district, street
                continue
            if street == '':
                street = '不限'
            dic[city][district][street][huxing_shi] = str(avgPrice) + '\t' + str(times)
        except Exception, e:
            #print e
            #print city, district, street
            pass
for city in dic:
    for district in dic[city]:
        for street in dic[city][district]:
            print city, district, street, dic[city][district][street]
