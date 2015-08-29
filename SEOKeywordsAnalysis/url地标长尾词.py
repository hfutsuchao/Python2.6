#coding:utf-8
import os

save_path = './locURL'
if not os.path.isdir(save_path):    #目录不存在就创建
            os.makedirs(save_path)

citys = open('city.txt','r')
dicCity = {}

for c in citys:
    domain,cityName = c[:-1].split('\t')
    dicCity[cityName] = domain

print dicCity
num = 0
with open('query_result.csv','r') as tmpfile:
    result = open(save_path+'/locURL'+str(num)+'.txt','w')
    for line,i in enumerate(tmpfile):
        i = i.replace('"','')
        if int(line/16000) > num:
            num = num + 1
            result.close()
            result = open(save_path+'/locURL'+str(num)+'.txt','w')
        try:
            city,name,pinyin = i[:-1].split(',')
            url1 = "http://" + dicCity[city] + ".ganji.com/fang1/loc_" + pinyin + "/"
            url3 = "http://" + dicCity[city] + ".ganji.com/fang3/loc_" + pinyin + "/"
            url5 = "http://" + dicCity[city] + ".ganji.com/fang5/loc_" + pinyin + "/"
            result.write(url1+'\n'+url3+'\n'+url5+'\n')
        except Exception, e:
            print i, e
