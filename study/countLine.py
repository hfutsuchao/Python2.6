#coding: gbk
have = open('C:\\Users\\suchao\\Desktop\\puids.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\resultPuids.txt','w')
dic = {}
for kw in have:
    if kw[:-1] in dic:
        dic[kw[:-1]] = dic[kw[:-1]] + 1
    else:
        dic[kw[:-1]] = 1
for kw in dic:
    result.write(kw + '\t' + str(dic[kw]) + '\n')