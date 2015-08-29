#coding:utf-8

import urllib

file = open('2015kw.txt','r').readlines()
result = open('2015Kresult.txt','w')

dic = {}
uvCount = 0
pvCount = 0
ec = 0
c = 0

for line in file:
    c=c+1
    try:
        kw, uv, pv = line.split('\t')
        if kw in dic:
            dic[kw] = dic[kw] + int(pv[:-1])
        else:
            dic[kw] = int(pv[:-1])
        uvCount = uvCount + 1
        pvCount = pvCount + 1
    except:
        ec = ec + 1
        print line
        continue

print uvCount, pvCount,ec,c

for kw in dic:
    result.write(kw + '\t' + str(dic[kw]) + '\n')
