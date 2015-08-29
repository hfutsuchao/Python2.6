#coding:gbk
import random
cds = open('xqhx.txt','r').readlines()

dic={}

for c in cds:
    #print c
    xiaoquName,huxing_shi = c.split('\t')
    #cityName,districtName,streetName = c.split('\t')
    huxing_shi=huxing_shi[:-1]
    if xiaoquName in dic:
        dic[xiaoquName][huxing_shi] = ""
    else:
        dic[xiaoquName] = {}
        dic[xiaoquName][huxing_shi] = ""

for xiaoquName in dic:
    shi = ""
    for i in sorted(dic[xiaoquName].iteritems(), key = lambda k:int(k[0]),reverse = False):
        shi = shi + i[0] + "," 
        if len(shi) >= 6:
            shi = shi + "多"
            break
    print xiaoquName+"\t"+shi