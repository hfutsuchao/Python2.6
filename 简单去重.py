#coding: gbk
have = open('C:\\Users\\suchao\\Desktop\\xiaoqu-name.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\result.txt','w')
dic = {}
for kw in have:
    if kw in dic:
        pass
    else:
        dic[kw] = ''
for kw in dic:
    result.write(kw)