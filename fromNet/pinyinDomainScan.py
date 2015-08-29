#coding:utf-8 
from yuming import ifRegged
import sys
import time,random

dicType = []
dic = {}

dtFile = open('domainType','r').readlines()
for t in dtFile[1:-1]:
    dicType.append(t[:-1])

#print dicType

times = [1,2,3,4]
for t in times:
    dic[t] = []

totalDic = []

pinyinFile = open('pinyin','r').readlines()
for py in pinyinFile[1:-1]:
    py = py[:-2]
    dic[1].append(py) 
    totalDic.append(py) 
    for py2 in pinyinFile:
        py2 = py2[:-2]
        dic[2].append(py+py2)
        totalDic.append(py+py2)
'''        for py3 in pinyinFile:
            py3 = py3[:-1]
            dic[3].append(py+py2+py3)
            for py4 in pinyinFile:
                py4 = py4[:-1]
                dic[4].append(py+py2+py3+py4)
'''

result = open('unRegged','a')

'''
print dicType[:10]
sys.exit()
'''

for dm in totalDic: 
    for dtype in dicType[:13]:
        domainName = dm + dtype
        try:
            regResult = ifRegged(domainName)
        except Exception,e:
            print domainName,e
            continue
        if regResult==1:
            print domainName + ' unRegged!'
            result.write(domainName + '\t' + 'unRegged!' + '\n') 
        time.sleep(random.random()*1)
    result.close()
    time.sleep(3)
    result = open('unRegged','a')
