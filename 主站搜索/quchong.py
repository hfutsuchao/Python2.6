#coding: gbk
import os

qys = {}
sts = {}
xqs = {}

qys1 = {}
sts1 = {}
xqs1 = {}

st2 = open("st2.txt",'w')
xq2 = open("xq2.txt",'w')

with open('qy.txt') as qy:
    for s in qy:
        keys,value = s.split('\t')
        qys[keys] = value
        
with open('st.txt') as st:
    for s in st:
        keys,value = s.split('\t')
        sts[keys] = value

with open('xq.txt') as xq:
    for s in xq:
        try:
            keys,value = s.split('\t')
        except:
            print s
        xqs[keys] = value

print len(qys),len(xqs),len(sts)

for s in sts:
    if s in qys:
        sts[s] = 0

for x in xqs:
    if (x in sts) or (x in qys):
        xqs[x] = 0
        
print len(qys),len(xqs),len(sts)

for s in sts:
    if sts[s] != 0:
        st2.write(s + "\t" +sts[s]) 

for x in xqs:
    if xqs[x] != 0:
        xq2.write(x + "\t" +xqs[x])