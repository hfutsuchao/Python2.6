# coding: utf-8
import os,MySQLdb,time
t= time.time()
dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))
data = open('C:\\Users\\suchao\\Desktop\\allpremier.txt').readlines()

resultAccountIds = open(dateNow+'accountIds.txt','w')
resultCompanyNames = open(dateNow+'CompanyNames.txt','w')
resultCustomerNames = open(dateNow+'CustomerNames.txt','w')
resultDistricts = open(dateNow+'Districts.txt','w')
resultStreets = open(dateNow+'Streets.txt','w')
resultCategoryNames = open(dateNow+'CategoryNames.txt','w')

'''conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="gcrm",charset="utf8")
cursor = conn.cursor()
    
accountIds = {}
for d in data:
    accountId,companyName,district,street,lp,clicks,datetime,reportdate = d.split('\t')
    if accountId not in accountIds:
        sql = 'SELECT ca.accountName, c.CompanyName, c.FullName, ca.CellPhone, FROM_UNIXTIME(ca.PremierExpire)  FROM customer_account ca INNER JOIN customer c ON ca.CustomerId=c.CustomerId WHERE accountId='+accountId+' LIMIT 1'
        cursor.execute(sql)
        for row in cursor.fetchall():
            accountName = row[0]
            companyName = row[1]
            FullName = row[2]
            CellPhone = row[3]
            PremierExpire = row[4]
        accountIds[accountId] = accountName+'\t'+companyName+'\t'+FullName+'\t'+str(CellPhone)+'\t'+str(PremierExpire)
'''
accountIds = {}
companyNames = {}
customerNames = {}
districts = {}
streets = {}
categoryNames = {}
peoples = {}
'''for date in range(1,19):
    if len(date) == 1:
        date = '0' + str(date)
    accountIds['2012-09-'+date+' 00:00:00'] = {}
'''
for d in data[:10]:
    houseId,accountId,companyName,customerName,district,street,xiaoqu,categoryName,clicks,reportdate = d.split('\t')
    if accountIds.has_key(accountId):
        accountIds[accountId] = accountIds[accountId] + int(clicks)
    else:
        accountIds[accountId] = int(clicks)
    for key in peoples:
        if accountId not in peoples[key].values():
            peoples[key][customerName] = accountId
    if companyNames.has_key(companyName):
        companyNames[companyName] = companyNames[companyName] + int(clicks)
    else:
        companyNames[companyName] = int(clicks)
    if customerNames.has_key(customerName):
        customerNames[customerName] = customerNames[customerName] + int(clicks)
        if accountId not in peoples.values():
            peoples['customerNames'][customerName] = accountId
    else:
        customerNames[customerName] = int(clicks)
    if districts.has_key(district):
        districts[district] = districts[district] + int(clicks)
    else:
        districts[district] = int(clicks)
    if streets.has_key(street):
        streets[street] = streets[street] + int(clicks)
    else:
        streets[street] = int(clicks)
    if categoryNames.has_key(categoryName):
        categoryNames[categoryName] = categoryNames[categoryName] + int(clicks)
    else:
        categoryNames[categoryName] = int(clicks)
for i in sorted(accountIds.items(),key=lambda e:e[1],reverse=True):resultAccountIds.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')
for i in sorted(companyNames.items(),key=lambda e:e[1],reverse=True):resultCompanyNames.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')
for i in sorted(customerNames.items(),key=lambda e:e[1],reverse=True):resultCustomerNames.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')
for i in sorted(districts.items(),key=lambda e:e[1],reverse=True):resultDistricts.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')
for i in sorted(streets.items(),key=lambda e:e[1],reverse=True):resultStreets.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')
for i in sorted(categoryNames.items(),key=lambda e:e[1],reverse=True):resultCategoryNames.write(str(i[0])+'\t'+str(i[1])+'\t'+str(float(i[1])/7)[:str(float(i[1])/7).find('.')+3]+'\n')