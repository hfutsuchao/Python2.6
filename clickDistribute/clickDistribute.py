#coding:utf-8

fang1 = open('data/fang1.txt','r').readlines()
fang5 = open('data/fang5.txt','r').readlines()
fang6 = open('data/fang6.txt','r').readlines()
fang8 = open('data/fang8.txt','r').readlines()

citys = open('citys.txt','r').readlines()

dicCitys = {}

for city in citys:
    domain, name = city.split('\t')
    dicCitys[domain] = name[:-1]

cats = ['fang1', 'fang5', 'fang6', 'fang8']

dnys = locals()

dic = {}

for cat in cats:
    dic[cat] = {}
    dnys[cat + 'result'] = open( cat + '.txt','w')

for line in fang1:
    dt, city, uv, pv, dv, freeGeren, freeAgent, topGeren, topAgent, freePremier, premier, ppd, fangxin = line.split('\t')
    if city in dic['fang1']:
        dic['fang1'][city]['uv'] = dic['fang1'][city]['uv'] + int(uv)
        dic['fang1'][city]['pv'] = dic['fang1'][city]['pv'] + int(pv)
        dic['fang1'][city]['freeGeren'] = dic['fang1'][city]['freeGeren'] + int(freeGeren)
        dic['fang1'][city]['freeAgent'] = dic['fang1'][city]['freeAgent'] + int(freeAgent)
        dic['fang1'][city]['topGeren'] = dic['fang1'][city]['topGeren'] + int(topGeren)
        dic['fang1'][city]['topAgent'] = dic['fang1'][city]['topAgent'] + int(topAgent)
        dic['fang1'][city]['freePremier'] = dic['fang1'][city]['freePremier'] + int(freePremier)
        dic['fang1'][city]['premier'] = dic['fang1'][city]['premier'] + int(premier)
        dic['fang1'][city]['ppd'] = dic['fang1'][city]['ppd'] + int(ppd)
        dic['fang1'][city]['fangxin'] = dic['fang1'][city]['fangxin'] + int(fangxin)

    else:
        dic['fang1'][city] = {}
        dic['fang1'][city]['uv'] = int(uv)
        dic['fang1'][city]['pv'] = int(pv)
        dic['fang1'][city]['freeGeren'] = int(freeGeren)
        dic['fang1'][city]['freeAgent'] = int(freeAgent)
        dic['fang1'][city]['topGeren'] = int(topGeren)
        dic['fang1'][city]['topAgent'] = int(topAgent)
        dic['fang1'][city]['freePremier'] = int(freePremier)
        dic['fang1'][city]['premier'] = int(premier)
        dic['fang1'][city]['ppd'] = int(ppd)
        dic['fang1'][city]['fangxin'] = int(fangxin)

for line in fang5:
    dt, city, uv, pv, dv, freeGeren, freeAgent, topGeren, topAgent, freePremier, premier, ppd, fangxin = line.split('\t')
    if city in dic['fang5']:
        dic['fang5'][city]['uv'] = dic['fang5'][city]['uv'] + int(uv)
        dic['fang5'][city]['pv'] = dic['fang5'][city]['pv'] + int(pv)
        dic['fang5'][city]['freeGeren'] = dic['fang5'][city]['freeGeren'] + int(freeGeren)
        dic['fang5'][city]['freeAgent'] = dic['fang5'][city]['freeAgent'] + int(freeAgent)
        dic['fang5'][city]['topGeren'] = dic['fang5'][city]['topGeren'] + int(topGeren)
        dic['fang5'][city]['topAgent'] = dic['fang5'][city]['topAgent'] + int(topAgent)
        dic['fang5'][city]['freePremier'] = dic['fang5'][city]['freePremier'] + int(freePremier)
        dic['fang5'][city]['premier'] = dic['fang5'][city]['premier'] + int(premier)
        dic['fang5'][city]['ppd'] = dic['fang5'][city]['ppd'] + int(ppd)
        dic['fang5'][city]['fangxin'] = dic['fang5'][city]['fangxin'] + int(fangxin)

    else:
        dic['fang5'][city] = {}
        dic['fang5'][city]['uv'] = int(uv)
        dic['fang5'][city]['pv'] = int(pv)
        dic['fang5'][city]['freeGeren'] = int(freeGeren)
        dic['fang5'][city]['freeAgent'] = int(freeAgent)
        dic['fang5'][city]['topGeren'] = int(topGeren)
        dic['fang5'][city]['topAgent'] = int(topAgent)
        dic['fang5'][city]['freePremier'] = int(freePremier)
        dic['fang5'][city]['premier'] = int(premier)
        dic['fang5'][city]['ppd'] = int(ppd)
        dic['fang5'][city]['fangxin'] = int(fangxin)

for line in fang6:
    dt, city, uv, pv, dv, freeGeren, freeAgent, topGeren, topAgent, freePremier, premier, ppd, fangxin = line.split('\t')
    if city in dic['fang6']:
        
        if city == 'bj.ganji.com':
            print dic['fang6'][city]['pv'], dic['fang6'][city]['freeGeren'], pv, freeGeren
        
        dic['fang6'][city]['uv'] = dic['fang6'][city]['uv'] + int(uv)
        dic['fang6'][city]['pv'] = dic['fang6'][city]['pv'] + int(pv)
        dic['fang6'][city]['freeGeren'] = dic['fang6'][city]['freeGeren'] + int(freeGeren)
        dic['fang6'][city]['freeAgent'] = dic['fang6'][city]['freeAgent'] + int(freeAgent)
        dic['fang6'][city]['topGeren'] = dic['fang6'][city]['topGeren'] + int(topGeren)
        dic['fang6'][city]['topAgent'] = dic['fang6'][city]['topAgent'] + int(topAgent)
        dic['fang6'][city]['freePremier'] = dic['fang6'][city]['freePremier'] + int(freePremier)
        dic['fang6'][city]['premier'] = dic['fang6'][city]['premier'] + int(premier)
        dic['fang6'][city]['ppd'] = dic['fang6'][city]['ppd'] + int(ppd)
        dic['fang6'][city]['fangxin'] = dic['fang6'][city]['fangxin'] + int(fangxin)
        if city == 'bj.ganji.com':
            print dic['fang6'][city]['pv'], dic['fang6'][city]['freeGeren']

    else:
        dic['fang6'][city] = {}
        dic['fang6'][city]['uv'] = int(uv)
        dic['fang6'][city]['pv'] = int(pv)
        dic['fang6'][city]['freeGeren'] = int(freeGeren)
        dic['fang6'][city]['freeAgent'] = int(freeAgent)
        dic['fang6'][city]['topGeren'] = int(topGeren)
        dic['fang6'][city]['topAgent'] = int(topAgent)
        dic['fang6'][city]['freePremier'] = int(freePremier)
        dic['fang6'][city]['premier'] = int(premier)
        dic['fang6'][city]['ppd'] = int(ppd)
        dic['fang6'][city]['fangxin'] = int(fangxin)

for line in fang8:
    dt, city, uv, pv, dv, freeGeren, freeAgent, topGeren, topAgent, freePremier, premier, ppd, fangxin = line.split('\t')
    if city in dic['fang8']:
        dic['fang8'][city]['uv'] = dic['fang8'][city]['uv'] + int(uv)
        dic['fang8'][city]['pv'] = dic['fang8'][city]['pv'] + int(pv)
        dic['fang8'][city]['freeGeren'] = dic['fang8'][city]['freeGeren'] + int(freeGeren)
        dic['fang8'][city]['freeAgent'] = dic['fang8'][city]['freeAgent'] + int(freeAgent)
        dic['fang8'][city]['topGeren'] = dic['fang8'][city]['topGeren'] + int(topGeren)
        dic['fang8'][city]['topAgent'] = dic['fang8'][city]['topAgent'] + int(topAgent)
        dic['fang8'][city]['freePremier'] = dic['fang8'][city]['freePremier'] + int(freePremier)
        dic['fang8'][city]['premier'] = dic['fang8'][city]['premier'] + int(premier)
        dic['fang8'][city]['ppd'] = dic['fang8'][city]['ppd'] + int(ppd)
        dic['fang8'][city]['fangxin'] = dic['fang8'][city]['fangxin'] + int(fangxin)

    else:
        dic['fang8'][city] = {}
        dic['fang8'][city]['uv'] = int(uv)
        dic['fang8'][city]['pv'] = int(pv)
        dic['fang8'][city]['freeGeren'] = int(freeGeren)
        dic['fang8'][city]['freeAgent'] = int(freeAgent)
        dic['fang8'][city]['topGeren'] = int(topGeren)
        dic['fang8'][city]['topAgent'] = int(topAgent)
        dic['fang8'][city]['freePremier'] = int(freePremier)
        dic['fang8'][city]['premier'] = int(premier)
        dic['fang8'][city]['ppd'] = int(ppd)
        dic['fang8'][city]['fangxin'] = int(fangxin)

for cat in dic:
    for city in dic[cat]:
        dv = int(float(dic[cat][city]['pv'])/dic[cat][city]['uv']*100)/100.0
        days = 31
        #print cat, city, dic[cat][city]['freeGeren'], dic[cat][city]['freeAgent'], dic[cat][city]['topGeren'], dic[cat][city]['topAgent'], dic[cat][city]['freePremier'], dic[cat][city]['premier'], dic[cat][city]['ppd'], dic[cat][city]['fangxin']
        try:
            dnys[cat + 'result'].write(str(dicCitys[city]) + '\t' + str(dic[cat][city]['uv']/days) + '\t' + str(dic[cat][city]['pv']/days) + '\t' + str(dv) + '\t' + str(dic[cat][city]['freeGeren']/days) + '\t' + str(dic[cat][city]['freeAgent']/days) + '\t' + str(dic[cat][city]['topGeren']/days) + '\t' + str(dic[cat][city]['topAgent']/days) + '\t' + str(dic[cat][city]['freePremier']/days) + '\t' + str(dic[cat][city]['premier']/days) + '\t' + str(dic[cat][city]['ppd']/days) + '\t' + str(dic[cat][city]['fangxin']/days) + '\n')
        except:
            #print str(city) + '\t' + str(dic[cat][city]['uv']) + '\t' + str(dic[cat][city]['pv']) + '\t' + str(dic[cat][city]['freeGeren']) + '\t' + str(dic[cat][city]['freeAgent']) + '\t' + str(dic[cat][city]['topGeren']) + '\t' + str(dic[cat][city]['topAgent']) + '\t' + str(dic[cat][city]['freePremier']) + '\t' + str(dic[cat][city]['premier']) + '\t' + str(dic[cat][city]['ppd']) + '\t' + str(dic[cat][city]['fangxin'])
            #dnys[cat + 'result'].write(str(city) + '\t' + str(dic[cat][city]['uv']/days) + '\t' + str(dic[cat][city]['pv']/days) + '\t' + str(dv) + '\t' + str(dic[cat][city]['freeGeren']/days) + '\t' + str(dic[cat][city]['freeAgent']/days) + '\t' + str(dic[cat][city]['topGeren']/days) + '\t' + str(dic[cat][city]['topAgent']/days) + '\t' + str(dic[cat][city]['freePremier']/days) + '\t' + str(dic[cat][city]['premier']/days) + '\t' + str(dic[cat][city]['ppd']/days) + '\t' + str(dic[cat][city]['fangxin']/days) + '\n')
            pass