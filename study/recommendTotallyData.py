#coding:utf-8
rd = open('/Users/NealSu/Downloads/rd.txt','r').readlines()

res = open('/Users/NealSu/Downloads/res.txt','w')

dic = {}
dic['show'] = {}
dic['click'] = {}
'''dic['show']['uuid'] = []
dic['show']['babyId'] = []
dic['show']['pageId'] = []
dic['show']['toysId'] = []
dic['click']['uuid'] = []
dic['click']['babyId'] = []
dic['click']['pageId'] = []
dic['click']['pageInnerId'] = []
dic['click']['toysId'] = []
'''
for line in rd:
    dt, uuid,  et = line.split('\t')
    et = et.replace('/main/index/recommend/','')

    if et.find('show') != -1:
        if uuid not in dic['show']:
            dic['show'][uuid] = []
        '''dic['show']['uuid'].append(uuid)'''
        dic['show'][uuid].append(et)
        '''dic['show']['babyId'].append(et.split('/')[1])
        dic['show']['pageId'].append(et.split('/')[2])
        dic['show']['toysId'].append(et.split('/')[3])'''
    if et.find('click') != -1:
        if uuid not in dic['click']:
            dic['click'][uuid] = []
        dic['click'][uuid].append(et)
        '''dic['click']['babyId'].append(et.split('/')[1])
        dic['click']['pageId'].append(et.split('/')[2])
        dic['click']['pageInnerId'].append(et.split('/')[3])
        dic['click']['toysId'].append(et.split('/')[4])'''


sumShowPV = sum([len(dic['show'][x]) for x in dic['show']])
sumClickPV = sum([len(dic['click'][x]) for x in dic['click']])
sumShowUV = len(dic['show'])
sumClickUV = len(dic['click'])
print '\t','PVshow','PVclick','UVshow','UVclick'
print 'all', sumShowPV, sumClickPV, sumClickPV/(sumShowPV*100.0)*100.0, sumShowUV, sumClickUV, sumClickUV/(sumShowUV*100.0)*100.0

sumBabyShowPV = 0
sumBabyClickPV = 0
sumBabyShowUV = []
sumBabyClickUV = []
for i in dic['show']:
    for k in dic['show'][i]:
        if (k.find('undefined') == -1) and (k.find('show/0/') == -1):
            sumBabyShowPV = sumBabyShowPV + 1
            sumBabyShowUV.append(i)

for i in dic['click']:
    for k in dic['click'][i]:
        if (k.find('undefined') == -1) and (k.find('click/0/') == -1):
            sumBabyClickPV = sumBabyClickPV + 1
            sumBabyClickUV.append(i)

print 'babyId', sumBabyShowPV, sumBabyClickPV, sumBabyClickPV/(sumBabyShowPV*100.0)*100.0, len(set(sumBabyShowUV)), len(set(sumBabyClickUV)), len(set(sumBabyClickUV))/(len(set(sumBabyShowUV))*100.0)*100.0

sumBabyShowPV = sum([len(dic['show'][x]) for x in dic['show']]) - sumBabyShowPV
sumBabyClickPV = sum([len(dic['click'][x]) for x in dic['click']]) - sumBabyClickPV
sumBabyShowUV = len(dic['show']) - len(set(sumBabyShowUV))
sumBabyClickUV = len(dic['click']) - len(set(sumBabyClickUV))

print 'noBabyId', sumBabyShowPV, sumBabyClickPV, sumBabyClickPV/(sumBabyShowPV*100.0)*100.0, sumBabyShowUV, sumBabyClickUV, sumBabyClickUV/(sumBabyShowUV*100.0)*100.0