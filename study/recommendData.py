#coding:utf-8
rd = open('/Users/NealSu/Downloads/rd.txt','r').readlines()

res = open('/Users/NealSu/Downloads/res.txt','w')

dic = {}
dic['show'] = {}
dic['click'] = {}

for line in rd:
    dt, uuid,  et = line.split('\t')
    et = et.replace('/main/index/recommend/','')

    if et.find('show') != -1:
    	if dt not in dic['show']:
            dic['show'][dt] = {}
        if uuid not in dic['show'][dt]:
            dic['show'][dt][uuid] = []
        dic['show'][dt][uuid].append(et)

    if et.find('click') != -1:
    	if dt not in dic['click']:
            dic['click'][dt] = {}
        if uuid not in dic['click'][dt]:
            dic['click'][dt][uuid] = []
        dic['click'][dt][uuid].append(et)

for dt in dic['show']:
    print dt
    sumShowPV = sum([len(z) for z in [y for y in [dic['show'][dt][x] for x in dic['show'][dt]]]])
    sumClickPV = sum([len(dic['click'][dt][x]) for x in dic['click'][dt]])
    sumShowUV = len(dic['show'][dt])
    sumClickUV = len(dic['click'][dt])
    print '\t','PVshow','PVclick','UVshow','UVclick'
    print 'all', sumShowPV, sumClickPV, sumClickPV/(sumShowPV*100.0)*100.0, sumShowUV, sumClickUV, sumClickUV/(sumShowUV*100.0)*100.0

    sumBabyShowPV = 0
    sumBabyClickPV = 0
    sumBabyShowUV = []
    sumBabyClickUV = []
    for i in dic['show'][dt]:
        for k in dic['show'][dt][i]:
            if (k.find('undefined') == -1) and (k.find('show/0/') == -1):
                sumBabyShowPV = sumBabyShowPV + 1
                sumBabyShowUV.append(i)

    for i in dic['click'][dt]:
        for k in dic['click'][dt][i]:
            if (k.find('undefined') == -1) and (k.find('click/0/') == -1):
                sumBabyClickPV = sumBabyClickPV + 1
                sumBabyClickUV.append(i)

    print 'babyId', sumBabyShowPV, sumBabyClickPV, sumBabyClickPV/(sumBabyShowPV*100.0)*100.0, len(set(sumBabyShowUV)), len(set(sumBabyClickUV)), len(set(sumBabyClickUV))/(len(set(sumBabyShowUV))*100.0)*100.0

    sumBabyShowPV = sumShowPV - sumBabyShowPV
    sumBabyClickPV = sumClickPV - sumBabyClickPV
    sumBabyShowUV = len(dic['show'][dt]) - len(set(sumBabyShowUV))
    sumBabyClickUV = len(dic['click'][dt]) - len(set(sumBabyClickUV))

    print 'noBabyId', sumBabyShowPV, sumBabyClickPV, sumBabyClickPV/(sumBabyShowPV*100.0)*100.0, sumBabyShowUV, sumBabyClickUV, sumBabyClickUV/(sumBabyShowUV*100.0)*100.0