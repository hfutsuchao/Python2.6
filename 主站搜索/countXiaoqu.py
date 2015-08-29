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
with open('utf8xq.txt') as set:
    for s in set:
        #keys,value = s.split('\t')
        #kws = keys.split('+')
        dic[s[:-1]] = 0
print len(keywords),len(dic)
for dicKey in keywords:
    #print dicKey
    if dicKey in dic:
        print dicKey
        sum = sum + int(keywords[dicKey])
print sum