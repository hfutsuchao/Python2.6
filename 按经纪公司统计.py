# -*- coding: utf-8 -*-
# 统计几天内CPC总消费额度
import time, MySQLdb, os
from pychartdir import *

result = open('result.txt','w')

#频道类型
arr = [1,3,5,6,7,8,9]
dic = {}
sum = 0
timeNow = int(time.time())
dateNow = time.strftime('%Y-%m-%d',time.localtime(timeNow))
dayNow = time.strftime('%H:%M:%S',time.localtime(timeNow))
day = dateNow[8:10]
month = dateNow[5:7]
year = dateNow[0:4]
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3810,db="house_cpc",charset="utf8")
conn2=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="gcrm",charset="utf8")
cursor = conn.cursor()
cursor2 = conn2.cursor()
for houseType in arr:
    #sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\') AND click_time<='+str(timeNow)+' GROUP BY 点击时间 ;'
    #连接
    sql='SELECT location_type, SUBSTR(FROM_UNIXTIME(click_time), 9, 2), account_id, COUNT(1), AVG(cpc_price), SUM(real_price) FROM house_click_record_12_'+str(houseType)+' WHERE STATUS=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\') - '+str(86400*7)+' AND click_time<=UNIX_TIMESTAMP(\''+dateNow+'\') GROUP BY location_type, SUBSTR(FROM_UNIXTIME(click_time), 9, 2),account_id'
    #print sql
    cursor.execute(sql)
    for row in cursor.fetchall():
        account_id = row[2]
        sqlGetInfo='SELECT c.CompanyName FROM customer_account ca INNER JOIN  customer c ON ca.CustomerId=c.CustomerId WHERE ca.accountid ='+str(account_id)
        cursor2.execute(sqlGetInfo)
        for row2 in cursor2.fetchall():
            companyName = row2[0]+'_'+str(row[1])+'_'+str(row[0])
        if companyName in dic:
            dic[companyName]['real_price'] = dic[companyName]['real_price'] + row[5]
            dic[companyName]['clicks'] = dic[companyName]['clicks'] + row[3]
        else:
            dic[companyName] = {}
            dic[companyName]['real_price'] = row[5]
            #print companyName,dic[companyName]['real_price'],row[5]
            dic[companyName]['clicks'] = row[3]
            #print dic[companyName]['clicks']
for ele in dic:
    result.write(ele+'\t'+str(dic[ele]['clicks'])+'\t'+str(dic[ele]['real_price'])+'\n')
result.close()