#coding:utf-8

import urllib

file = open('C:/Users/suchao/Desktop/kws.txt','r').readlines()
result = open('Kresult.txt','w')

dic = {}

for line in file:
    try:
        dt, city, cat, kw, uv, v, pv = line.split('\t')
        if city in dic:
            if cat in dic[city]:
                if kw not in dic[city][cat]:
                    dic[city][cat][kw] = int(uv)
                else:
                    dic[city][cat][kw] = dic[city][cat][kw] + int(uv)
            else:
                dic[city][cat] = {}
                dic[city][cat][kw] = int(uv)
        else:
            dic[city] = {}
            dic[city][cat] = {}
            dic[city][cat][kw] = int(uv)
    except:
        print line

for city in dic:
    for cat in dic[city]:
        for kw in dic[city][cat]:
            if dic[city][cat][kw] >= 3 and (cat == '/fang/fang1/search' or cat == '/fang/fang3/search'):
                result.write(city + '\t' + cat + '\t' + kw + '\t' + str(dic[city][cat][kw]) + '\n')