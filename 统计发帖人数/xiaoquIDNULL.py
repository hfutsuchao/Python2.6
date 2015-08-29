# coding: gbk
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#data = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\fufei_zhongjie_short_20121108.log').readlines()
geren = open('null.txt','w')
#jjr = open('all.txt','w')

def getSql(category,datetime,type):
    if type == 'null':
        sql = 'SELECT city,count(1) FROM '+category+' WHERE listing_status =5 and show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400 and xiaoqu_id=0 group by city;'
    elif type == 'all':
        sql = 'SELECT city,count(1) FROM '+category+' WHERE listing_status =5 and show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400 group by city;'
    else:
        return "参数传入错误！传入：类别，日期，发帖人身份：null或者all"
    return sql

#城市对应关系的统计
categorys=["house_source_rent","house_source_sell","house_source_share","house_source_loupan"]

citys={}

conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3311,db="management",charset="gbk")
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
    except:
        continue
    #try:
    cursor=conn.cursor()
    for category in categorys:
        #print category
        sqlGeren = getSql(category,'2013-12-18',"null")
        #sqlGeren = getSql(category,'2013-06-17',"geren")
        #sqlJjr = getSql(category,'2013-06-17',"jjr")
        #print sqlJjr
        #print sqlGeren
        cursor.execute(sqlGeren)
        for row in cursor.fetchall():
            #resultClickGeren.write(houseId+'\t'+houseIdClick[houseId])
            geren.write(category+'\t'+str(row[0])+'\t'+'null'+'\t'+str(row[1])+'\n')
            #resultClickGeren.write('\n')
        '''cursor.execute(sqlJjr)
        for row in cursor.fetchall():
            #resultClickGeren.write(houseId+'\t'+houseIdClick[houseId])
            jjr.write(category+'\t'+str(row[0])+'\t'+'免费经纪人'+'\t'+str(row[1])+'\n')'''
            #resultClickGeren.write('\n')
    #except:
        #print city,'error'