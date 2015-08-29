# coding: gbk
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
data = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\fufei_zhongjie_short_20121108.log').readlines()
data2 = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\mianfei_geren_short_20121108.log').readlines()
data3 = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\mianfei_zhongjie_short_20121108.log').readlines()
#resultShow = open(dateNow+'resultShow.txt','w')
#resultClick = open(dateNow+'resultClick.txt','w')
resultShowGeren = open(dateNow+'resultShowGeren.txt','w')
resultClickGeren = open(dateNow+'resultClickGeren.txt','w')
#resultShowmfzj = open(dateNow+'resultShowmfzj.txt','w')
#resultClickmfzj = open(dateNow+'resultClickmfzj.txt','w')

arrTime = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

#-----------------------------------------------------------下面为提取相关信息------------------------#

#######################################以下为提取house_id信息#########################################
'''
houseIdShow = {}
houseIdClick = {}
for d in data:
    logTime,gjch,gjalog,uuid,url = d.split('\t')
    if ('-' != url[:-1]) and (url.find('.htm') != -1):
        if gjalog.find("show") != -1:
            city = url[url.index(':')+3:url.index('.')]
            try:
                houseId = url[url.index('-')+1:url.index('.htm')]
            except:
                print url
                exit()
            category = gjch[gjch.index('/fang/fang')+6:gjch.index('/fang/fang')+11]
            if houseId in houseIdShow:
                houseIdShow[houseId] = city+'_'+category+'\t'+str(int(houseIdShow[houseId].split('\t')[1])+1)+'\t'+houseIdShow[houseId].split('\t')[2]+' '+uuid
                #print houseIdShow[houseId]
            else:
                houseIdShow[houseId] = city+'_'+category+'\t'+'1'+'\t'+uuid
        elif gjalog.find('click') != -1:
            city = url[url.index(':')+3:url.index('.')]
            houseId = url[url.index('-')+1:url.index('.htm')]
            category = gjch[gjch.index('/fang/fang')+6:gjch.index('/fang/fang')+11]
            if houseId in houseIdClick:
                houseIdClick[houseId] = city+'_'+category+'\t'+str(int(houseIdClick[houseId].split('\t')[1])+1)+'\t'+houseIdClick[houseId].split('\t')[2]+' '+uuid
                #print houseIdClick[houseId]
            else:
                houseIdClick[houseId] = city+'_'+category+'\t'+'1'+'\t'+uuid
print len(houseIdClick)
print len(houseIdShow)
'''
def getSql(category,houseId,type='zhongjie'):
    #category = houseIdClick[houseId].split('\t')[0].split('_')[1]
    if type == 'zhongjie':
        if category == 'fang1':
            sql = 'SELECT c.CompanyName 客户公司, district_name 区域, street_name 街道, title 标题, image_count 图片数, TYPE 频道类型, bid_status 是否竞价, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,huxing_shi 室,huxing_ting 厅,huxing_wei 卫,peizhi 房屋配置  FROM house_premier.house_source_rent_premier rp INNER JOIN gcrm.customer_account cb INNER JOIN gcrm.customer c ON rp.account_id=cb.AccountId AND cb.CustomerId=c.CustomerId WHERE rp.house_id='+houseId+';'
        elif category == 'fang3':
            sql = 'SELECT c.CompanyName 客户公司, district_name 区域, street_name 街道, title 标题, image_count 图片数, TYPE 频道类型, bid_status 是否竞价, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,house_type 主次卧类型,peizhi 房屋配置  FROM house_premier.house_source_share_premier rp INNER JOIN gcrm.customer_account cb INNER JOIN gcrm.customer c ON rp.account_id=cb.AccountId AND cb.CustomerId=c.CustomerId WHERE rp.house_id='+houseId+';'
        elif category == 'fang5':
            sql = 'SELECT c.CompanyName 客户公司, district_name 区域, street_name 街道, title 标题, image_count 图片数, TYPE 频道类型, bid_status 是否竞价, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,huxing_shi 室,huxing_ting 厅,huxing_wei 卫  FROM house_premier.house_source_sell_premier rp INNER JOIN gcrm.customer_account cb INNER JOIN gcrm.customer c ON rp.account_id=cb.AccountId AND cb.CustomerId=c.CustomerId WHERE rp.house_id='+houseId+';'
        else:
            return '类别错误'
    elif type == 'mianfei':
        if category == 'fang1':
            sql = 'SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,huxing_shi 室,huxing_ting 厅,huxing_wei 卫,peizhi 房屋配置 FROM house_source_rent WHERE puid='+houseId+';'
        elif category == 'fang3':
            sql = 'SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,huxing_shi 室,huxing_ting 厅,huxing_wei 卫,peizhi 房屋配置 FROM house_source_share WHERE puid='+houseId+';'
        elif category == 'fang5':
            sql = 'SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,huxing_shi 室,huxing_ting 厅,huxing_wei 卫 FROM house_source_sell WHERE puid='+houseId+';'
        else:
            return '类别错误'
    else:
        return "参数传入错误！传入：类别，房源ＩＤ"
    return sql
#print getSql('fang5','12321312421','mianfei')
'''
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")

for houseId in houseIdClick:
    category = houseIdClick[houseId].split('\t')[0].split('_')[1]
    #print houseIdClick[houseId],category
    sql = getSql(category,houseId)
    #print sql
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        resultClick.write(houseId+'\t'+houseIdClick[houseId])
        for i in row:
            resultClick.write('\t'+str(i))
        resultClick.write('\n')
resultClick.close()

for houseId in houseIdShow:
    category = houseIdShow[houseId].split('\t')[0].split('_')[1]
    #print houseIdShows[houseId],category
    sql = getSql(category,houseId)
    print sql
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        resultShow.write(houseId+'\t'+houseIdShow[houseId])
        for i in row:
            resultShow.write('\t'+str(i))
        resultShow.write('\n')
resultShow.close()
cursor.close()

'''

#免费贴的数据获取

houseIdShow = {}
houseIdClick = {}
for d in data2:
    logTime,gjch,gjalog,uuid,url = d.split('\t')
    if ('-' != url[:-1]) and (url.find('.htm') != -1):
        if gjalog.find("show") != -1:
            city = url[url.index(':')+3:url.index('.')]
            #print url
            category = gjch[gjch.index('/fang/fang')+6:gjch.index('/fang/fang')+11]
            try:
                houseId = url[url.index('ganji.com/fang')+16:url.index('x.htm')]
            except:
                print url
            #print houseId
            if houseId in houseIdShow:
                if city != 'www':
                    houseIdShow[houseId] = city+'_'+category+'\t'+str(int(houseIdShow[houseId].split('\t')[1])+1)+'\t'+houseIdShow[houseId].split('\t')[2]+' '+uuid
                    #print houseIdShow[houseId]
                else:
                    houseIdShow[houseId] = houseIdShow[houseId].split('\t')[0]+'\t'+str(int(houseIdShow[houseId].split('\t')[1])+1)+'\t'+houseIdShow[houseId].split('\t')[2]+' '+uuid
                    #print houseIdShow[houseId]
            else:
                houseIdShow[houseId] = city+'_'+category+'\t'+'1'+'\t'+uuid
        elif gjalog.find('click') != -1:
            city = url[url.index(':')+3:url.index('.')]
            category = gjch[gjch.index('/fang/fang')+6:gjch.index('/fang/fang')+11]
            #print category
            try:
                houseId = url[url.index('ganji.com/fang')+16:url.index('x.htm')]
            except:
                continue
            if houseId in houseIdClick:
                if city != 'www':
                    houseIdClick[houseId] = city+'_'+category+'\t'+str(int(houseIdClick[houseId].split('\t')[1])+1)+'\t'+houseIdClick[houseId].split('\t')[2]+' '+uuid
                    #print houseIdClick[houseId]
                else:
                    houseIdClick[houseId] = houseIdClick[houseId].split('\t')[0]+'\t'+str(int(houseIdClick[houseId].split('\t')[1])+1)+'\t'+houseIdClick[houseId].split('\t')[2]+' '+uuid
            else:
                houseIdClick[houseId] = city+'_'+category+'\t'+'1'+'\t'+uuid
                #print houseIdClick[houseId]
print len(houseIdClick)
print len(houseIdShow)

#城市对应关系的统计
citys={}

conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="management",charset="gbk")
cursor = conn.cursor()
cursor.execute('SELECT domain,pinyin FROM city;')
for row in cursor.fetchall():
    citys[row[0]]=row[1]
cursor.close()

#免费贴点击部分的统计
for houseId in houseIdClick:
    city = houseIdClick[houseId].split('\t')[0].split('_')[0]
    try:
        city = citys[city]
    except:
        print 'cityerror',houseId,houseIdClick[houseId]
        city = 'others'
    #print city
    try:
        conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")
    except:
        try:
            conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
        except:
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
            except:
                print 'sqlerror',houseId,houseIdClick[houseId]
    #'''
    category = houseIdClick[houseId].split('\t')[0].split('_')[1]
    sql = getSql(category,houseId,"mianfei")
    #print sql
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        resultClickGeren.write(houseId+'\t'+houseIdClick[houseId])
        for i in row:
            resultClickGeren.write('\t'+str(i))
        resultClickGeren.write('\n')
resultClickGeren.close()

#对于免费贴展示部分的统计
for houseId in houseIdShow:
    city = houseIdShow[houseId].split('\t')[0].split('_')[0]
    try:
        city = citys[city]
    except:
        print 'cityerror',houseId,houseIdShow[houseId]
        city = 'others'
    #print city
    try:
        conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")
    except:
        try:
            conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
        except:
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
            except:
                print 'sqlerror',houseId,houseIdShow[houseId]
    try:
        category = houseIdShow[houseId].split('\t')[0].split('_')[1]
        sql = getSql(category,houseId,"mianfei")
        cursor = conn.cursor()
        cursor.execute('SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,huxing_shi 室,huxing_ting 厅,huxing_wei 卫,peizhi 房屋配置 FROM house_source_rent WHERE puid='+houseId+';')
        for row in cursor.fetchall():
            resultShowGeren.write(houseId+'\t'+houseIdShow[houseId])
            for i in row:
                resultShowGeren.write('\t'+str(i))
            resultShowGeren.write('\n')
    except:
        print '执行错误！'
resultShowGeren.close()
cursor.close()



'''
    if house_id in dic:
        #print house_id,dic[house_id]
        huxing_shi = dic[house_id].split('\t')[0]
        price = dic[house_id].split('\t')[1]
    else:
        huxing_shi = 'null'
        price = 'null'
    
    if huxing_shi in dicDist:
        dicDist[huxing_shi][huxing_shi]['count'] = dicDist[huxing_shi][huxing_shi]['count'] + 1
        dicDist[huxing_shi][huxing_shi]['click'] = dicDist[huxing_shi][huxing_shi]['click'] + int(clicks)
        for company in companys:
            if company == companyName:
                dicDist[huxing_shi][company]['count'] = dicDist[huxing_shi][company]['count'] + 1
                dicDist[huxing_shi][company]['click'] = dicDist[huxing_shi][company]['click'] + int(clicks)
                break
    else:
        dicDist[huxing_shi] = {}
        dicDist[huxing_shi][huxing_shi] = {}
        dicDist[huxing_shi][huxing_shi]['count'] = 1
        dicDist[huxing_shi][huxing_shi]['click'] = int(clicks)
        for company in companys:
            dicDist[huxing_shi][company] = {}
            dicDist[huxing_shi][company]['count'] = 0
            dicDist[huxing_shi][company]['click'] = 0
    if price in dicPrice:
        dicPrice[price][price]['count'] = dicPrice[price][price]['count'] + 1
        dicPrice[price][price]['click'] = dicPrice[price][price]['click'] + int(clicks)
        for company in companys:
            if company == companyName:
                dicPrice[price][company]['count'] = dicPrice[price][company]['count'] + 1
                dicPrice[price][company]['click'] = dicPrice[price][company]['click'] + int(clicks)
                break
    else:
        dicPrice[price] = {}
        dicPrice[price][price] = {}
        dicPrice[price][price]['count'] = 1
        dicPrice[price][price]['click'] = int(clicks)
        for company in companys:
            dicPrice[price][company] = {}
            dicPrice[price][company]['count'] = 0
            dicPrice[price][company]['click'] = 0

for huxing_shi in dicDist:
    resultshi.write(str(huxing_shi)+'\t'+str(dicDist[huxing_shi][huxing_shi]['count'])+'-'+str(dicDist[huxing_shi][huxing_shi]['click']))
    for company in companys:
        resultshi.write('\t'+str(dicDist[huxing_shi][company]['count'])+'-'+str(dicDist[huxing_shi][company]['click']))
    resultshi.write('\n')
resultshi.close()
for price in dicPrice:
    resultprice.write(str(price)+'\t'+str(dicPrice[price][price]['count'])+'-'+str(dicPrice[price][price]['click']))
    for company in companys:
        resultprice.write('\t'+str(dicPrice[price][company]['count'])+'-'+str(dicPrice[price][company]['click']))
    resultprice.write('\n')
resultprice.close()

#######################################以下为价格和室型信息的后续处理#########################################

resultshi = open(dateNow+'resultshi.txt').readlines()
resultprice = open(dateNow+'resultprice.txt').readlines()
Reportshi = open(dateNow+'ReportShi.txt','w')
Reportprice = open(dateNow+'ReportPrice.txt','w')
for shi in resultshi:
    s,allCount,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = shi.split('\t')
    Reportshi.write(s+'\t'+allCount.split('-')[0]+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[0]+'\t'+c2.split('-')[0]+'\t'+c3.split('-')[0]+'\t'+c4.split('-')[0]+'\t'+c5.split('-')[0]+'\t'+c6.split('-')[0]+'\t'+c7.split('-')[0]+'\t'+c8.split('-')[0]+'\t'+c9.split('-')[0]+'\t'+c10.split('-')[0]+'\n')
Reportshi.close()
for price in resultprice:
    p,allCount,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = price.split('\t')
    Reportprice.write(p+'\t'+allCount.split('-')[0]+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[0]+'\t'+c2.split('-')[0]+'\t'+c3.split('-')[0]+'\t'+c4.split('-')[0]+'\t'+c5.split('-')[0]+'\t'+c6.split('-')[0]+'\t'+c7.split('-')[0]+'\t'+c8.split('-')[0]+'\t'+c9.split('-')[0]+'\t'+c10.split('-')[0]+'\n')
Reportprice.close()
os.system('pause')
print('总用时:\t'+str(int(time.time())-int(t))+'s\n')
os.system('pause')




'''































'''
    if dic.has_key(district):
        dic[district] = dic[district] + 1
    else:
        dic[district] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):resultsq.write(i[0]+'\t'+str(i[1])+'\n')
resultsq.close()
























#######################################以下为筛选街道信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(street):
        dic[street] = dic[street] + 1
    else:
        dic[street] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):resultst.write(i[0]+'\t'+str(i[1])+'\n')
resultst.close()

#######################################以下为筛选楼盘小区信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(lp):
        dic[lp] = dic[lp] + 1
    else:
        dic[lp] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):resultlp.write(i[0]+'\t'+str(i[1])+'\n')
resultlp.close()

#######################################以下为筛选经纪公司信息#########################################
dic = {}
for d in data:
    houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
    if dic.has_key(companyName):
        dic[companyName] = dic[companyName] + 1
    else:
        dic[companyName] = 1
for i in sorted(dic.items(),key=lambda e:e[1],reverse=True):resultcmy.write(i[0]+'\t'+str(i[1])+'\n')
resultcmy.close()

#---------------------------------------------------------------下面为提取对应关系------------------------#

#打开并处理商圈，街道，楼盘等信息
districts = open(dateNow+'resultsq.txt').readlines()
streets = open(dateNow+'resultst.txt').readlines()
#companys = open(dateNow+'resultcmy.txt').readlines()
companys = open('company.txt').readlines()
lps = open(dateNow+'resultlp.txt').readlines()

districts = [i.split('\t')[0] for i in districts]
streets = [i.split('\t')[0] for i in streets]
#companys = [i.split('\t')[0] for i in companys][:8]
companys = [i[:-1] for i in companys]
lps = [i.split('\t')[0] for i in lps][:800]

#打开文件，准备写入结果数据
st_sqReport = open(dateNow+'st-sq对应关系.txt','w')
lp_sq_stReport = open(dateNow+'lp_sq_st对应关系.txt','w')
dicDist = {}

for st in streets:
    for d in data:
        houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
        if st == street:
            dicDist[st] = district
            break
for st in streets:
    st_sqReport.write(st+'\t'+dicDist[st]+'\n')
st_sqReport.close()

dicDist = {}

for l in lps:
    for d in data:
        houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
        if l == lp:
            dicDist[l] = district+'\t'+street
            break
for l in lps:
    lp_sq_stReport.write(l+'\t'+dicDist[l]+'\n')
lp_sq_stReport.close()

#--------------------------------------------------下面为处理区域、街道及小区统计信息------------------------#

#打开文件，准备写入结果数据

Reportdist = open(dateNow+'Reportdist.txt','w')
Reportst = open(dateNow+'Reportst.txt','w')
Reportlp = open(dateNow+'Reportlp.txt','w')

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
    Reportdist.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        Reportdist.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    Reportdist.write('\n')
Reportdist.close()
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
    Reportst.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        Reportst.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    Reportst.write('\n')
Reportst.close()
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
    Reportlp.write(l+'\t'+str(dicDist[l][l]['post'])+'\t'+str(dicDist[l][l]['clicks']))
    for company in companys:
        Reportlp.write('\t'+str(float(dicDist[l][company])/tmp*100)[:5]+'%')
    Reportlp.write('\n')
Reportlp.close()

#######################################以下为筛选热门时段信息#########################################
dic = {}
for company in companys:
    resultt = open(dateNow+company+'resultt.txt','w')
    all = 0
    for hour in arrTime:
        dic[hour] = 0
    for d in data:
        houseId,companyName,district,street,lp,clicks,datetime = d.split('\t')
        if companyName.find(company) != -1:
            t = datetime[11:13]
            dic[t] = dic[t] + 1
    a = [int(i) for i in dic.values()]
    all = sum(a)
    for hour in arrTime:
        resultt.write(str(float(dic[hour])/all*100)[:5]+'%\n')
    resultt.close()

#--------------------------------------------------下面为处理室型、价格相关统计信息------------------------#

#打开文件，准备写入结果数据
#rentShiPrice = open(dateNow+'renttmpfile.txt','r').readlines()
resultshi = open(dateNow+'resultshi.txt','w')
resultprice = open(dateNow+'resultprice.txt','w')

dic = {}
for ele in rentShiPrice:
    house_id,shi,price = ele.split('\t')
    dic[house_id] = str(shi) + '\t' + str(price[:-1])

arrTime = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']



#######################################以下为筛选价格和室型信息#########################################

conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")

print conn

dicDist = {}
dicPrice = {}
dicArea = {}

for d in data:
    house_id,companyName,district,street,lp,clicks,datetime = d.split('\t')
    cursor = conn.cursor()
    cursor.execute('select huxing_shi,price from house_source_rent_premier where house_id='+house_id+';')
    for row in cursor.fetchall():
        huxing_shi = row[0]
        price = str(row[1])
    #cursor.close()
    
    if house_id in dic:
        #print house_id,dic[house_id]
        huxing_shi = dic[house_id].split('\t')[0]
        price = dic[house_id].split('\t')[1]
    else:
        huxing_shi = 'null'
        price = 'null'
    
    if huxing_shi in dicDist:
        dicDist[huxing_shi][huxing_shi]['count'] = dicDist[huxing_shi][huxing_shi]['count'] + 1
        dicDist[huxing_shi][huxing_shi]['click'] = dicDist[huxing_shi][huxing_shi]['click'] + int(clicks)
        for company in companys:
            if company == companyName:
                dicDist[huxing_shi][company]['count'] = dicDist[huxing_shi][company]['count'] + 1
                dicDist[huxing_shi][company]['click'] = dicDist[huxing_shi][company]['click'] + int(clicks)
                break
    else:
        dicDist[huxing_shi] = {}
        dicDist[huxing_shi][huxing_shi] = {}
        dicDist[huxing_shi][huxing_shi]['count'] = 1
        dicDist[huxing_shi][huxing_shi]['click'] = int(clicks)
        for company in companys:
            dicDist[huxing_shi][company] = {}
            dicDist[huxing_shi][company]['count'] = 0
            dicDist[huxing_shi][company]['click'] = 0
    if price in dicPrice:
        dicPrice[price][price]['count'] = dicPrice[price][price]['count'] + 1
        dicPrice[price][price]['click'] = dicPrice[price][price]['click'] + int(clicks)
        for company in companys:
            if company == companyName:
                dicPrice[price][company]['count'] = dicPrice[price][company]['count'] + 1
                dicPrice[price][company]['click'] = dicPrice[price][company]['click'] + int(clicks)
                break
    else:
        dicPrice[price] = {}
        dicPrice[price][price] = {}
        dicPrice[price][price]['count'] = 1
        dicPrice[price][price]['click'] = int(clicks)
        for company in companys:
            dicPrice[price][company] = {}
            dicPrice[price][company]['count'] = 0
            dicPrice[price][company]['click'] = 0

for huxing_shi in dicDist:
    resultshi.write(str(huxing_shi)+'\t'+str(dicDist[huxing_shi][huxing_shi]['count'])+'-'+str(dicDist[huxing_shi][huxing_shi]['click']))
    for company in companys:
        resultshi.write('\t'+str(dicDist[huxing_shi][company]['count'])+'-'+str(dicDist[huxing_shi][company]['click']))
    resultshi.write('\n')
resultshi.close()
for price in dicPrice:
    resultprice.write(str(price)+'\t'+str(dicPrice[price][price]['count'])+'-'+str(dicPrice[price][price]['click']))
    for company in companys:
        resultprice.write('\t'+str(dicPrice[price][company]['count'])+'-'+str(dicPrice[price][company]['click']))
    resultprice.write('\n')
resultprice.close()

#######################################以下为价格和室型信息的后续处理#########################################

resultshi = open(dateNow+'resultshi.txt').readlines()
resultprice = open(dateNow+'resultprice.txt').readlines()
Reportshi = open(dateNow+'ReportShi.txt','w')
Reportprice = open(dateNow+'ReportPrice.txt','w')
for shi in resultshi:
    s,allCount,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = shi.split('\t')
    Reportshi.write(s+'\t'+allCount.split('-')[0]+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[0]+'\t'+c2.split('-')[0]+'\t'+c3.split('-')[0]+'\t'+c4.split('-')[0]+'\t'+c5.split('-')[0]+'\t'+c6.split('-')[0]+'\t'+c7.split('-')[0]+'\t'+c8.split('-')[0]+'\t'+c9.split('-')[0]+'\t'+c10.split('-')[0]+'\n')
Reportshi.close()
for price in resultprice:
    p,allCount,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = price.split('\t')
    Reportprice.write(p+'\t'+allCount.split('-')[0]+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[0]+'\t'+c2.split('-')[0]+'\t'+c3.split('-')[0]+'\t'+c4.split('-')[0]+'\t'+c5.split('-')[0]+'\t'+c6.split('-')[0]+'\t'+c7.split('-')[0]+'\t'+c8.split('-')[0]+'\t'+c9.split('-')[0]+'\t'+c10.split('-')[0]+'\n')
Reportprice.close()
os.system('pause')
print('总用时:\t'+str(int(time.time())-int(t))+'s\n')
os.system('pause')

'''