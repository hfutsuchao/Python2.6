#coding:utf-8

import urllib
import sys

file2014 = open('2014Kresult.txt','r').readlines()
file2015 = open('2015Kresult.txt','r').readlines()
result = open('2015result.txt','w')

dic2014 = {}
dic2015 = {}
dic = {}

uvCount = 0
pvCount = 0
ec = 0
c = 0
pv2014 = 0
pv2015 = 0

#2014关键字去重汇总
for line in file2014:
    try:
        kw, pv = line.split('\t')
        if kw in dic2014:
            dic2014[kw] = dic2014[kw] + int(pv[:-1])
        else:
            dic2014[kw] = int(pv[:-1])
        pv2014 = pv2014 + int(pv[:-1])
    except:
        print line

#2015关键字去重汇总
for line in file2015:
    try:
        kw, pv = line.split('\t')
        if kw in dic2015:
            dic2015[kw] = dic2015[kw] + int(pv[:-1])
        else:
            dic2015[kw] = int(pv[:-1])
        pv2015 = pv2015 + int(pv[:-1])
    except:
        print line

print pv2014, pv2015

#计算二者之间的交集和差集
dif2015 = list(set(dic2015) - set(dic2014))
dif2014 = list(set(dic2014) - set(dic2015))
same = list(set(dic2014)&set(dic2015))

print '2015 and 2014:', len(dic2015), len(dic2014)
print 'same:',len(same), 'dif2014:', len(dif2014), 'dif2015:',len(dif2015)
citys = open('cdsx/city.txt','r').readlines()
districts = open('cdsx/district.txt','r').readlines()
streets = open('cdsx/street.txt','r').readlines()
xiaoqus = open('cdsx/xiaoqu.txt','r').readlines()

zufangKw = ['租房','出租']
dis = []
city = []
street = []
xiaoqu = []

for line in citys:
    dis.append(line[:-1])
for line in districts:
    city.append(line[:-1])
for line in streets:
    street.append(line[:-1])
for line in xiaoqus:
    xiaoqu.append(line[:-1])
'''
def dicGenerator(dim=[]):
    dic = {}
    dimLength = len(dim)
    if dimLength == 0:
        return dic
    else:
        for i in xrange(0,dimLength):
            pass
'''
dic = {}
kwType = ['same','dif']
years = [2014,2015]
statType = ['count','sum']
isBrand = ['isBrand', 'notBrand']

for y in years:
    dic[y] = {}
    for k in kwType:
        dic[y][k] = {}
        for b in isBrand:
            dic[y][k][b] = {}
            for t in statType:
                dic[y][k][b][t] = {}

count2014 = 0
count2015 = 0
sum2014 = 0
sum2015 = 0
c2014 = 0
c2015 = 0
s2014 = 0
s2015 = 0

#same KW 词类分布情况统计（分别修改city district street）

for kw in same:
    '''sum2014 = sum2014 + dic2014[kw]
    sum2015 = sum2015 + dic2015[kw]
    if kw.find('赶集') != -1:
        c2014 = c2014 + 1
        s2014 = s2014 + dic2014[kw]
        s2015 = s2015 + dic2015[kw]
        continue'''
    #result.write(kw + '\t' + str(dic2014[kw]) + '\n')
    #pass
    for k in zufangKw:
        for p in city:
            if kw.find(p) != -1 and kw.find(k) != -1:
                count2014 = count2014 + 1
                sum2014 = sum2014 + dic2014[kw]
                sum2015 = sum2015 + dic2015[kw]

#print sum2015,'isBrand(count 2014uv 2015uv)',c2014,s2014,s2015
print 'notBrand(count 2014uv 2015uv)',count2014,sum2014,sum2015
sys.exit()

#dif KW 词类分布情况统计

for kw in dif2015:
    #if kw.find('赶集') != -1:
    result.write(kw + '\t' + str(dic2015[kw]) + '\n')
    '''c2015 = c2015 + 1
    s2015 = s2015 + dic2015[kw]
    '''
    '''for k in zufangKw:
        for p in street:
            if kw.find(p) != -1 and kw.find(k) != -1:
                count2015 = count2015 + 1
                sum2015 = sum2015 + dic2015[kw]'''

print count2014,count2015
print sum2014,sum2015
#print c2014,s2014,c2015,s2015

'''for kw in dic:
    result.write(kw + '\t' + str(dic[kw]) + '\n')'''