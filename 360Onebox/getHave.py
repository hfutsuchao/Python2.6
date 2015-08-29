#coding:gbk

dicHave = {}

dic = {}

with open('have.txt','r') as have:
    for h in have:
        dicHave[h[:-1]] = ''

with open('allcitydist.txt','r') as allcitydist:
    for citydist in allcitydist:
        short_name,domain,short_name,url = citydist.split('\t')
        if domain in dicHave:
            dic[citydist] = ''
            
for i in dic.keys():
    print i[:-1]