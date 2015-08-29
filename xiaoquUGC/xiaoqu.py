#coding:utf-8

dic = {}

xiaoquDic = {}

cityBig = ["sh","cd","bj","gz","nj","cq","wh","tj","sz","hz","sjz","zz","cs","qd","fz","sy","foshan","hf","su","km","dl","jn","xa","nn","hn","dg","ty","nc","xm","cc","zhongshan","zhuhai","nb","wx","hrb","changzhou","weifang","gy","yantai","huizhou","quanzhou"]
cityMiddle = ["lz","nantong","linyi","yangzhou","tangshan","wei","xuzhou","zibo","qinhuangdao","xj","jiaxing","sanya","zhuzhou","baoding","gl","shaoxing","nmg","mianyang","jilin","yc","qingyuan","langfang","zhenjiang","xn","hengshui"]

boundaryBig = 10
boundaryMiddle = 6
boundarySmall = 5

a = 0
b = 0
c = 0

bigFile = open('bigCity.txt','w')
middleFile = open('middleCity.txt','w')
smallFile = open('smallCity.txt','w')

with open('C:/Users/suchao/Desktop/xiaoqu1117.xls','r') as xiaoquFile:
    for xiaoquInfo in xiaoquFile:
        id, city, districtId, streetId, xiaoqu, lnglat, pinyin, address, times = xiaoquInfo.split('\t')
        if city in cityBig:
            if (int(times) >= boundaryBig):
                try:
                    dic[city] = dic[city] + 1
                    a = a + 1
                    #print xiaoquInfo
                    bigFile.write(xiaoquInfo)
                except:
                    dic[city] = 1
            continue
        if (city in cityMiddle):
            if int(times) >= boundaryMiddle:
                try:
                    dic[city] = dic[city] + 1
                    b = b + 1
                    middleFile.write(xiaoquInfo)
                except:
                    dic[city] = 1
                    middleFile.write(xiaoquInfo)
            continue
        if int(times) >= boundarySmall:
            try:
                dic[city] = dic[city] + 1
                c = c + 1
                smallFile.write(xiaoquInfo)
            except:
                dic[city] = 1
                smallFile.write(xiaoquInfo)

print  a,b,c
for city in dic:
    #print city,dic[city]
    pass