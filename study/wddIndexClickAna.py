#coding:utf-8
rd = open('/Users/NealSu/Downloads/rd.txt','r').readlines()
#res = open('/Users/NealSu/Downloads/res.txt','w')

dic = {}

for line in rd:
    dt, uuid,  et = line.split('\t')
    et = et.replace('/main/index/','')
    
    evType = et.split('/')[0]

    if evType not in dic:
        dic[evType] = {}
        dic[evType]['show'] = {}
        dic[evType]['click'] = {}


    if et.find('show') != -1:
    	if dt not in dic[evType]['show']:
            dic[evType]['show'][dt] = {}
        if uuid not in dic[evType]['show'][dt]:
            dic[evType]['show'][dt][uuid] = []
        dic[evType]['show'][dt][uuid].append(et)
    else:
        if dt not in dic[evType]['show']:
            dic[evType]['show'][dt] = {}
        if uuid not in dic[evType]['show'][dt]:
            dic[evType]['show'][dt][uuid] = []
    	if dt not in dic[evType]['click']:
            dic[evType]['click'][dt] = {}
        if uuid not in dic[evType]['click'][dt]:
            dic[evType]['click'][dt][uuid] = []
        dic[evType]['click'][dt][uuid].append(et)
for evType in dic:
    for dt in dic[evType]['click']:
        try:
            print dt + '\t' + evType.replace('\n','') + '\t' + str(len(dic[evType]['click'][dt])) + '\t' + str(sum([len(dic[evType]['click'][dt][x]) for x in dic[evType]['click'][dt]]))
        except Exception,e:
            print e