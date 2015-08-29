# coding: utf-8
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
dataClick = open('C:\\Users\\suchao\\Desktop\\quzhongjiedianji.log').readlines()
dataXianshi = open('C:\\Users\\suchao\\Desktop\\quzhongjiexianshi.log').readlines()
resultShow = open(dateNow+'resultShow.txt','w')
resultClick = open(dateNow+'resultClick.txt','w')
resultShowGeren = open(dateNow+'resultShowGeren.txt','w')
resultClickGeren = open(dateNow+'resultClickGeren.txt','w')
resultShowmfzj = open(dateNow+'resultShowmfzj.txt','w')
resultClickmfzj = open(dateNow+'resultClickmfzj.txt','w')
resultShowzj = open(dateNow+'resultShowzj.txt','w')
resultClickzj = open(dateNow+'resultClickzj.txt','w')

#区分城市
cities = ['北京','上海','广州','深圳']
for dc in dataClick:
    date,category,agent,tuiguang,url,gjalog = dc.split('\t')
    peizhi = gjalog.split('@')
    del peizhi[0]
    #print peizhi
    peizhiInfo = ''
    for p in peizhi:
        peizhiInfo+='\t'+p
    peizhiInfo = peizhiInfo[1:]
    try:
        city = gjalog.split('@')[1][5:]
    except:
        print dc
        continue
    if city in cities:
        resultClick.write(date+'\t'+category+'\t'+agent+'\t'+tuiguang+'\t'+peizhiInfo)
resultClick.close()

for dx in dataXianshi:
    date,category,agent,tuiguang,url,gjalog = dx.split('\t')
    peizhi = gjalog.split('@')
    del peizhi[0]
    #print peizhi
    peizhiInfo = ''
    for p in peizhi:
        peizhiInfo+='\t'+p
    peizhiInfo = peizhiInfo[1:]
    try:
        city = gjalog.split('@')[1][5:]
    except:
        print dx
        continue
    if city in cities:
        resultShow.write(date+'\t'+category+'\t'+agent+'\t'+tuiguang+'\t'+peizhiInfo)
resultShow.close()

resultShow = open(dateNow+'resultShow.txt','r').readlines()
resultClick = open(dateNow+'resultClick.txt','r').readlines()

#区分身份

for show in resultShow:
    if show.find('tuiguang=1') != -1:
        resultShowzj.write(show)
    elif show.find('agent=1') != -1 :
        resultShowmfzj.write(show)
    elif show.find('agent=0') != -1 :
        resultShowGeren.write(show)
    else :
        print 'error!\t',show

for click in resultClick:
    if click.find('tuiguang=1') != -1:
        resultClickzj.write(click)
    elif click.find('agent=1') != -1 :
        resultClickmfzj.write(click)
    elif click.find('agent=0') != -1 :
        resultClickGeren.write(click)
    else :
        print 'error!\t',click

#细分城市