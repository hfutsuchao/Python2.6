#coding:utf-8
f = open('C:/Users/suchao/Desktop/1.txt','r').readlines()

r = open('C:/Users/suchao/Desktop/res.txt','w')

for line in f:
    xiaoqu_id,city,type,content = line.split('\t')
    for k in content.split('、'):
        r.write(xiaoqu_id + '\t' + city + '\t' + type + '\t' + k + '\n')