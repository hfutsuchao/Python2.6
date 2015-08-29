#coding: utf-8
import os

keywords = {}

dic = {}

sum = 0

with open('fangkwinall.txt') as kw:
    for s in kw:
        '''keys,value = s.split('\t')
        keywords[keys] = int(value)'''
        
        #cat,uv,v,pv,keyword = s.split('\t')
        
        try:
            #keyword,uv,v,pv = s.split('\t')
            keyword,uv = s.split('\t')
            keywords[keyword] = int(uv)
        except:
            print s
print 'ok'
with open('utf8xq.txt') as set:
    for s in set:
        #keys,value = s.split('\t')
        #kws = keys.split('+')
        dic[s[:-1]] = 0
print 'ok2'
print len(keywords),len(dic)
for dicKey in keywords:
    for kw in dic:
        t = 0
        #kw = kw.split('+')
        for k in kw:
            #if dicKey.find(k) == -1:
            if dicKey == kw:
                break
            else:
                t = t + 1
                continue
        if t != len(kw):
            #print dicKey,keywords[dicKey]
            sum = sum + int(keywords[dicKey])
            break
print sum