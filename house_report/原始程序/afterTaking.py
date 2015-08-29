import time

dateNow = time.strftime('%Y-%m-%d',time.localtime(time.time()))

'''
resultshi = open(dateNow+'resultshi.txt').readlines()
resultprice = open(dateNow+'resultprice.txt').readlines()
allshi = open('allShi.txt','w')
allprice = open('allPrice.txt','w')
for shi in resultshi:
    s,allCount,c1,c2,c3,c4,c5,c6,c7,c8 = shi.split('\t')
    allshi.write(s+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[1]+'\t'+c2.split('-')[1]+'\t'+c3.split('-')[1]+'\t'+c4.split('-')[1]+'\t'+c5.split('-')[1]+'\t'+c6.split('-')[1]+'\t'+c7.split('-')[1]+'\t'+c8.split('-')[1])

for price in resultprice:
    p,allCount,c1,c2,c3,c4,c5,c6,c7,c8 = price.split('\t')
    allprice.write(p+'\t'+allCount.split('-')[1]+'\t'+c1.split('-')[1]+'\t'+c2.split('-')[1]+'\t'+c3.split('-')[1]+'\t'+c4.split('-')[1]+'\t'+c5.split('-')[1]+'\t'+c6.split('-')[1]+'\t'+c7.split('-')[1]+'\t'+c8.split('-')[1])

'''

resultshi = open(dateNow+'shiresult.txt').readlines()
resultprice = open(dateNow+'priceresult.txt').readlines()
Reportshi = open(dateNow+'ReportShi.txt','w')
Reportprice = open(dateNow+'ReportPrice.txt','w')
for shi in resultshi:
    s,allCount,c1,c2,c3,c4,c5,c6,c7,c8 = shi.split('\t')
    Reportshi.write(s+'\t'+allCount+'\t'+c1.split('-')[1]+'\t'+c2.split('-')[1]+'\t'+c3.split('-')[1]+'\t'+c4.split('-')[1]+'\t'+c5.split('-')[1]+'\t'+c6.split('-')[1]+'\t'+c7.split('-')[1]+'\t'+c8.split('-')[1])
Reportshi.close()
for price in resultprice:
    p,allCount,c1,c2,c3,c4,c5,c6,c7,c8 = price.split('\t')
    Reportprice.write(p+'\t'+allCount+'\t'+c1.split('-')[1]+'\t'+c2.split('-')[1]+'\t'+c3.split('-')[1]+'\t'+c4.split('-')[1]+'\t'+c5.split('-')[1]+'\t'+c6.split('-')[1]+'\t'+c7.split('-')[1]+'\t'+c8.split('-')[1])
Reportprice.close()
