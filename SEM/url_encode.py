#coding:utf-8

import urllib

fileKw = open('kw.txt','r').readlines()
fileCity = open('city.txt','r').readlines()
result = open('urlEncode.txt','w')

dic = {}

for line in fileCity:
	domain, city = line.split('\t')
	dic[domain] = city[:-1]

for line in fileKw:
	try:
		domain, kw, num = line.split('\t')
		result.write(dic[domain] + '\t' + line[:-1] + '\thttp://' + domain + '.ganji.com/fang1/_' + urllib.urlencode({'':kw}).split('=')[1] + '/\thttp://3g.ganji.com/' + domain + '_fang1/?keyword=' + urllib.urlencode({'':kw}).split('=')[1] + '\n')
	except Exception,e:
		print line,e