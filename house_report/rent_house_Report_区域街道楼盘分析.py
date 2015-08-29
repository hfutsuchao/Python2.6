# coding: gbk
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))

#打开并处理商圈，街道，楼盘等信息
data = open('C:\\Users\\suchao\\Desktop\\rent.txt').readlines()
districts = open(dateNow+'sqresult.txt').readlines()
streets = open(dateNow+'stresult.txt').readlines()
companys = open(dateNow+'cmyresult.txt').readlines()
lps = open(dateNow+'lpresult.txt').readlines()

districts = [i.split('\t')[0] for i in districts]
streets = [i.split('\t')[0] for i in streets]
companys = [i.split('\t')[0] for i in companys][:8]
lps = [i.split('\t')[0] for i in lps][:800]

#打开文件，准备写入结果数据

distReport = open(dateNow+'distReport.txt','w')
stReport = open(dateNow+'stReport.txt','w')
lpReport = open(dateNow+'lpReport.txt','w')
'''
districts = ['朝阳','海淀','丰台','昌平','大兴','西城','宣武','房山','东城','石景山']
streets = ['清河','上地','中关村','亚运村','安贞','四季青','芍药居','五棵松','西三旗',
           '六里桥','知春路','西直门','魏公村','国贸','青塔','大望路','公主坟',
           '广安门','西坝河','太阳宫','学院路','惠新西街','双榆树','定慧寺','紫竹桥',
           '航天桥','科技园区','田村','北京大学','鲁谷','马连道','玉泉路','万柳',
           '陶然亭','右安门','军博','德胜门','花园桥','西单','亚运村小营','永定路',
           '阜成门','北大地','苏州桥','看丹桥','皂君庙','金融街','蓟门桥','CBD',
           '北太平庄','车道沟','菜户营','大钟寺','卢沟桥','长椿街','白纸坊','玉泉营',
           '新街口','机场南楼','三里河','岳各庄','八角','宣武门','车公庄','西直门外',
           '牛街','增光路','小西天','月坛','丽泽桥','万泉河','科丰桥','复兴门',
           '积水潭','杨庄','国展','木樨地','鼓楼大街','西便门','礼士路','八里庄',
           '甘家口','展览路','万寿寺','老山','八宝山','天宁寺','西客站','永乐',
           '西局','小马厂','石景山','大观园','燕郊']
companys = ['中大恒基','链家','我爱我家','中原','麦田','安信']
#companys = ['北京中大恒基房地产经纪有限公司','北京链家房地产经纪有限公司','北京我爱我家房地产经纪有限公司','北京中原房地产经纪有限公司','北京麦田房产经纪有限公司','北京安信嘉和房地产经纪有限责任公司']
#companys = ['北京中大恒基房地产经纪有限公司','北京链家房地产经纪有限公司','北京我爱我家房地产经纪有限公司','北京中原房地产经纪有限公司','北京麦田房产经纪有限公司','北京安信嘉和房地产经纪有限责任公司','独立经纪人']
#companys = ['中大恒基','链家','我爱我家','中原','麦田','安信','独立经纪人']
lps = open('lp.txt').readlines()
lps = [l[:-1] for l in lps]
'''

arrTime = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
dicDist = {}

#######################################以下为筛选商圈信息#########################################

for st in districts:
    dicDist[st] = {}
for st in districts:
    dicDist[st][st] = {}
    dicDist[st][st]['post'] = 0
    dicDist[st][st]['clicks'] = 0
    for company in companys:
        dicDist[st][company] = 0
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    for st in districts:
        if district == st:
            dicDist[st][st]['post'] = dicDist[st][st]['post'] + 1
            dicDist[st][st]['clicks'] = dicDist[st][st]['clicks'] + int(clicks)
            for company in companys:
                if companyName == company:
                    dicDist[st][company] = dicDist[st][company] + 1
                    break
            break
for l in districts:
    tmp = dicDist[l][l]['post']
    distReport.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        distReport.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    distReport.write('\n')

dicDist = {}

#####################################下面是筛选街道信息###########################################
for st in streets:
    dicDist[st] = {}
for st in streets:
    dicDist[st][st] = {}
    dicDist[st][st]['post'] = 0
    dicDist[st][st]['clicks'] = 0
    for company in companys:
        dicDist[st][company] = 0
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if street == '':
        street = district
    for st in streets:
        if street == st:
            dicDist[st][st]['post'] = dicDist[st][st]['post'] + 1
            dicDist[st][st]['clicks'] = dicDist[st][st]['clicks'] + int(clicks)
            for company in companys:
                if companyName == company:
                    dicDist[st][company] = dicDist[st][company] + 1
                    break
            break

for l in streets:
    tmp = dicDist[l][l]['post']
    stReport.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        stReport.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    stReport.write('\n')
###################################下面是筛选楼盘小区信息##############################################

dicDist = {}

for l in lps:
    dicDist[l] = {}
for l in lps:
    dicDist[l][l] = {}
    dicDist[l][l]['post'] = 0
    dicDist[l][l]['clicks'] = 0
    for company in companys:
        dicDist[l][company] = 0
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    for l in lps:
        if lp == l:
            dicDist[l][l]['post'] = dicDist[l][l]['post'] + 1
            dicDist[l][l]['clicks'] = dicDist[l][l]['clicks'] + int(clicks)
            for company in companys:
                if companyName == company:
                    dicDist[l][company] = dicDist[l][company] + 1
                    break
            break

for l in lps:
    tmp = dicDist[l][l]['post']
    lpReport.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        lpReport.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    lpReport.write('\n')

print time.time()-t
#os.system('pause')