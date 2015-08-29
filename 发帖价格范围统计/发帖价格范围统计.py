# coding: gbk
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#data = open('C:\\Users\\suchao\\Desktop\\phone_20121108\\fufei_zhongjie_short_20121108.log').readlines()
result = open('result.txt','w')

dic = {}

def getSql(category,datetime):
    sql = 'SELECT listing_status,agent,price FROM '+category+' WHERE show_time between unix_timestamp("'+datetime+'") and unix_timestamp("'+datetime+'")+86400;'
    return sql

#城市对应关系的统计
categorys=["house_source_rent","house_source_sell","house_source_share","house_source_shortrent","house_source_storerent","house_source_storetrade","house_source_wantbuy","house_source_wantrent","house_source_plant","house_source_officetrade","house_source_officerent","house_source_loupan"]

for cat in categorys:
    dic[cat] = {}
    dic[cat]["agent0"] = {}
    dic[cat]["agent1"] = {}
    dic[cat]["agent2"] = {}

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
        sql = getSql(category,'2013-06-10')
        #print sqlJjr
        #print sqlGeren
        cursor.execute(sql)
        for row in cursor.fetchall():
            listing_status,agent,price = row
            agent = str(agent)
            price = str(price)
            listing_status = str(listing_status)
            if listing_status not in dic[category]["agent"+agent]:
                dic[category]["agent"+agent][listing_status] = {}
                dic[category]["agent"+agent][listing_status][price] = 1
            elif price not in dic[category]["agent"+agent][listing_status]:
                dic[category]["agent"+agent][listing_status][price] = 1
            else:
                dic[category]["agent"+agent][listing_status][price] = dic[category]["agent"+agent][listing_status][price] + 1
for category in dic:
    for agent in dic[category]:
        for listing_status in dic[category][agent]:
            for price in dic[category][agent][listing_status]:
                result.write(category+'\t'+agent+'\t'+listing_status+'\t'+price+'\t'+str(dic[category][agent][listing_status][price])+'\n')
