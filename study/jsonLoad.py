#coding:utf-8

import time
import md5
import json

result = open('/Users/NealSu/Downloads/hotResul.txt','w')
jsonFile = open('/Users/NealSu/Downloads/hot','r').read()

jsons = jsonFile.split("fengexian")

count = 1
dic = {}

for line in jsons:
	toys = json.loads(line)['data']['toys']
	for row in toys:
		dic[count] = row
		count = count + 1

print len(dic)

for i in dic:
    result.write(str(i)+'\t'+str(dic[i]['toyName'].encode('utf-8'))+"\n")
