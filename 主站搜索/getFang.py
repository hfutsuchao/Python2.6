# coding: utf-8
import os,MySQLdb,hashlib,json

dic = {}

dic['allkw'] = 0

tmp = open('fangkwinall.txt','w')

with open('C:\\Users\\sc\\Desktop\\zzkw.txt','r') as kws:
    for uc in kws:
        try:
            cat,kw,uv,v,pv = uc.split('\t')
        except Exception,e:
            print e
        if cat.find('fang') != -1:
            try:
                dic[kw] = dic[kw] + int(uv)
                dic['allkw'] = dic['allkw'] + int(uv)
            except:
                dic[kw] = int(uv)
                dic['allkw'] = dic['allkw'] + int(uv)
            kw = kw.decode('utf-8')
            if kw.find('出租') != -1:
                try:
                    dic['出租关键字'] = dic['出租关键字'] + int(uv)
                except:
                    dic['出租关键字'] = int(uv)
            if kw.find('转让') != -1:
                try:
                    dic['转让关键字'] = dic['转让关键字'] + int(uv)
                except:
                    dic['转让关键字'] = int(uv)
            if kw.find('出售') != -1:
                try:
                    dic['出售关键字'] = dic['出售关键字'] + int(uv)
                except:
                    dic['出售关键字'] = int(uv)
for k in sorted(dic.items(), key = lambda x:int(x[1]) ,reverse = True ):
    #print k
    tmp.write(k[0] + '\t' + str(k[1]) + '\n')