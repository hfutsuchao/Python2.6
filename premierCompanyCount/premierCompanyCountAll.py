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
        
        if v.find('21') != -1:
            v = v.replace('21','二十一')
            print city,v
            dic[city][v] = {}
            dic[city][v]['ganji'] = 0
            dic[city][v]['wuba'] = 0
            dic[city][v]['company'] = v
            continue
        if v != '':
            print city,v
            dic[city][v] = {}
            dic[city][v]['ganji'] = 0
            dic[city][v]['wuba'] = 0
            dic[city][v]['company'] = vBackup
        
#sys.exit()
for data in dkData[1:]:
    
    arr = data.split('\t')
    city = arr[0]
    company = arr[1]
    if company.find('21') != -1:
        company = company.replace('21','二十一')
    ganjiCount = arr[4]
    wubaCount = arr[5]
    cat = arr[2]
    #print city, cat, company, ganjiCount, wubaCount
    
    try:
        for c in dic[city].keys():
            if company.find(c) != -1 or c.find(company) != -1:
                dic[city][c]['ganji'] = dic[city][c]['ganji'] + int(ganjiCount)
                dic[city][c]['wuba'] = dic[city][c]['wuba'] + int(wubaCount)
    except:
        pass

result = open('result.txt','w')

for city in dic:
    for company in dic[city]:
        result.write(city + '\t' + str(dic[city][company]['company']) + '\t' + company + '\t' + str(dic[city][company]['ganji']) + '\t' + str(dic[city][company]['wuba']) + '\n')
        