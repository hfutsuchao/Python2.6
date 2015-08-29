# coding: gbk
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#data = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\fufei_zhongjie_short_20121108.log').readlines()
geren = open('geren.txt','w')
jjr = open('jjr.txt','w')

def getSql(category,datetime,type):
    if type == 'jjr':
        if category == 'fang1':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_rent WHERE agent=1 and source_type = 0 and listing_status >=5 and show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        elif category == 'fang3':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_share WHERE agent=1 and source_type = 0  and listing_status >=5 and  show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        elif category == 'fang5':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_sell WHERE agent=1 and source_type = 0  and listing_status >=5 and  show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        else:
            return '类别错误'
    elif type == 'geren':
        if category == 'fang1':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_rent WHERE agent=0 and source_type = 0  and listing_status >=5 and show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        elif category == 'fang3':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_share WHERE agent=0 and source_type = 0  and listing_status >=5 and  show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        elif category == 'fang5':
            sql = 'SELECT distinct cookie_id,count(1) FROM house_source_sell WHERE agent=0 and source_type = 0  and listing_status >=5 and  show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
        else:
            return '类别错误'
    else:
        return "参数传入错误！传入：类别，日期，发帖人身份：jjr或者geren"
    return sql

#城市对应关系的统计
categorys=['fang1','fang3','fang5']

citys={}

conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db="management",charset="gbk")
cursor = conn.cursor()
cursor.execute('SELECT domain,pinyin FROM city;')
for row in cursor.fetchall():
    citys[row[0]]=row[1]
cursor.close()
citys['others']='others'

#免费贴点击部分的统计
for domain in citys:
    city = citys[domain]
    try:
        conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3310,db=city,charset="gbk")
        cursor=conn.cursor()
        for category in categorys:
            #print category
            sqlGeren = getSql(category,'2012-11-12',"geren")
            sqlJjr = getSql(category,'2012-11-12',"jjr")
            #print sqlJjr
            #print sqlGeren
            cursor.execute(sqlGeren)
            for row in cursor.fetchall():
                #resultClickGeren.write(houseId+'\t'+houseIdClick[houseId])
                geren.write(category+'\t'+city+'\t'+'免费个人'+'\t'+str(row[1])+'\n')
                #resultClickGeren.write('\n')
            cursor.execute(sqlJjr)
            for row in cursor.fetchall():
                #resultClickGeren.write(houseId+'\t'+houseIdClick[houseId])
                jjr.write(category+'\t'+city+'\t'+'免费经纪人'+'\t'+str(row[1])+'\n')
                #resultClickGeren.write('\n')
    except:
        print city,'error'