from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse,Http404
import datetime,time
import qd
#from uvMonitor.UVPVPub import *
from urllib import unquote

def stat(request,source='',detail='',dur=''):
    if source:
        qd.sources = [source]
    if detail:
        qd.detail = detail
    if dur:
        qd.day_dt_stat_date = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*int(dur)))
        
    dic = qd.getDetail()
    dateList = qd.getDates(qd.day_dt_stat_date,qd.day_dt_end_date)
    for source in dic:
        for detail in dic[source]:
            for dt in dateList:
                if dt not in dic[source][detail]:
                    dic[source][detail][dt] = {'uv':0,'pv':0}
    datas = {}
    for source in dic:
        for detail in dic[source]:
            if detail not in ['avg','total']:
                datas[detail] = []
                for dt in dateList:
                    datas[detail].append(dic[source][detail][dt]['uv'])
                    
    return render_to_response('lineChart.html', {'dateList': dateList, 'datas':datas} )

def uvPVPub(request,days,city,type):
    
    city = unquote(city).encode('utf-8')
    
    dic = getUVPVPub(days,city,type)
    
    '''for date in dic:
        for detail in dic[source]:
            if detail not in ['avg','total']:
                datas[detail] = ''
                for dt in dateList:
                    datas[detail] = str(datas[detail]) + str(dic[source][detail][dt]['uv']) + ',' 
                datas[detail] = datas[detail][:-1]'''
    #dateList = [2013-05-13,2013-05-13,2013-05-13,2013-05-13,2013-05-13]
    #datas = {'series1':{'name':'baidu','data':[1,2,3,4,5]},'series2':{'name':'360','data':[5,4,3,2,1]}}
    return render_to_response('lineChart.html', {'dateList': dic['dateList'], 'datas':dic['datas']} )

def getCitysSources(request,city):
    
    cityName = unquote(city).encode('utf-8')
    
    citysUV = getAllCitysSources(cityName)
    
    return render_to_response('pieChart.html', citysUV)
