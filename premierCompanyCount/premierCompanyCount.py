#coding:utf-8
import sys
dkData = open('dk.txt','r').readlines()

cc = open('cc.txt','r').readlines()

keywords = ['房地产','房屋','地产','房产','经纪','有限','公司','有限','代理','中介','市','不动产','物业','顾问','置换','服务','（新环境）','销售','（）','咨询','连锁','集团']

dic = {}

for line in cc[1:]:
    city, c1, c2, c3 = line.split('\t')
    
    #print c3
    
    dic[city] = {}
    
    tmp = [c1, c2, c3[:-1]]
    
    for v in tmp:
        vBackup = v
        if v.find(city) != -1:
            #print v
            v = v.replace(city,'')
            #print v
        for kw in keywords:
            if v.find(kw) != -1:
                #print v
                v = v.replace(kw,'')
        #print v
        
        if v != '':
            if v != '111':
                print city,v
            dic[city][v] = {}
            dic[city][v]['ganji'] = {}
            dic[city][v]['wuba'] = {}
            dic[city][v]['ganji']['租房'] = 0
            dic[city][v]['ganji']['二手房'] = 0
            dic[city][v]['ganji']['全部'] = 0
            dic[city][v]['wuba']['二手房'] = 0
            dic[city][v]['wuba']['租房'] = 0
            dic[city][v]['wuba']['全部'] = 0
            dic[city][v]['company'] = vBackup
            
        if v.find('二十一') != -1:
            v = v.replace('二十一','21')
            if v != '111':
                print city,v
            dic[city][v] = {}
            dic[city][v]['ganji'] = {}
            dic[city][v]['wuba'] = {}
            dic[city][v]['ganji']['租房'] = 0
            dic[city][v]['ganji']['二手房'] = 0
            dic[city][v]['ganji']['全部'] = 0
            dic[city][v]['wuba']['二手房'] = 0
            dic[city][v]['wuba']['租房'] = 0
            dic[city][v]['wuba']['全部'] = 0
            dic[city][v]['company'] = vBackup
sys.exit()
for data in dkData[1:]:
    arr = data.split('\t')
    city = arr[0]
    company = arr[1]
    ganjiCount = arr[4]
    wubaCount = arr[5]
    cat = arr[2]
    #print city, cat, company, ganjiCount, wubaCount
    
    try:
        for c in dic[city].keys():
            if company.find(c) != -1:
                dic[city][c]['ganji'][cat] = dic[city][c]['ganji'][cat] + int(ganjiCount)
                dic[city][c]['wuba'][cat] = dic[city][c]['wuba'][cat] + int(wubaCount)
    except:
        pass

for city in dic:
    for company in dic[city]:
        print city, dic[city][company]['company'], company, dic[city][company]['ganji']['二手房'], dic[city][company]['wuba']['二手房']
        