#coding:utf-8
import sms,html,hive,time,json,sys

params = {"UserName":"suchao","Domain":"@ganji.com","Password":"hFuT8141553561307"}
url = "http://sso.ganji.com/Account/LogOn"

stat = html.Html()
stat.post(url,params,"")

stat.headerConf({'X-Requested-With':'XMLHttpRequest'})

sourceURL = 'http://stat.corp.ganji.com/CustomBaseReportManagement/GetCustomBaseReportData?reportId=20035'
#seoURL = 'http://stat.corp.ganji.com/KendoUI/ReportViz?reportId=20051'
day_dt_stat_date = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*7))
day_dt_end_date = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*1))

sources = ['dh','seo','ganji_edm','unknown','sem','sns','total','self']
sources = ['seo']
detail = ''
operation = ''

Judgmentdetail = detail

def getDates(day_dt_stat_date,day_dt_end_date):
    dateStart = time.mktime(time.strptime(day_dt_stat_date, '%Y-%m-%d'))
    dateEnd = time.mktime(time.strptime(day_dt_end_date, '%Y-%m-%d'))
    days = int(dateEnd - dateStart)/86400 + 1
    dateList = []
    for day in range(0,days):
        dateList.append(time.strftime('%Y-%m-%d', time.localtime(dateStart + 86400*day)))
    return  dateList


def getData(day_dt_stat_date,day_dt_end_date):
    global sources,detail
    
    count = ['total','avg']
    uvpv = ['uv','pv']
    
    dic = {}.fromkeys(sources,{})
    
    for source in dic:
        dic[source] = dic[source].fromkeys(count,{}.fromkeys(uvpv,0))
        
    for source in sources:
        sourceParams = {
                        'page':'1',
                        'para_filter':'"day_dt_stat_date":"' + day_dt_stat_date + '","day_dt_end_date":"' + day_dt_end_date + '","city_key":"0","category_key":"7","source":"' + source + '"',
                        'size':'10000000'
                        }
        
        if detail and detail != 'All':
            sourceParams['para_filter'] = sourceParams['para_filter'] + ',"detail":"' + detail + '"'
        
        #print sourceParams
        #print sourceURL,sourceParams
        
        getR = stat.post(sourceURL,sourceParams,"")
        
        #print type(getR),getR
        
        sourceData = json.loads(getR)
        
        for i in xrange(0,sourceData['total']):
            row = sourceData['data'][i]
            detail = row['detail']
            day_name = row['day_name']
            uv = row['uv']
            pv = row['pv']
            if detail in dic[source]:
                if day_name in dic[source][detail]:
                    dic[source][detail][day_name]['uv'] = dic[source][detail][day_name]['uv'] + int(uv)
                    dic[source][detail][day_name]['pv'] = dic[source][detail][day_name]['pv'] + int(pv)
                else:
                    dic[source][detail][day_name] = {}
                    dic[source][detail][day_name]['uv'] = int(uv)
                    dic[source][detail][day_name]['pv'] = int(pv)
            else:
                dic[source][detail] = {}
                dic[source][detail][day_name] = {}
                dic[source][detail][day_name]['uv'] = int(uv)
                dic[source][detail][day_name]['pv'] = int(pv)
        
        for detail in dic[source]:
            if detail in count:
                continue

            if 'total' not in dic[source][detail]:
                dic[source][detail]['total'] = {}
                dic[source][detail]['total']['uv'] = 0
                dic[source][detail]['total']['pv'] = 0
                dic[source][detail]['avg'] = {}
                dic[source][detail]['avg']['uv'] = 0
                dic[source][detail]['avg']['pv'] = 0
        
            #print detail,len(dic[source][detail])
            for day_name in dic[source][detail]:
                try:
                    if day_name in count:
                        continue
                    dic[source][detail]['total']['uv'] = dic[source][detail]['total']['uv'] + dic[source][detail][day_name]['uv']
                    dic[source][detail]['total']['pv'] = dic[source][detail]['total']['pv'] + dic[source][detail][day_name]['pv']
                    dic[source]['total']['uv'] = dic[source]['total']['uv'] + dic[source][detail][day_name]['uv']
                    dic[source]['total']['pv'] = dic[source]['total']['pv'] + dic[source][detail][day_name]['pv']
                except Exception,e:
                    print e
                    
            dic[source][detail]['avg']['uv'] = dic[source][detail]['total']['uv']/float(len(dic[source][detail])-2)
            dic[source][detail]['avg']['pv'] = dic[source][detail]['total']['pv']/float(len(dic[source][detail])-2)
        try:
            dic[source]['avg']['uv'] = dic[source]['total']['uv']/float(len(dic[source][detail])-2)
            dic[source]['avg']['pv'] = dic[source]['total']['pv']/float(len(dic[source][detail])-2)
        except Exception,e:
            #print e
            pass
        #print dic[source]['avg']['uv'],dic[source]['avg']['pv']
        #print detail,dic[source][detail]
        #break
    return dic


def getDetail():
    dic = getData(day_dt_stat_date,day_dt_end_date)
    return dic

def getOption():
    dic = getDetail()
    if operation == 'getOption':
        str = "<option value='All'>All</option>"
        for source in sources:
            dic[source].pop('avg')
            dic[source].pop('total')
            for i in sorted(dic[source].items(),key = lambda x:x[1]['avg']['uv'],reverse = True):
                str = str + "<option value='" + i[0] + "'>" + i[0] + "</option>"
        return str

def getAll():
    dic = getDetail()
    dicAll = {}
    dateList = getDates(day_dt_stat_date,day_dt_end_date)
    for source in sources:
        dicAll[source] = {}
        dicAll[source]['All'] = {}
        for date in dateList:
            for detail in dic[source]:
                if detail in ['avg','total']:
                    continue
                if date in dicAll[source]['All']:
                    try:
                        if date in dic[source][detail]:
                            #print dicAll[source][date]['uv'],int(dic[source][detail][date]['uv'])
                            dicAll[source]['All'][date]['uv'] = dicAll[source]['All'][date]['uv'] + int(dic[source][detail][date]['uv'])
                    except Exception,e:
                        print e
                        print 'hah'
                        pass
                else:
                    dicAll[source]['All'][date] = {}
                    try:
                        if date in dic[source][detail]:
                            dicAll[source]['All'][date]['uv'] = int(dic[source][detail][date]['uv'])
                    except Exception,e:
                        print e
                        print 'hah2'
                        pass
    return dicAll

'''
qd = {}

for source in dic:
    for detail in dic[source]:
        if  type(dic[source][detail]) == dict and detail not in ['total','avg']:
            for dt in dic[source][detail]:
                #print source,detail,dt,dic[source][detail][dt]
                qd[source + '_' + detail + '_' + dt] = dic[source][detail][dt]
    #break
'''
#print json.dumps(qd)

'''fileQd = open('qd.txt','w')

for row in sorted(qd.items(),key = lambda y:y[1]['uv'],reverse = True):
    fileQd.write(row[0] + '\t' + str(row[1]['uv']) + '\t' + str(row[1]['pv']) + '\n')

fileQd.close()'''
#print json.dumps(dic, indent=1);