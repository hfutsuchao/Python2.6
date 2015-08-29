#coding: utf-8
#import os,MySQLdb,time
#conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="GBK")

#conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")

#citys = open('C:\\Users\\suchao\\Desktop\\360onebox\\360-city-rent.txt','r').readlines()
cityFile = open('C:\\Users\\suchao\\Desktop\\360onebox\\city-rent-2013-04-01.txt','r').readlines()
districtFile = open('C:\\Users\\suchao\\Desktop\\360onebox\\district-rent-2013-04-01.txt','r').readlines()
streetFile = open('C:\\Users\\suchao\\Desktop\\360onebox\\street-rent-2013-04-01.txt','r').readlines()

dibiaoFile = open('C:\\Users\\suchao\\Desktop\\360onebox\\dibiaoresult.txt','r').readlines()

dbs = {}
for i in dibiaoFile:
    db,hotDibiao = i.split('\t')
    dbs[db] = hotDibiao[:-1]

citys = {'bj':'北京','sh':'上海','nj':'南京','hz':'杭州','xa':'西安','gz':'广州','sz':'深圳','wh':'武汉','cd':'成都','cq':'重庆','tj':'天津','sy':'沈阳','cc':'长春','su':'苏州','dl':'大连'}

result = open('C:\\Users\\suchao\\Desktop\\360onebox\\rentNew.txt','w')

dic = {}

#城市相关
for i in cityFile:
    try:
        id,city,xiaoquName,districtName,streetName,number,oldSellPrice,sellPrice,wuyeType,houseType,subway,bus,null = i.split('\t')
        jiaotong = subway
        bus = '路,'.join(bus.split(','))
        bus = bus.split(',')
        bus.pop()
        bus = ','.join(bus)
        city = citys[city]
        #print len(i.split('\t'))
        if jiaotong == '':
            jiaotong = bus
        if sellPrice == '0':
            sellPrice =  oldSellPrice
        if sellPrice != '0':
            rentPrice3 = int(int(sellPrice)/4.5)
            rentPrice2 = int(int(rentPrice3)/1.3)
            rentPrice1 = int(int(rentPrice2)/1.3)
            #print xiaoquName,sellPrice,rentPrice3,rentPrice2,rentPrice1
            sellPrice = str(rentPrice1) + ',' + str(rentPrice2) + ',' + str(rentPrice3)
        else:
            sellPrice = '暂无数据'
    except:
        #print len(i.split('\t'))
        #print i,'error1'
        '''if len(i)>=5:
            print city'''
        continue
    print city
    if city in dic:
        if city in dic[city]:
            if city in dic[city][city]:
                dic[city][city][city] = dic[city][city][city] + '^^' + xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
            else:
                dic[city][city] = {}
                dic[city][city][city] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
        else:
            print 'error2'
    else:
        dic[city] = {}
        dic[city][city] = {}
        dic[city][city][city] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong

#区域相关

for i in districtFile:
    try:
        id,city,xiaoquName,districtName,streetName,number,oldSellPrice,sellPrice,wuyeType,houseType,subway,bus,null = i.split('\t')
        jiaotong = subway
        bus = '路,'.join(bus.split(','))
        bus = bus.split(',')
        bus.pop()
        bus = ','.join(bus)
        city = citys[city]
        if jiaotong == '':
            jiaotong = bus
        if sellPrice == '0':
            sellPrice =  oldSellPrice
        if sellPrice != '0':
            rentPrice3 = int(int(sellPrice)/4.5)
            rentPrice2 = int(int(rentPrice3)/1.3)
            rentPrice1 = int(int(rentPrice2)/1.3)
            #print xiaoquName,sellPrice,rentPrice3,rentPrice2,rentPrice1
            sellPrice = str(rentPrice1) + ',' + str(rentPrice2) + ',' + str(rentPrice3)
        else:
            sellPrice = '暂无数据'
    except:
        #print i,'error1'
        continue
    if city in dic:
        if districtName in dic[city]:
            dic[city][districtName][districtName] = dic[city][districtName][districtName] + '^^' + xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
        else:
            dic[city][districtName] = {}
            dic[city][districtName][districtName] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
    else:
        dic[city] = {}
        dic[city][districtName] = {}
        dic[city][districtName][districtName] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong

#街道相关

for i in streetFile:
    try:
        id,city,xiaoquName,districtName,streetName,number,oldSellPrice,sellPrice,wuyeType,houseType,subway,bus,null = i.split('\t')
        jiaotong = subway
        bus = '路,'.join(bus.split(','))
        bus = bus.split(',')
        bus.pop()
        bus = ','.join(bus)
        city = citys[city]
        if jiaotong == '':
            jiaotong = bus
        if sellPrice == '0':
            sellPrice =  oldSellPrice
        if sellPrice != '0':
            rentPrice3 = int(int(sellPrice)/4.5)
            rentPrice2 = int(int(rentPrice3)/1.3)
            rentPrice1 = int(int(rentPrice2)/1.3)
            #print xiaoquName,sellPrice,rentPrice3,rentPrice2,rentPrice1
            sellPrice = str(rentPrice1) + ',' + str(rentPrice2) + ',' + str(rentPrice3)
        else:
            sellPrice = '暂无数据'
    except:
        #print i,'error1'
        continue
    if city in dic:
        if districtName in dic[city]:
            if streetName in dic[city][districtName]:
                dic[city][districtName][streetName] = dic[city][districtName][streetName] + '^^' + xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
            else:
                dic[city][districtName][streetName] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong
        else:
            dic[city][districtName] = {}
            dic[city][districtName][streetName] = xiaoquName + '\t' + sellPrice + '\t' + houseType + '\t' + jiaotong

print len(dic)

for city in dic:
    for districtName in dic[city]:
        for streetName in dic[city][districtName]:
            if streetName != '其他':
                tmp = city + '_' + districtName + '_' + streetName
                try:
                    tmptmp = dbs[tmp]
                    result.write(city + '\t' + districtName + '\t' + streetName + '\t' + dbs[tmp] + '\t' + dic[city][districtName][streetName]+'\n')
                except:
                    print tmp
            else:
                print streetName
result.close()

'''
for i in cds:
    city_id,city,district_id,districtName,street_id,streetName = i.split('\t')
    streetName = streetName[:-1]
    for rent in rents:
        city_ids,district_ids,districtNames,street_ids,streetNames,xiaoqu_ids,xiaoquNames,huxing_shis,prices = rent.split('\t')
        prices = prices[:-1]
        #print city_id,city_ids,districtName,districtNames,streetName,streetName
        if (city_id == city_ids) and (districtName == districtNames) and (streetName == streetNames):
            if xiaoquNames not in dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames]:
                dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames] = {}
                dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['price'] = int(prices)
                dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['houses'] = 1
            else:
                dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['price'] = dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['price'] + int(prices)
                dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['houses'] = dic[str(city_ids)+'_'+str(districtNames)+'_'+streetNames][xiaoquNames]['houses'] + 1
for loc in dic.keys():
    #print loc,dic[loc]
    for xiaoqu in dic[loc].keys():
        #print xiaoqu,dic[loc]
        try:
            result.write(loc+'\t'+xiaoqu+'\t'+str(int(dic[loc][xiaoqu]['price'])/int(dic[loc][xiaoqu]['houses']))+'\t'+str(dic[loc][xiaoqu]['houses'])+'\n')
            #print loc+'\t'+xiaoqu+'\t'+str(int(dic[loc][xiaoqu]['price'])/int(dic[loc][xiaoqu]['houses']))+'\t'+str(dic[loc][xiaoqu]['houses'])+'\n'
        except:
            print loc,xiaoqu,dic[loc][xiaoqu]['houses']
'''
