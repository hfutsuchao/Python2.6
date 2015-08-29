#coding: gbk
ours = open('C:\\Users\\suchao\\Desktop\\xiaoqu_allbs.txt').readlines()
have = open('C:\\Users\\suchao\\Desktop\\af_sh.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\shdiff.txt','w')
resultkeyi = open('C:\\Users\\suchao\\Desktop\\shkeyi.txt','w')
#resultsame = open('C:\\Users\\suchao\\Desktop\\shsame.txt','w')
for h in have:
    name,sq,address = h.decode('gbk').split('\t')
    #
    length = len(name)
    n = []
    if length>3:
        for i in range(0,length-3):
            n.append(name[i:i+3])
    else:
        n.append(name)
    t = 0
    for sname in n:
        for our in ours:
            m,ct,a = our.split('\t')
            if (ct == 'sh') and (m.find(sname) != -1):
                t=1
                if name != m:
                    resultkeyi.write(h[:-1]+'\t'+our)
                break;
        if 1 == t:
            break;
    if t==0:
        result.write(h)
result.close()
resultkeyi.close()
#
'''
t = 0
for our in ours:
    m,ct,a = our.split('\t')
    if (ct == 'sh') and (m == name):
        t=1
        resultsame.write(h[:-1]+'\t'+our)
        break;
if(t==0):
    result.write(h)
'''
