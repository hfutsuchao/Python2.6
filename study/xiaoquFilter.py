#coding:utf-8

signs = ['，','。','：','“','”','!','！','—','（','(',':',',']

xiaoqus = open('xiaoquName.txt','r').readlines()

result = open('resultXiaoqu.txt','w')

for xiaoqu in xiaoqus:

    wirte = True
    if len(xiaoqu) >30 or len(xiaoqu) <9:
        continue
    for s in signs:
        if xiaoqu.find(s) != -1:
            wirte = False
            break
    if wirte :
        result.write(xiaoqu)
    