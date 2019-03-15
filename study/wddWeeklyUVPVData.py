#coding:utf-8
rd = open('/Users/NealSu/Downloads/rd.txt','r').readlines()

res = open('/Users/NealSu/Downloads/res.txt','w')
resh = open('/Users/NealSu/Downloads/resh.txt','w')

dic = {}

for line in rd:
    dt, pt, uuid = line.split('\t')
    pt = pt.split('@')[0]
    if dt not in dic:
        dic[dt] = {}
    if pt not in dic[dt]:
        dic[dt][pt] = []
    dic[dt][pt].append(uuid)

for dt in dic:
    for pt in dic[dt]:
        if pt.find('http') != -1:
            sumClickPV = len(dic[dt][pt])
            sumClickUV = len(set(dic[dt][pt]))
            resh.write(dt + '\t' + pt + '\t' + str(sumClickUV) + '\t' + str(sumClickPV) + '\n')
        else:
            sumClickPV = len(dic[dt][pt])
            sumClickUV = len(set(dic[dt][pt]))
            res.write(dt + '\t' + pt + '\t' + str(sumClickUV) + '\t' + str(sumClickPV) + '\n')