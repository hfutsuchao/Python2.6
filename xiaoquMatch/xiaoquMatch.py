#coding: utf-8

dicXiaoqu = {}

dicHL = {}

xiaoquKws = open('bjxq.txt','r').readlines()

homelinks = open('homelink.txt','r').readlines()

for line in homelinks:
    city, id, xiaoqu = line.split('\t')
    xiaoqu = xiaoqu[:-1]
    if city in dicHL:
        if xiaoqu not in dicHL[city]:
            dicHL[city][xiaoqu] = id
    else:
        dicHL[city] = {}
        dicHL[city][xiaoqu] = id

for line in xiaoquKws:
    city, id, xiaoqu = line.split('\t')
    xiaoqu = xiaoqu[:-1]
    if city in dicXiaoqu:
        if xiaoqu not in dicXiaoqu[city]:
            dicXiaoqu[city][xiaoqu] = id
    else:
        dicXiaoqu[city] = {}
        dicXiaoqu[city][xiaoqu] = id


tmp = open('tmp.txt','w')

for city in dicHL:
    if city in dicXiaoqu:
        for xiaoqu in dicHL[city]:
            for xq in dicXiaoqu[city]:
                #if xiaoqu.find(xq) != -1:
                if (xiaoqu != xq) and (xiaoqu.find(xq) != -1) and (len(xq)/float(len(xiaoqu)) >= 0.6 ):
                    tmp.write(xiaoqu + '\t' + xq + '\t' + dicXiaoqu[city][xq] + '\n')
                    break

'''
for city in dicHL:
    if city in dicXiaoqu:
        for xq in dicHL[city]:
            for xiaoqu in dicXiaoqu[city]:
                #if xiaoqu.find(xq) != -1:
                if (xiaoqu != xq) and (xiaoqu.find(xq) != -1) and (len(xiaoqu)/float(len(xq)) >= 0.6 ):
                    tmp.write(xq + '\t' + xiaoqu + '\t' + dicXiaoqu[city][xiaoqu] + '\n')
                    break
'''