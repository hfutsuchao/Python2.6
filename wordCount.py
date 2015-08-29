# coding: gbk

tmp = open('C:\\Users\\suchao\\Desktop\\temp.txt').readlines()

biaodian = [",","，"]

dic = {}

for t in tmp:
    if t.find('，') != -1:
        t = "1111111"
    if t in dic:
        dic[t] = dic[t] + 1
    else:
        dic[t] = 1

for k in dic:
    print k[:-1],dic[k]