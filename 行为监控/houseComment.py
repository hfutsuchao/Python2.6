#coding:utf-8
import sys

try:
    houseUrl = sys.argv[1]
except:
    houseUrl = 'http://qd.ganji.com/fang1/751337937x.htm'
dic = {}

with open('F:/kuaipan/MyTools/Python2.6/uvMonitor/data/house.txt','r') as tmpFile:
    for line in tmpFile:
        dt, uuid, url = line.split('\t')
        url = url[:-1].split('?')[0]
        if url == houseUrl:
            if uuid not in dic:
                dic[uuid] = {}
                dic[uuid]['time'] = dt
                dic[uuid]['urlsLater'] = []

with open('F:/kuaipan/MyTools/Python2.6/uvMonitor/data/house.txt','r') as tmpFile:
    for line in tmpFile:
        dt, uuid, url = line.split('\t')
        url = url[:-1].split('?')[0]
        if uuid in dic:
            if dt >= dic[uuid]['time']:
                dic[uuid]['urlsLater'].append(url)

urlDic = {}
for uuid in dic:
    for url in dic[uuid]['urlsLater']:
        if url in urlDic:
            urlDic[url] = urlDic[url] + 1
        else:
            urlDic[url] = 1

for i in sorted(urlDic.items(), key=lambda e:e[1], reverse=True)[:9]:
    print i[0],i[1]