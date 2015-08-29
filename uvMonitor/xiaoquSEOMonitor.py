#coding:utf-8
import html,hive,os

#{{Get Xiaoqu SEOUV From pvLogFile
def getXiaoquSEO(logFile,xiaoquListFile):
    xiaoquDic = {}
    with open(logFile,'r') as pvLogs:
        try:
            for line in pvLogs:
                try:
                    xiaoqu, uuid = line.split('\t')
                except Exception, e:
                    print e
                    continue
                uuid = uuid[:-1]
                if xiaoqu in xiaoquDic:
                    if uuid not in xiaoquDic[xiaoqu]['uuids']:
                        xiaoquDic[xiaoqu]['uuids'].append(uuid)
                        xiaoquDic[xiaoqu]['uv'] = xiaoquDic[xiaoqu]['uv'] + 1
                        xiaoquDic[xiaoqu]['pv'] = xiaoquDic[xiaoqu]['pv'] + 1
                    else:
                        xiaoquDic[xiaoqu]['pv'] = xiaoquDic[xiaoqu]['pv'] + 1
                else:
                    xiaoquDic[xiaoqu] = {}
                    xiaoquDic[xiaoqu]['uuids'] = [uuid]
                    xiaoquDic[xiaoqu]['uv'] = 1
                    xiaoquDic[xiaoqu]['pv'] = 1
        except Exception, e:
            print e
    print len(xiaoquDic)
    
    sumUV = 0
    sumPV = 0
    with open(xiaoquListFile,'r') as xiaoqus:
        for xiaoqu in xiaoqus:
            xiaoqu = xiaoqu[:-1]
            if xiaoqu in xiaoquDic:
                sumUV = sumUV + xiaoquDic[xiaoqu]['uv']
                sumPV = sumPV + xiaoquDic[xiaoqu]['pv']
    return sumUV,sumPV
#}}

#def getData(startDate,endDate):
    
dts = ["2013-09-"+(str(i),str(i))[len(str(i))-1] for i in range(10,29)]

dyn = globals()

for day in dts:
    dyn['hive'+day] = hive.Hive()
    #sql = "select regexp_extract(url, '/xiaoqu/([^/]*)/(.*|$)',1), uuid from web_pv_log_detail3 where dt = '" + day + "' and gjch regexp 'xiaoqu'"
    
    sql = "select regexp_extract(url, '/xiaoqu/([^/]*)/(.*|$)',1), uuid from web_pv_log_detail3 where dt = '" + day + "' and url regexp 'http://bj.ganji.com/xiaoqu/' and ca_name='se'"
    
    dyn['hive'+day].desc = day + 'xiaoquPvLog'
    dyn['hive'+day].session_name = day + 'xiaoquPvLog'
    print dyn['hive'+day].desc
    dyn['hive'+day].select(sql, dyn['hive'+day].desc, dyn['hive'+day].session_name)

xiaoquSEOUV = {}
for day in dts:
    #print dyn['hive'+day]
    print day
    print dyn['hive'+day].getData()
    uv, pv = getXiaoquSEO('data/'+dyn['hive'+day].desc+'.txt','xiaoqu.txt')
    xiaoquSEOUV[day] = str(uv) + '\t' + str(pv)
print xiaoquSEOUV

#xiaoquSEOUV = getData(10,27)

outPut = open('xiaoquSEO.txt','w')
for day in xiaoquSEOUV:
    try:
        outPut.write(day + '\t' + xiaoquSEOUV[day] + '\n')
    except:
        pass
#os.system('shutdown -h')