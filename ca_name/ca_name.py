#coding:utf-8
import sys
import html
import hive
from commonFunction import dateVal

hiveHandle = hive.Hive()

def fromAnalysisSimple(dt,conditions):
    
    sql = 'select dt,count(distinct uuid) as uv, count(1) as pv from web_pv_log_detail3 where dt="' + dt + '" and ' + conditions + ' and cat regexp "/fang/" group by dt;'
    print sql
    hiveHandle.desc = 'temp'+dt
    hiveHandle.session_name = 'temp'+dt
    try:
        hiveHandle.select(sql,hiveHandle.desc,hiveHandle.session_name)
        hiveHandle.getData()
    except Exception, e:
        print e

def fromAnalysisAll(select,conditions):

    sql = 'select ' + select + ' from web_pv_log_detail3 where ' + conditions + ';'
    print sql
    hiveHandle.desc = 'temp'
    hiveHandle.session_name = 'temp'
    try:
        hiveHandle.select(sql,hiveHandle.desc,hiveHandle.session_name)
        hiveHandle.getData()
    except Exception, e:
        print e
    
    
def main():
    if dateVal(sys.argv[1]):
        fromAnalysisSimple(sys.argv[1],sys.argv[2])
    else:
        fromAnalysisAll(sys.argv[1],sys.argv[2])
    f = open('data/'+hiveHandle.session_name+'.txt','r')
    print f.read()

if __name__ == "__main__":
    main()