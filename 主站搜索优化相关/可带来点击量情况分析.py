#coding: gbk
have = open('C:\\Users\\suchao\\Desktop\\gjz.txt').readlines()
zhuzhan = open('C:\\Users\\suchao\\Desktop\\zhuzhan.txt').readlines()
#result = open('C:\\Users\\suchao\\Desktop\\result.txt','w')
dic = {}
sum = 0
for kw in zhuzhan:
    kw = kw[:-1]
    #print kw
    for h in have:
        gjz,uv = h.split('\t')
        #if gjz.find(kw) != -1:
        if gjz == kw:
            #print kw
            sum = sum + int(uv)
print sum
'''            print 1
            if kw in dic:
                dic[kw] = int(dic[kw]) + int(uv)
            else:
                dic[kw] = int(uv)
print len(dic)
for i in sorted(dic.iteritems(), key=lambda d:int(d[1]), reverse = True ):
    result.write(i[0]+'\t'+str(i[1])+'\n')'''