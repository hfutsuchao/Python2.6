# -*- coding: cp936-*-
import MySQLdb
import datetime
import urllib
import re
from datetime import datetime,timedelta


# 建立一个连结
Con = MySQLdb.connect(host="192.168.116.20", port=3380,   user= "lixueshi", passwd= "i14p4Dkyd", db= "house_report")
# 生成一个cursor, 用来执行sql语句
Cursor = Con.cursor( )

def init():
    # 建立一个连结
    global Cursor,companylist,hzyfdic
    
    #每次清空 临时文件夹
    sql = 'DELETE FROM koubeitemp'
    #print sql
    Cursor.execute(sql)
    
    #每次先清空当天的口碑,然后再往里录入新口碑
    sql = 'DELETE FROM koubei where date="'+str(datetime.today())[:10]+'"'
    Cursor.execute(sql)
    
    
    #把wrapper放到列表里
    sql = 'SELECT DISTINCT(company) FROM wrapperCompany'
    #print sql
    Cursor.execute(sql)
    Results = Cursor.fetchall( )
    
    for r in Results:
        m = r[0].decode('utf-8').encode('cp936')
        companylist.append(m)
        
    #把wrapper放到列表里
    sql = 'SELECT * FROM koubei_hzyf'
    #INSERT INTO koubei_hzyf (company,months) VALUES ('天泰航空',13)
    #sql = 'insert into koubei_hzyf (company,months) VALUES ("天泰航空",12)'
    #print sql
    Cursor.execute(sql)
    Results = Cursor.fetchall( )

    for r in Results:
        m = r[0].decode('utf-8').encode('cp936')
        #print m,r[1]
        hzyfdic[m] = r[1]



    

                                    
def main():
    global Cursor
    
    sql = "SELECT * FROM house_company_report_2012_07 LIMIT 10;"
    Cursor.execute(sql)

    # Fetch all results from the cursor into a sequence and close the connection
    # 取得返回的值并关闭连接
    Results = Cursor.fetchall( )
    
    for r in Results:
        print r
    

if __name__ == '__main__':
    main()
    

