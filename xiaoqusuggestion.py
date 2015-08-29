#!/usr/bin/env python
#coding:gbk
import re
def ditstance(source, target):
    """ ditstance(source, target)->int return the levenshtein ditstance
>>> ditstance("126.com", "127.com")
1
>>> ditstance("127.com", "126.com")
1
>>> ditstance("hotmail.com", "hotmail.com")
0
>>> ditstance("", "")
0
>>> ditstance("sina.com", "")
8
>>> ditstance("", "gmail.com")
9
>>> ditstance("sina.com", "sina.cn")
2
>>> ditstance("qq.cn", "qq.com")
2
>>> ditstance("139.com", ".139.com")
1
>>> ditstance("qq.", "qq.com")
3
>>> ditstance("gmail.com", ".gmail.com")
1
>>> ditstance(".gmail.com", "gmail.com")
1
"""
    src_length = len(source)+1
    tgt_length = len(target)+1

    if src_length == 1:
        return tgt_length - 1
    if tgt_length == 1:
        return src_length - 1

    matrix = [range(tgt_length)]
    for i in range(1, src_length):
        row = [0]*tgt_length
        row[0] = i
        matrix.append(row)

    for i in range(1, src_length):
        src_char = source[i-1]
        for j in range(1, tgt_length):
            tgt_char = target[j-1]
            cost = 0 if src_char == tgt_char else 1
            above = matrix[i-1][j]+1
            left = matrix[i][j-1]+1
            diag = matrix[i-1][j-1]+cost
            value = min(above, left, diag)
            matrix[i][j]=value
    #return matrix[src_length-1][tgt_length-1]
    return 1-float(matrix[src_length-1][tgt_length-1])/(max(tgt_length,src_length)-1)

if __name__=="__main__":
    xq = open('C:\\Users\\suchao\\Desktop\\xq.txt').readlines()
    dic = {}
    for i in xq:
        stmp = ditstance("下地南", i[:-1])*2
        r = re.findall('(.*)(下)(.*)(地)(.*)(南)(.*)',i[:-1])
        if len(r)>0:
            #print r[0]
            if r[0][0]=='' and r[0][1]=='下':
                scort = 1
            else:
                scort = 0
            if r[0][2]=='' and r[0][3]=='地':
                scort = scort + 1
            else:
                scort = scort + 0
            if r[0][4]=='' and r[0][5]=='南':
                scort = scort + 1
            else:
                scort = scort + 0
            if r[0][6]=='':
                scort = scort + 1
            else:
                scort = scort + 0        
            dic[i[:-1]] = scort
        if i[:-1] not in dic:
            dic[i[:-1]] = stmp
    #print len(dic)
    tmp = 0
    for r in sorted(dic.iteritems(),key = lambda d:d[1],reverse = True):
        print r[0],r[1]
        if tmp==10:
            break
        tmp = tmp + 1