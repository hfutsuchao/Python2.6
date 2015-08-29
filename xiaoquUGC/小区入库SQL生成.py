#coding:utf-8
import GJDB
import sys
db = GJDB.GJDB()
db.crawl()
db.selectDB('crawler_ds')
db.selectData('set names utf8;')
#sys.exit()
xqxxs = open('C:/users/suchao/desktop/bsgscxq.txt','r').readlines()
tmpFile = open('tmpFilexq.txt','w')
for xqxx in xqxxs:
    name, source, url  = xqxx.split('\t')
    sql = "SELECT city,district,developer,community,'','',prop_company,prop_fee,plot_ratio,gree_coverage,'',building_year,address FROM crawler_house_xiaoqu WHERE claw_date='20131230' AND city IN ('北京','广州','深圳','上海') AND community='"+name+"' AND url='"+url[:-1]+"';"
    print sql
    result = db.selectData(sql)
    if len(result) >=1:
        result = '\t'.join(list(db.selectData(sql)[0]))
        tmpFile.write(result+'\n')