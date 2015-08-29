#encoding:utf-8
import json
import html
import time

idFile = open('ids.txt','r').readlines()

result = open('result.txt','w')

def isFree(ids):
    import GJDB
    DB = GJDB.GJDB()
    DB.gcrm()
    DB.selectDB('gcrm')
    DB.selectData('set names utf8')
    return DB.selectData('SELECT accountid FROM customer_account WHERE accountid IN (' + str(ids) + ') AND premierExpire=0')

def getHouse(ids):
    import GJDB
    DB = GJDB.GJDB()
    DB.tg()
    DB.selectDB('house_premier')
    DB.selectData('set names utf8')
    sql = 'SELECT TYPE, house_id, title, account_id, FROM_UNIXTIME(post_at)  FROM house_source_list WHERE post_at >= UNIX_TIMESTAMP("2014-03-01") AND account_id IN (' + ids + ')'
    return DB.selectData(sql)
'''
i = 0
for line in idFile:
    r = isFree(line[:-1])
    if len(r):
        if i < 100:
            result.write(str(r[0][0])+ ',')
            i = i + 1
        else:
            result.write(str(r[0][0])+ '\n')
            i = 0
'''
for line in idFile:
    print getHouse(line[:-1])
    result.write()