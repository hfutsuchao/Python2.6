#coding: gbk
import os,MySQLdb,time
dianji = open('C:\\Users\\suchao\\Desktop\\dianji.log','r').readlines()
xianshi = open('C:\\Users\\suchao\\Desktop\\xianshi.log','r').readlines()

datetime = ['2012-11-08','2012-11-09','2012-11-10','2012-11-11','2012-11-12','2012-11-13']
'''
resultFang1Dianji = open('resultFang1Dianji.txt','w')
resultFang3Dianji = open('resultFang3Dianji.txt','w')
resultFang5Dianji = open('resultFang5Dianji.txt','w')

resultFang1Xianshi = open('resultFang1Xianshi.txt','w')
resultFang3Xianshi = open('resultFang3Xianshi.txt','w')
resultFang5Xianshi = open('resultFang5Xianshi.txt','w')
'''
resultCityClickDuankou = open('resultCityClickDuankou.txt','w')
resultCityClickMianfei = open('resultCityClickMianfei.txt','w')
resultCityXianshiDuankou = open('resultCityXianshiDuankou.txt','w')
resultCityXianshiMianfei = open('resultCityXianshiMianfei.txt','w')

fourCities = ['bj','sh','gz','sz']

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
            sql = 'SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,pay_type 付款方式,house_type 主次卧类型 ,huxing_shi 室,huxing_ting 厅,huxing_wei 卫,peizhi 房屋配置 FROM house_source_share WHERE puid='+houseId+';'
        elif category == 'fang5':
            sql = 'SELECT district_name 区域, street_name 街道, title 标题, image_count 图片数, price 价格, xiaoqu 小区名称,fang_xing 房屋类型,AREA 面积,chaoxiang 朝向,zhuangxiu 装修情况,huxing_shi 室,huxing_ting 厅,huxing_wei 卫 FROM house_source_sell WHERE puid='+houseId+';'
        else:
            return '类别错误'
    else:
        return "参数传入错误！传入：类别，房源ＩＤ"
    return sql

citys = {}

cityChange={}

conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="management",charset="gbk")
cursor = conn.cursor()
cursor.execute('SELECT domain,pinyin FROM city;')
for row in cursor.fetchall():
    cityChange[row[0]]=row[1]
cursor.close()


for d in dianji:
    date,agent,tuiguang,url,times = d.split('\t')
    #获取城市和类型以及房源ID
    city = url[url.find('//')+2:url.find('.')]
    category = url[url.find('/fang')+1:url.find('/fang')+6]
    if url == '-':
        house_id = '0'
    elif url.find('tuiguang-') != -1:
        house_id = url.split('tuiguang-')[1]
        house_id = house_id[:house_id.find('.htm')]
    else:
        try:
            house_id = url.split('/fang')[1]
            if house_id.find('x.htm') != -1:
                house_id = house_id[2:house_id.find('x.htm')]
            else:
                house_id = 0
        except:
            house_id = 0
    if city in fourCities:
        if tuiguang == 'tuiguang=1':
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")
                sql = getSql(category,house_id,'zhongjie')
            except:
                print 'sqlerror77',d
                continue
            cursor = conn.cursor()
            cursor.execute(sql)
        elif tuiguang == 'tuiguang=0':
            city = cityChange[city]
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")
                sql = getSql(category,house_id,'mianfei')
            except:
                try:
                    conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
                    sql = getSql(category,house_id,'mianfei')
                except:
                    try:
                        conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
                        sql = getSql(category,house_id,'mianfei')
                    except:
                        print 'sqlerror95',d
                        continue
            cursor = conn.cursor()
            cursor.execute(sql)
        for row in cursor.fetchall():
            if tuiguang == 'tuiguang=1':
                resultCityClickDuankou.write(date+'\t'+city+'\t'+category+'\t'+agent+'_'+tuiguang+'\t'+house_id+'\t'+times[:-1])
                for i in row:
                    resultCityClickDuankou.write('\t'+str(i))
                resultCityClickDuankou.write('\n')
            else:
                resultCityClickMianfei.write(date+'\t'+city+'\t'+category+'\t'+agent+'_'+tuiguang+'\t'+house_id+'\t'+times[:-1])
                for i in row:
                    resultCityClickMianfei.write('\t'+str(i))
                resultCityClickMianfei.write('\n')
resultCityClickMianfei.close()
resultCityClickDuankou.close()

'''
citys = {}

for x in xianshi:
    date,agent,tuiguang,url,times = x.split('\t')
    city = url[url.find('//')+2:url.find('.')]
    category = url[url.find('/fang')+1:url.find('/fang')+6]
    if url == '-':
        house_id = '0'
    elif url.find('tuiguang-') != -1:
        house_id = url.split('tuiguang-')[1]
        house_id = house_id[:house_id.find('.htm')]
    else:
        try:
            house_id = url.split('/fang')[1]
            if house_id.find('x.htm') != -1:
                house_id = house_id[2:house_id.find('x.htm')]
            else:
                house_id = 0
        except:
            house_id = 0
    if city in fourCities:
        if tuiguang == 'tuiguang=1':
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")
                sql = getSql(category,house_id,'zhongjie')
            except:
                print 'sqlerror165',x
                continue
            cursor = conn.cursor()
            cursor.execute(sql)
        elif tuiguang == 'tuiguang=0':
            city = cityChange[city]
            try:
                conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")
                sql = getSql(category,house_id,'mianfei')
            except:
                try:
                    conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
                    sql = getSql(category,house_id,'mianfei')
                except:
                    try:
                        conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="others",charset="gbk")
                        sql = getSql(category,house_id,'mianfei')
                    except:
                        print 'sqlerror183',x
                        continue
            cursor = conn.cursor()
            cursor.execute(sql)
        for row in cursor.fetchall():
            if tuiguang == 'tuiguang=1':
                resultCityXianshiDuankou.write(date+'\t'+city+'\t'+category+'\t'+agent+'_'+tuiguang+'\t'+house_id+'\t'+times[:-1])
                for i in row:
                    resultCityXianshiDuankou.write('\t'+str(i))
                resultCityXianshiDuankou.write('\n')
            else:
                resultCityXianshiMianfei.write(date+'\t'+city+'\t'+category+'\t'+agent+'_'+tuiguang+'\t'+house_id+'\t'+times[:-1])
                for i in row:
                    resultCityXianshiMianfei.write('\t'+str(i))
                resultCityXianshiMianfei.write('\n')
resultCityXianshiDuankou.close()
resultCityXianshiMianfei.close()
'''