from mySQLClass import MySQLClass

cur = MySQLClass('lixueshi','192.168.116.20','i14p4Dkyd',3320)
cur.connectDB()
cur.selectDB('house_premier')
sql = "SELECT city,AVG(price),COUNT(1) FROM house_premier.house_source_rent_premier WHERE city IN (300,900,2600,2500,2300) AND post_at>= UNIX_TIMESTAMP('2013-06-01') GROUP BY city;"
result = cur.selectData(sql)

for r in result:
    print r