# -*- coding: utf-8 -*-
# 统计几天内CPC总消费额度
import time, MySQLdb, os
from pychartdir import *

result = open('result.txt','w')

#conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3810,db="house_cpc",charset="utf8")
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3810,db="house_cpc",charset="utf8")
for houseType in arr:
    sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\') AND click_time<='+str(timeNow)+' GROUP BY 点击时间 ;'
    #连接
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        sum = sum + row[1]
result.write(dateNow+'\t'+str(sum)+'\n')

result.close()
#关闭
conn.close()