# coding: gbk
import os
import MySQLdb
data = open('houseId.txt').readlines()
result = open('result.txt','w')

dic = {}

conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="gbk")

#######################################以下为筛选商圈信息#########################################
countIdNull = 0
xiaoqu_id = 0
xiaoqu = ''
for houseId in data:
    cursor = conn.cursor()
    cursor.execute("select xiaoqu_id,concat(district_name,'-',street_name,'-',xiaoqu) As xiaoqu from house_source_rent_premier where house_id="+houseId+";")
    for row in cursor.fetchall():
        xiaoqu_id = row[0]
        xiaoqu = row[1]
        #result.write( xiaoqu_id +'\t'+row[1] + '\n')
    cursor.close()
    if 0 == xiaoqu_id:
        countIdNull = countIdNull + 1
print(countIdNull,len(data),float(countIdNull)/len(data)*100)

result.close()
os.system('pause')
