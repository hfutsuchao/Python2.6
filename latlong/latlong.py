#-*- coding: utf-8 -*-
from xml.dom import minidom
import urllib2, urllib, re
jwd = open('C:\\Users\\suchao\\Desktop\\bjjwd.txt','w')
KEY = 'ABQIAAAAm5e8FerSsVCrPjUC9W8BqBShYm95JTkTs6vbZ7nB48Si7EEJuhQJur9kGGJoqUiYond0w-7lKR6JpQ'
url = 'http://maps.googleapis.com/maps/api/geocode/xml'
xiaoqu = open('C:\\Users\\suchao\\Desktop\\jwd.txt').readlines()
for xq in xiaoqu:
    cityName,dist = xq.split('-')
    city = {'sensor': 'false','address': cityName+dist}
    city = urllib.urlencode(city)
    #print city
    url_get = url + '?' +city
    print url_get
    #print url_get
    #url_get = url + '?' +'sensor=false&address='+xq[:-1]
    handler = urllib2.urlopen(url_get).read()
    result = re.findall('<location>\s+<lat>(.*?)</lat>\s+<lng>(.*?)</lng>\s+</location>',handler)
    try :
        lon = result[0][0]
        lat = result[0][1]
        jwd.write(cityName+dist+'\t'+str(lon)+'\t'+str(lat)+'\n')
    except:
        jwd.write(cityName+dist+'\t'+'No result!\n')
        #print(xq[:-1]+'\t'+'No result!\n')
