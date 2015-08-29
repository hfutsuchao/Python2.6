#coding: utf-8

dicXiaoqu = {}

xiaoquKws = open('xiaoquKws.txt','r').readlines()

with open('xiaoquNames.txt','r') as xiaoquNames:
    for line in xiaoquNames:
        city, xiaoqu = line.split('\t')
        xiaoqu = xiaoqu[:-1]
        if city in dicXiaoqu:
            if xiaoqu not in dicXiaoqu[city]:
                dicXiaoqu[city][xiaoqu] = ''
        else:
            dicXiaoqu[city] = {}
            dicXiaoqu[city][xiaoqu] = ''
            dicXiaoqu[city]['sumUV'] = 0
            dicXiaoqu[city]['sumPV'] = 0
            dicXiaoqu[city]['allUV'] = 0
            dicXiaoqu[city]['allPV'] = 0

#with open('xiaoquKws.txt','r') as xiaoquKws:
for line in xiaoquKws:
    try:
        cat, city, xiaoqu, uv, v, pv = line.split('\t')
    except:
        print line
        continue
    if city in dicXiaoqu:
        dicXiaoqu[city]['allUV'] = dicXiaoqu[city]['allUV'] + int(uv)
        dicXiaoqu[city]['allPV'] = dicXiaoqu[city]['allPV'] + int(pv)
        '''if xiaoqu in dicXiaoqu[city]:
            dicXiaoqu[city]['sumUV'] = dicXiaoqu[city]['sumUV'] + int(uv)
            dicXiaoqu[city]['sumPV'] = dicXiaoqu[city]['sumPV'] + int(pv)'''
        for xq in dicXiaoqu[city]:
            if xiaoqu.find('xq') != -1:
                dicXiaoqu[city]['sumUV'] = dicXiaoqu[city]['sumUV'] + int(uv)
                dicXiaoqu[city]['sumPV'] = dicXiaoqu[city]['sumPV'] + int(pv)
                break
for city in dicXiaoqu:
    print city, dicXiaoqu[city]['sumUV'], dicXiaoqu[city]['sumPV'], dicXiaoqu[city]['allUV'], dicXiaoqu[city]['allPV']