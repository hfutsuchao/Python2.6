#coding:utf-8
data = open('F:/BaiduYunDownload/tianya/tianya.txt','r')
for line in data:
    kw = raw_input("ToDo ID:")
    if line.find(kw) != -1:
        print line