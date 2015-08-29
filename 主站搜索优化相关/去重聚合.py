#coding: gbk
have = open('C:\\Users\\suchao\\Desktop\\gjz.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\result.txt','w')
dic = {}
for h in have:
    domain,uv,v,pv,kw = h.split('\t')
    if kw in dic:
        dic[kw] = int(dic[kw]) + int(uv)
    else:
        dic[kw] = int(uv)
for i in sorted(dic.iteritems(), key=lambda d:int(d[1]), reverse = True ):
    result.write(i[0][:-1]+'\t'+str(i[1])+'\n')