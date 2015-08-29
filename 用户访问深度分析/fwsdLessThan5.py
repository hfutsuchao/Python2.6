# coding: gbk
import os,MySQLdb,hashlib
from urllib import unquote

tmp = open('tmp_fwsdLess.txt','w')

cats = ['fang1/','fang3/','fang5/','fang6/','fang7/','fang8/','fang9/','fang10/','fang11/','fang12/','fang2/','fang4/']

'''def hex2dec(string_num):
    return str(int(string_num.upper(), 16))'''

UvPv = {}

count = 0

sum = 0

with open("F:/chromeDownload/fwjl.txt",'r') as source:
    for userCase in source:
        sum = sum + 1
        try:
            uuid,access_at,cat,ca_source,ca_kw,refer,url = userCase.split('\t')
            
            if uuid in UvPv:
                UvPv[uuid]['pv'] = UvPv[uuid]['pv'] + 1
                UvPv[uuid]['url'][access_at] = url
            else:
                UvPv[uuid] = {}
                UvPv[uuid]['pv'] = 1
                UvPv[uuid]['url'] = {}
                UvPv[uuid]['url'][access_at] = ca_source + ' | ' + unquote(ca_kw) + ' | ' + unquote(url)
        except Exception,e:
            print e
            pass

'''for uuid in UvPv:
    for i in sorted(UvPv[uuid]['url'].items(),key=lambda e:e[0],reverse=True):
        UvPv[uuid]['last'] = i
        break
'''
for uuid in UvPv:
    if UvPv[uuid]['pv'] <=1:
        try:
            tmp.write(str(uuid) + '\t' + str(UvPv[uuid]["pv"]))
            for i in sorted(UvPv[uuid]['url'].items(),key=lambda e:e[0],reverse=False):
                tmp.write('\t' + i[0] + ' | ' + str(i[1][:-1]))
            tmp.write('\n')
        except:
            pass
