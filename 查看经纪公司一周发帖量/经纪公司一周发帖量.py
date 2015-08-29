#coding: gbk
import os,MySQLdb,time

#fields = ['house_premier.house_source_rent_premier','house_premier.house_source_share_premier','house_premier.house_source_sell_premier','house_premier.house_source_officerent_premier','house_premier.house_source_officetrade_premier','house_premier.house_source_plant_premier','house_premier.house_source_loupan_premier','house_premier.house_source_storerent_premier','house_premier.house_source_storetrade_premier']
fields = ['house_premier.house_source_rent_premier','house_premier.house_source_share_premier','house_premier.house_source_sell_premier']

date = {}
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")
cursor = conn.cursor()
for field in fields:
    cursor.execute('SELECT SUBSTR(FROM_UNIXTIME(post_at),1,10) 日期,COUNT(1) 发布帖子数 FROM '+field+' WHERE post_at>=UNIX_TIMESTAMP("2012-11-15") AND account_id IN (SELECT AccountId FROM gcrm.customer JOIN gcrm.customer_account USING(CustomerId) WHERE CompanyName = "上海中原房地产经纪有限公司") GROUP BY 日期;')
    for row in cursor.fetchall():
        if row[0] in date:
            date[row[0]] = date[row[0]] + row[1]
        else:
            date[row[0]] = row[1]
cursor.close()

for d in date:
    print d,date[d]