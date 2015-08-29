#coding:utf-8
import GJDB

db = GJDB.GJDB()
db.rp()
db.selectDB('house_report')
#dts = []
dts = ['2013_01','2013_02','2013_03','2014_01','2014_02','2014_03']

result1 = open('result1.txt','w')
result2 = open('result2.txt','w')

for dt in dts:
    print dt
    sql1 = 'SELECT AccountCityId, FROM_UNIXTIME(ReportDate), SUM(ClickCount) ,SUM(HouseCount) FROM house_account_generalstat_report_' + dt + ' WHERE AccountCityId IN (0,100,401,400,800,801,1300,1400,1900,900,901,903,902,1000,1001,600,601,300,2800,500,402,2600,1800,1700,2500,2505,1200,1600,1501,1506,1502,1500,1507,1503,1513,200,2900,2200,2000,1100,2300,2100)  AND CountType IN (1,3) GROUP BY AccountCityId, ReportDate;'
    sql2 = 'SELECT AccountCityId, FROM_UNIXTIME(ReportDate), HouseType, SUM(ClickCount) ,SUM(HouseCount) FROM house_account_generalstat_report_' + dt + ' WHERE AccountCityId IN (0,100,401,400,800,801,1300,1400,1900,900,901,903,902,1000,1001,600,601,300,2800,500,402,2600,1800,1700,2500,2505,1200,1600,1501,1506,1502,1500,1507,1503,1513,200,2900,2200,2000,1100,2300,2100) AND  CountType IN (1,3) AND housetype IN (1,3,5) GROUP BY AccountCityId,ReportDate,HouseType;'
    data1 = db.selectData(sql1)
    data2 = db.selectData(sql2)
    for row in  data1:
        result1.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\n')
    for row in  data2:
        result2.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3])  + '\t' + str(row[4]) + '\n')