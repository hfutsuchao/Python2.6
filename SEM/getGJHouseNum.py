#coding:utf-8
import requests
from urllib import urlencode
from myThread import MyThread
from BeautifulSoup import BeautifulSoup

urlLists = open('/Users/NealSu/Downloads/url','r').readlines()
result = open('/Users/NealSu/Downloads/result','w')

def getGJhouseNum(url):
    html = BeautifulSoup(requests.get(url).text)
    elm = html.findAll('span', {'class':'fr'})
    return elm[0].strong.contents[0] 

'''
for i, line in enumerate(urlLists[1:]):
    try:
        xiaoqu_id, city, type, content, url = line[:-1].split('\t')
    except Exception,e:
        print line,e
        continue
    print i, line
    try:
        num = getGJhouseNum(url)
        result.write(url[:-1] + '\t' + str(num) + '\n')
    except Exception,e:
        print line,e
        continue
'''

for i, url in enumerate(urlLists):
    url = url[:-1]
    print url
    num = getGJhouseNum(url)
    result.write(url + '\t' + str(num) + '\n')
