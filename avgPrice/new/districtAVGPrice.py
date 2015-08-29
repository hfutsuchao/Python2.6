# coding: gbk
import os,MySQLdb,time

citys = {'beijing':'北京','shanghai':'上海','shenzhen':'深圳','guangzhou':'广州','xian':'西安','shenyang':'沈阳','jinan':'济南','dalian':'大连','hangzhou':'杭州','zhengzhou':'郑州','xiamen':'厦门','nanjing':'南京','wuhan':'武汉','suzhou':'苏州','kunming':'昆明','chongqing':'重庆','tianjin':'天津','chengdou':'成都','qingdao':'青岛','hefei':'合肥','fuzhou':'福州','shijiazhuang':'石家庄'}

resultRent = open('rent.txt','w')
resultShare = open('share.txt','w')

#rent AVG_price
for city in citys.keys():
    conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="GBK")
    #sql = "SELECT district_name,street_name,huxing_shi,AVG(price),COUNT(1) hs FROM house_source_rent WHERE post_at>=UNIX_TIMESTAMP('2013-9-29') AND huxing_shi<=3 AND huxing_shi>=1 GROUP BY district_name,street_name,huxing_shi HAVING hs>=3"
    sql = "SELECT huxing_shi,AVG(price),COUNT(1) hs FROM house_source_rent WHERE post_at>=UNIX_TIMESTAMP('2013-11-1') AND huxing_shi<=3 AND huxing_shi>=1 GROUP BY huxing_shi HAVING hs>=3"
    cursor = conn.cursor()
    cursor.execute(sql)
    for rows in cursor.fetchall():
        try:
            #resultRent.write(citys[city] + '\t' + rows[0] + '\t' + rows[1] + '\t' + str(rows[2]) + '\t' + str(int(rows[3])) + '\t' + str(rows[4]) + '\n')
            resultRent.write(citys[city] + '\t' + str(rows[0]) + '\t' + str(rows[1]) + '\t' + str(rows[2]) + '\n')
        except Exception, e:
            print e, rows
    cursor.close()
    conn.close()

#share AVG_price
for city in citys.keys():
    conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="GBK")
    #sql = "SELECT district_name,street_name,AVG(price),count(1) hs FROM house_source_share WHERE post_at>=UNIX_TIMESTAMP('2013-9-29') GROUP BY district_name,street_name having hs>=3"
    sql = "SELECT AVG(price),count(1) hs FROM house_source_share WHERE post_at>=UNIX_TIMESTAMP('2013-11-1') having hs>=3"
    cursor = conn.cursor()
    cursor.execute(sql)
    for rows in cursor.fetchall():
        try:
            #resultShare.write(citys[city] + '\t' + rows[0] + '\t' + rows[1] + '\t' + str(int(rows[2])) + '\t' + str(rows[3]) + '\n')
            resultShare.write(citys[city] + '\t' + str(rows[0]) + '\t' + str(rows[1]) + '\n')
        except Exception, e:
            print e, rows
    cursor.close()
    conn.close()

citys = {'0':'北京','100':'上海','401':'深圳','400':'广州','2300':'西安','800':'沈阳','1500':'济南','801':'大连','600':'杭州','1200':'郑州','1001':'厦门','900':'南京','2500':'武汉','901':'苏州','2800':'昆明','300':'重庆','200':'天津','500':'成都','1501':'青岛','1600':'合肥','1000':'福州','1100':'石家庄'}

conn=MySQLdb.connect(host="192.168.116.20",user="suchao",passwd="CE7w7pTNB",port=3328,db="house_premier",charset="GBK")

resulttgRent = open('tg_rent.txt','w')
resulttgShare = open('tg_share.txt','w')

#rent AVG_price
for city in citys.keys():
    #sql = "SELECT district_name,street_name,huxing_shi,AVG(price),COUNT(1) hs FROM house_source_rent_premier WHERE city=" + city + " and post_at>=UNIX_TIMESTAMP('2013-9-29') AND huxing_shi<=3 AND huxing_shi>=1 GROUP BY district_name,street_name,huxing_shi HAVING hs>=3"
    sql = "SELECT huxing_shi,AVG(price),COUNT(1) hs FROM house_source_rent_premier WHERE city=" + city + " and post_at>=UNIX_TIMESTAMP('2013-11-1') AND huxing_shi<=3 AND huxing_shi>=1 GROUP BY huxing_shi HAVING hs>=3"
    #print sql
    cursor = conn.cursor()
    cursor.execute(sql)
    for rows in cursor.fetchall():
        try:
            #resulttgRent.write(citys[city] + '\t' + rows[0] + '\t' + rows[1] + '\t' + str(rows[2]) + '\t' + str(int(rows[3])) + '\t' + str(rows[4]) + '\n')
            resulttgRent.write(citys[city] + '\t' + str(rows[0]) + '\t' + str(rows[1]) + '\t' + str(rows[2]) + '\n')
        except Exception, e:
            print e, rows

#share AVG_price
for city in citys.keys():
    #sql = "SELECT district_name,street_name,AVG(price),count(1) hs FROM house_source_share_premier WHERE city=" + city + " and post_at>=UNIX_TIMESTAMP('2013-9-29') GROUP BY district_name,street_name having hs>=3"
    sql = "SELECT AVG(price),count(1) hs FROM house_source_share_premier WHERE city=" + city + " and post_at>=UNIX_TIMESTAMP('2013-11-1') having hs>=3"
    #print sql
    cursor = conn.cursor()
    cursor.execute(sql)
    for rows in cursor.fetchall():
        try:
            #resulttgShare.write(citys[city] + '\t' + rows[0] + '\t' + rows[1] + '\t' + str(int(rows[2])) + '\t' + str(rows[3]) + '\n')
            resulttgShare.write(citys[city] + '\t' + str(rows[0]) + '\t' + str(rows[1]) + '\n')
        except Exception, e:
            print e, rows
