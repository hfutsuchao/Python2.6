#coding:utf-8
import requests
from urllib import urlencode
from myThread import MyThread
from BeautifulSoup import BeautifulSoup
import os

districtBig = open('districtBig.txt','w')
streetBig = open('streetBig.txt','w')

with open('district.txt','r') as districts:
    for i, line in enumerate(districts):
        print i,line
        city, districtName, url = line.split('\t')
        html = requests.get(url[:-1]).text
        html = BeautifulSoup(html)
        span = html.findAll('span',{'class':'fr'})
        houseNum = span[0].strong.contents[0].split('条')[0]
        if int(houseNum) >= 10:
            districtBig.write(city + '\t' + districtName + '\t' + houseNum + '\t' + url)

with open('street.txt','r') as streets:
    for i, line in enumerate(streets):
        print i,line
        city, streetName, url = line.split('\t')
        html = requests.get(url[:-1]).text
        html = BeautifulSoup(html)
        span = html.findAll('span',{'class':'fr'})
        houseNum = span[0].strong.contents[0].split('条')[0]
        if int(houseNum) >= 10:
            streetBig.write(city + '\t' + streetName + '\t' + houseNum + '\t' + url)
