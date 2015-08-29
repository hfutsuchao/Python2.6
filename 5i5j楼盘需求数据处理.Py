#coding: utf-8
import random
f1named1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang13-03-20-03-26-5i5j-named.txt').readlines()
f5named2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang5-03-20-03-26-5i5j-named.txt').readlines()
f1other1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang13-03-20-03-26-5i5j-other.txt').readlines()
f5other2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang5-03-20-03-26-5i5j-other.txt').readlines()
f1mf1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang13-03-27-5i5j-click-all.txt').readlines()
f5mf2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang5-03-27-5i5j-click-all.txt').readlines()
xiaoquRelation = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\5i5j_bj_xiaoqu_names.uniq.txt').readlines()

refreshes = {}
clicks = {}
companys = {'410':"zhongdahengji",'936':"xinzun",'835':"5i5j",'897':"ljdc",'972':"zhongyuandichan",'0':"other",'1':'mianfei'}

#****fang1/3****#
for n1 in f1named1[1:]:
    companyId,xiaoquName,clickCount,refreshCount = n1.split('\t')
    if companyId in refreshes:
        if xiaoquName in refreshes[companyId]:
            refreshes[companyId][xiaoquName] = int(refreshes[companyId][xiaoquName]) + int(refreshCount)
        else:
            refreshes[companyId][xiaoquName] = int(refreshCount)
    else:
        refreshes[companyId] = {}
        refreshes[companyId][xiaoquName] = int(refreshCount)
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
for n1 in f1other1[1:]:
    xiaoquName,clickCount,refreshCount = n1.split('\t')
    companyId = '0'
    if companyId in refreshes:
        if xiaoquName in refreshes[companyId]:
            refreshes[companyId][xiaoquName] = int(refreshes[companyId][xiaoquName]) + int(refreshCount)
        else:
            refreshes[companyId][xiaoquName] = int(refreshCount)
    else:
        refreshes[companyId] = {}
        refreshes[companyId][xiaoquName] = int(refreshCount)
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
#others
for n1 in f1mf1[1:]:
    xiaoquName,clickCount = n1.split('\t')
    companyId = '1'
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
#****fang5****#
'''for n1 in f5named2[1:]:
    companyId,xiaoquName,clickCount,refreshCount = n1.split('\t')
    if companyId in refreshes:
        if xiaoquName in refreshes[companyId]:
            refreshes[companyId][xiaoquName] = int(refreshes[companyId][xiaoquName]) + int(refreshCount)
        else:
            refreshes[companyId][xiaoquName] = int(refreshCount)
    else:
        refreshes[companyId] = {}
        refreshes[companyId][xiaoquName] = int(refreshCount)
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
for n1 in f5other2[1:]:
    xiaoquName,clickCount,refreshCount = n1.split('\t')
    companyId = '0'
    if companyId in refreshes:
        if xiaoquName in refreshes[companyId]:
            refreshes[companyId][xiaoquName] = int(refreshes[companyId][xiaoquName]) + int(refreshCount)
        else:
            refreshes[companyId][xiaoquName] = int(refreshCount)
    else:
        refreshes[companyId] = {}
        refreshes[companyId][xiaoquName] = int(refreshCount)
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
#others
for n1 in f5mf2[1:]:
    xiaoquName,clickCount = n1.split('\t')
    companyId = '1'
    if companyId in clicks:
        if xiaoquName in clicks[companyId]:
            clicks[companyId][xiaoquName] = int(clicks[companyId][xiaoquName]) + int(clickCount)
        else:
            clicks[companyId][xiaoquName] = int(clickCount)
    else:
        clicks[companyId] = {}
        clicks[companyId][xiaoquName] = int(clickCount)
'''
for companyId in refreshes:
    if companyId in ['0','1']:
        for xiaoquName in refreshes[companyId]:
            #print refreshes[companyId][xiaoquName]
            refreshes[companyId][xiaoquName] = int((1+max(0.2,random.random()/3))*int(refreshes[companyId][xiaoquName]))
            #print refreshes[companyId][xiaoquName],'haha'
for companyId in clicks:
    if companyId in ['0','1']:
        for xiaoquName in clicks[companyId]:
            #print clicks[companyId][xiaoquName]
            clicks[companyId][xiaoquName] = int((1+max(0.2,random.random()/3))*int(clicks[companyId][xiaoquName]))
            #print clicks[companyId][xiaoquName],'haha'

for companyId in refreshes:
    refreshFile = open('C:\\Users\\suchao\\Desktop\\'+companys[companyId]+'refresh.txt','w')
    clickFile = open('C:\\Users\\suchao\\Desktop\\'+companys[companyId]+'click.txt','w')
    for i in sorted(refreshes[companyId].iteritems(), key=lambda d:int(d[1]), reverse = True ):
        refreshFile.write(str(companyId)+'\t'+str(i[0])+'\t'+str(i[1])+'\n')
    for i in sorted(clicks[companyId].iteritems(), key=lambda d:int(d[1]), reverse = True ):
        clickFile.write(str(companyId)+'\t'+str(i[0])+'\t'+str(i[1])+'\n')
    refreshFile.close()
    clickFile.close()