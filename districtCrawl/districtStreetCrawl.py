#coding:utf-8
import sys
import html,time
import BeautifulSoup
import os
import sms
import time

htmlHandle = html.Html()

sms = sms.SMS()

dicCity = {}

with open('citys.txt','r') as citys:
    for city in citys:
        try:
            id, cityNmae = city.split('\t')
            dicCity[id] = cityNmae[:-1]
        except Exception, e:
            print e,'1'
outputFile = open('districtStreet.txt','w')

#print dicCity


def getDistric(cityId):
    
    dicDsitrict = {}
    dicStreet = {}
    global dicCity
    
    url = 'http://post.58.com/' + str(cityId) + '/8/s5'
    print url
    try:
        content = htmlHandle.get(url,'')
        content = BeautifulSoup.BeautifulSoup(content)
        
        districtTag = content.findAll('select',id='localArea')
        streetTag = content.findAll('select',id='selectDiduanHidden')
        #print districtTag[0]
        #print streetTag[0]
        for option in districtTag[0].findAll('option'):
            name = option.contents[0]
            #print name,dict(option.attrs)['value']
            dicDsitrict[dict(option.attrs)['value']] = name
            
        for option in streetTag[0].findAll('option'):
            name = option.contents[0]
            #print name,dict(option.attrs)['id'],dict(option.attrs)['value']
            key = dicDsitrict[dict(option.attrs)['id'].split('_')[0]]
            if key in dicStreet:
                dicStreet[key] = dicStreet[key] + ',' + name
            else:
                dicStreet[key] = name
        
        for value in dicDsitrict.values():
            if (value not in dicStreet) and (value != '--区域--'):
                dicStreet[value] = ''
        
        for key in dicStreet:
            #print key,dicStreet[key]
            outputFile.write(dicCity[cityId] + '\t' + key + '\t' + dicStreet[key] + '\n')
    except Exception, e:
        print e,'2'
        #sms.sendSMS("MBP rate Change!"+str(e),6)
for id in dicCity.keys():
    try:
        getDistric(id)
    except Exception, e:
        print e,'3'
    time.sleep(2)