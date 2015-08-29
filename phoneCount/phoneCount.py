#coding:utf-8

phoneFiles = open('phoneCount.txt','r').readlines()

dic = {}

for line in phoneFiles:
    dt, phone = line[:-1].split('\t')
    if dt in dic:
        dic[dt]['count'] = dic[dt]['count'] + 1
        if phone not in dic[dt]:
            dic[dt][phone] = ''
    else:
        dic[dt] = {}
        dic[dt]['count'] = 1
        dic[dt][phone] = ''
for dt in dic:
    print dt, dic[dt]['count'], len(dic[dt])