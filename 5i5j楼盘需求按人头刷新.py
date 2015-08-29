#coding: utf-8
import random
f1named1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang13-03-20-03-26-5i5j-refresh.txt').readlines()
f5named2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang5-03-20-03-26-5i5j-refresh.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\resultjjr.txt','w')
data = {}
for n1 in f1named1[1:]:
    districtName,xiaoquName,accountId,customerName,refreshCount = n1.split('\t')
    id = xiaoquName + '\t' + accountId
    if id in data:
        if 'f1refresh' in data[id]:
            data[id]['f1f1refresh'] = int(data[id]['f1refresh']) + int(refreshCount)
        else:
            data[id]['f1refresh'] = int(refreshCount)
            data[id]['customerName'] = customerName
            data[id]['f5refresh'] = 0
    else:
        data[id] = {}
        data[id]['f1refresh'] = int(refreshCount)
        data[id]['f5refresh'] = 0
        data[id]['customerName'] = customerName
for n1 in f5named2[1:]:
    districtName,xiaoquName,accountId,customerName,refreshCount = n1.split('\t')
    id = xiaoquName + '\t' + accountId
    if id in data:
        if 'f5refresh' in data[id]:
            data[id]['f5f1refresh'] = int(data[id]['f5refresh']) + int(refreshCount)
        else:
            data[id]['f5refresh'] = int(refreshCount)
            data[id]['customerName'] = customerName
            data[id]['f1refresh'] = 0
    else:
        data[id] = {}
        data[id]['f5refresh'] = int(refreshCount)
        data[id]['f1refresh'] = 0
        data[id]['customerName'] = customerName
for id in data:
    result.write(id+'\t'+data[id]['customerName']+'\t'+str(data[id]['f5refresh'])+'\t'+str(data[id]['f1refresh'])+'\t'+str(int(data[id]['f1refresh'])+int(data[id]['f5refresh']))+'\n')