#coding: gbk
import os
import random

setDic = {}
ruleDic = {}

result = open('result.txt','w')

with open('set.txt') as set:
    for s in set:
        key,value = s.split('\t')
        setDic[key] = value

with open('rule.txt') as rule:
    for r in rule:
        key,value = r.split('\t')
        ruleDic[key] = value

dic = {}

for keyR in ruleDic:
    keyRs = keyR.split(',')
    length = len(keyRs)
    dic[keyR] = {}
    for loop in range(0,20):
        dic[keyR][loop] = ''
        for i in range(0,length):
            lenSet = len(setDic[keyRs[i]][:-1].split(','))
            dic[keyR][loop] = dic[keyR][loop] + setDic[keyRs[i]][:-1].split(',')[random.randint(0,lenSet-1)].split('|')[0]
try:
    for i in dic:
        for j in dic[i]:
            print dic[i][j],i
except:
    pass

#result.write(setValue1.split('|')[0] + '+' + setValue2.split('|')[0] + '\t' + ruleDic[keyR])
''' 
    if len(keyRs) == 1:
        for setValue in setDic[keyRs[0]][:-1].split(','):
            result.write(setValue.split('|')[0] + '\t' + ruleDic[keyR])
    elif len(keyRs) == 2:
        for setValue1 in setDic[keyRs[0]][:-1].split(','):
            for setValue2 in setDic[keyRs[1]][:-1].split(','):
                result.write(setValue1.split('|')[0] + '+' + setValue2.split('|')[0] + '\t' + ruleDic[keyR])
'''