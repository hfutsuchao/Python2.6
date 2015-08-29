# coding: utf-8
import os,MySQLdb,hashlib,json,sys


dic = {}

dt = ["2013-07-"+('0'+str(i),str(i))[len(str(i))-1] for i in range(5,19)]
type = ['1','2','3']
pos= ['1','2','3']
show_type = ['0','1','2','3','4']
related_house = ['0','1']
is_tg = ['0','1']
tag = ['','city','district','street','xiaoqu','searchKey','close','house']
atype = ['show','click']

for d in dt:
    dic[d] ={}
    for ap in atype:
        dic[d][ap] = {}
        for tp in type:
            dic[d][ap][tp] = {}
            for p in pos:
                dic[d][ap][tp][p] = {}
                for st in show_type:
                    dic[d][ap][tp][p][st] = {}
                    for rh in related_house:
                        dic[d][ap][tp][p][st][rh] = {}
                        for it in is_tg:
                            dic[d][ap][tp][p][st][rh][it] = {}
                            for tg in tag:
                                dic[d][ap][tp][p][st][rh][it][tg] = 0

#dic.setdefault(((dt,{})[type],{})[pos],{})

uuids = {}

tagCount = 0 

with open("C:\\Users\\suchao\\Desktop\\5-18seoshow_click.txt",'r') as file:
    for uc in file:
        dt,uuid,url,type,pos,related_house,is_tg,show_type,tag,atype = uc.split('\t')
        if type == '2':
            uuids[dt + '_' + uuid] = type+ ',' +pos+ ',' +related_house+ ',' +is_tg
        #print uc
        atype = atype[:-1]
        if 1 or tag != "close":
            dic[dt][atype][type][pos][show_type][related_house][is_tg][tag] = dic[dt][atype][type][pos][show_type][related_house][is_tg][tag] + 1
        else:
            tagCount = tagCount + 1

with open("C:\\Users\\suchao\\Desktop\\5-18seofytj.txt",'r') as file:
    for uc in file:
        dt,uuid,show_type,atype = uc.split('\t')
        try:
            #type,pos,related_house,is_tg = uuids[dt + '_' + uuid].split(',')
            type = '2'
            pos = '1'
            related_house = '1'
            tag = 'house'
            is_tg = '1'
        except Exception,e:
            print e
            #sys.exit()
            tagCount = tagCount + 1
            continue
        #print uc
        atype = atype[:-1]
        dic[dt][atype][type][pos][show_type][related_house][is_tg][tag] = dic[dt][atype][type][pos][show_type][related_house][is_tg][tag] + 1

print tagCount

'''
for d in dic:
    #dic[d] ={}
    for ap in dic[d]:
        #dic[d][ap] = {}
        for tp in dic[d][ap]:
            #dic[d][ap][tp] = {}
            for p in dic[d][ap][tp]:
                #dic[d][ap][tp][p] = {}
                for st in dic[d][ap][tp][p]:
                    #dic[d][ap][tp][p][st] = {}
                    for rh in dic[d][ap][tp][p][st]:
                        #dic[d][ap][tp][p][st][rh] = {}
                        for it in dic[d][ap][tp][p][st][rh]:
                            #dic[d][ap][tp][p][st][rh][it] = {}
                            for tg in dic[d][ap][tp][p][st][rh][it]:
                                if dic[d][ap][tp][p][st][rh][it][tg] != 0:
                                    print d,ap,tp,p,st,rh,it,tg,dic[d][ap][tp][p][st][rh][it][tg]
'''

dt = ["2013-07-"+('0'+str(i),str(i))[len(str(i))-1] for i in range(5,19)]
type = ['1','2','3']
pos= ['1','2','3']
show_type = ['0','1','2','3','4']
related_house = ['0','1']
is_tg = ['0','1']
tag = ['','city','district','street','xiaoqu','searchKey','close','house']
atype = ['show','click']

'''for d in dt:
    #dic[d] ={}
    for ap in atype:
        #dic[d][ap] = {}
        for tp in type:
            #dic[d][ap][tp] = {}
            for p in pos:
                #dic[d][ap][tp][p] = {}
                for st in show_type:
                    #dic[d][ap][tp][p][st] = {}
                    for rh in related_house:
                        #dic[d][ap][tp][p][st][rh] = {}
                        for it in is_tg:
                            #print d,tp,p,st,rh,it
                            #dic[d][ap][tp][p][st][rh][it] = {}
                            dic[d]['show'][tp][p][st][rh][it][""] = (1,dic[d]['show'][tp][p][st][rh][it][""])[dic[d]['show'][tp][p][st][rh][it][""]>0]
                            print d,tp,p,st,rh,it,sum(dic[d]['click'][tp][p][st][rh][it].values()),dic[d]['show'][tp][p][st][rh][it][""],float(sum(dic[d]['click'][tp][p][st][rh][it].values()))/dic[d]['show'][tp][p][st][rh][it][""]
'''

r = open('rate.txt','w')
for d in dt:
    #dic[d] ={}
    for tp in type:
        #dic[d][ap][tp] = {}
        for p in pos:
            #dic[d][ap][tp][p] = {}
            for st in show_type:
                #dic[d][ap][tp][p][st] = {}
                for rh in related_house:
                    #dic[d][ap][tp][p][st][rh] = {}
                    for it in is_tg:
                        for t in tag:
                            #print d,tp,p,st,rh,it
                            #dic[d][ap][tp][p][st][rh][it] = {}
                            dic[d]['show'][tp][p][st][rh][it][""] = (1,dic[d]['show'][tp][p][st][rh][it][""])[dic[d]['show'][tp][p][st][rh][it][""]>0]
                            r.write(str(d) + '\t' + str(tp) + '\t' + str(p) + '\t' + str(st) + '\t' + str(rh) + '\t' + str(it) + '\t' + str(t) + '\t' + str(dic[d]['click'][tp][p][st][rh][it][t]) + '\t' + str(dic[d]['show'][tp][p][st][rh][it][""]) + '\t' + str(float(dic[d]['click'][tp][p][st][rh][it][t])/dic[d]['show'][tp][p][st][rh][it][""]) + '\n' )
                            