#coding:utf-8
xiaoqu = open("kw.txt").readlines()
for i in range(1,5):
    dic = {}
    for bj in xiaoqu:
        try:
            bj = bj.decode('utf-8')
            kw,uv = bj.split('\t')
        except:
            print bj 
            continue
        length = len(kw)
        if(length >= i):
            for x in range(0,length):
                if((x+i) <= length):
                    if(kw[x:x+i] in dic):
                        dic[kw[x:x+i]] = dic[kw[x:x+i]] + int(uv)
                    else:
                        dic[kw[x:x+i]] = int(uv)
    ciyu_count = open(str(i)+'ciyu_count.txt','w')
    for d in sorted(dic.items(), key = lambda i:i[1], reverse=True):
        ciyu_count.write(d[0]+'\t'+str(d[1])+'\n')
