# coding: gbk
import os,time

dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))

data = open('C:\\Users\\suchao\\Desktop\\rent.txt').readlines()
sqresult = open(dateNow+'sqresult.txt','w')
stresult = open(dateNow+'stresult.txt','w')
lpresult = open(dateNow+'lpresult.txt','w')
cmyresult = open(dateNow+'cmyresult.txt','w')
tresult = open(dateNow+'tresult.txt','w')
arrTime = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']


#######################################以下为筛选商圈信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(district):
        dic[district] = dic[district] + 1
    else:
        dic[district] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):sqresult.write(i[0]+'\t'+str(i[1])+'\n')

#######################################以下为筛选街道信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(street):
        dic[street] = dic[street] + 1
    else:
        dic[street] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):stresult.write(i[0]+'\t'+str(i[1])+'\n')

#######################################以下为筛选楼盘小区信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(lp):
        dic[lp] = dic[lp] + 1
    else:
        dic[lp] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):lpresult.write(i[0]+'\t'+str(i[1])+'\n')

#######################################以下为筛选经纪公司信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(companyName):
        dic[companyName] = dic[companyName] + 1
    else:
        dic[companyName] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):cmyresult.write(i[0]+'\t'+str(i[1])+'\n')

#######################################以下为筛选热门时段信息#########################################
dic = {}
for time in arrTime:
    dic[time] = 0
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if companyName.find('中大恒基') != -1:
        t = datetime[11:13]
        dic[t] = dic[t] + 1
for time in arrTime:
    tresult.write(time+'\t'+str(dic[time])+'\n')