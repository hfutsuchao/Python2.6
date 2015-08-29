#coding: gbk
import re
searches = open('C:\\Users\\suchao\\Desktop\\614.txt').readlines()
keywords = open('C:\\Users\\suchao\\Desktop\\xiaoqu.txt').readlines()

keywords = [i[:-1] for i in keywords]

result = {}
keys = {}
i=0;
for k in keywords:
    keys[i]=k
    i = i + 1

i=0
for search in searches:
    for key in keys:
        if search.find(keys[key]) != -1:
            result[i] = search[:-1]
            #print result[i]
            i = i + 1
            break
sum = 0
#print len(result)
for r in result:
    try:
        key,count = result[r].split('\t')
        print count
    except:
        print result[r]
        continue
    #print count
    sum = sum + int(count)
print sum
