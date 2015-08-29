#coding:utf-8
import GJDB

db = GJDB.GJDB()
db.rp()
db.selectDB('house_report')
#dts = []
dts = ['2013_01','2013_02','2013_03','2013_04','2013_05','2013_06','2013_07','2013_08','2013_09','2013_10','2013_11','2013_12','2014_01','2014_02','2014_03']

result1 = open('result1.txt','w')
result2 = open('result2.txt','w')

for dt in dts:
    print dt
    sql1 = 'SELECT FROM_UNIXTIME(ReportDate), SUM(ClickCount) ,SUM(HouseCount) FROM house_account_generalstat_report_' + dt + ' WHERE CountType IN (1,3) GROUP BY ReportDate;'
    sql2 = 'SELECT FROM_UNIXTIME(ReportDate), HouseType, SUM(ClickCount) ,SUM(HouseCount) FROM house_account_generalstat_report_' + dt + ' WHERE CountType IN (1,3) AND housetype IN (1,3,5) GROUP BY ReportDate,HouseType'
    data1 = db.selectData(sql1)
    data2 = db.selectData(sql2)
    for row in  data1:
        result1.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\n')
    for row in  data2:
        result2.write(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\n')