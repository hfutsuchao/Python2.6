#coding:utf-8
import os,re,codecs
tmp = open('C:\\Users\\suchao\\Desktop\\tmp.txt','w')
'''

#import changeNum.py
source = open('C:\\Users\\suchao\\Desktop\\xq.txt').readlines()


for s in source:
    if len(re.findall("[，、。《》]",s.decode("utf-8)))>=1:
        #print s
        tmp.write(s)

'''

i = 1

with codecs.open('C:\\Users\\suchao\\Desktop\\xq.txt','r','utf-8') as f:
    for s in f: # 这个python会自动给你处理的，用的迭代，基本不占内存，看你每行占的内存确定
        #print s
        a = re.findall(ur"[“”，。！《》、\-\(\)（）/\'\,;；？]",s)
        if len(a)>=1:
            i = i + 1
            #print i
        else:
            if len(s) <= 10:
                try:
                    tmp.write(s[:-1])
                except:
                    print 1
print i