#coding: gbk
have = open('C:\\Users\\suchao\\Desktop\\xq.txt').readlines()
domains = open('C:\\Users\\suchao\\Desktop\\domain.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\result.txt','w')

domainDic = {}
for domain in domains:
    d,name = domain.split('\t')
    domainDic[d] = name[:-1]
dic = {}

for kw in have:
    xq,dm = kw.split('\t')
    try:
        result.write(xq + '\t' + domainDic[dm[:-1]]+'\n')
    except:
        print xq,dm