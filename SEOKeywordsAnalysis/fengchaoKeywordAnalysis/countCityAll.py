#coding:utf-8
dic = {}

outputFile = open('output.txt','w')
with open('F:/kuaipan/MyTools/Python2.6/MyClass/kwAll.txt','r') as file:
    for line in file:
        city,kw,search,isSelf,id,hot = line.split('\t')
        if (kw.find('租房') != -1) or (kw.find('出租') != -1) or (kw.find('租赁') != -1):
            if (kw.find('58') == -1) and (kw.find('搜房') == -1) and (kw.find('安居客') == -1):
                if kw not in dic:
                    dic[kw] = search
for kw in dic:
    outputFile.write(kw + '\t' + dic[kw] + '\n')