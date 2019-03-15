#coding:utf-8
import requests
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
from EmailClass import Email
import sys
reload(sys)
sys.setdefaultencoding('utf8')

myMail = Email(password='814155356')

urlLists = open('/Users/NealSu/GoogleDisk/MyTools/Python2.6/tools/cityXiaoqu.txt','r').readlines()
result = open('/Users/NealSu/GoogleDisk/MyTools/Python2.6/tools/result.txt','r').readlines()

#already published
dicLastUrl = {}
for i in result:
    dicLastUrl[i.split('\t')[0]] = i.split('\t')[4][:-1]

cats = ['fang1']

result = open('/Users/NealSu/GoogleDisk/MyTools/Python2.6/tools/result.txt','w')

for i, line in enumerate(urlLists):
    try:
        city, keyword, hx = line.split()
        if keyword not in dicLastUrl:
            dicLastUrl[keyword] = ''
    except:
        print line
        continue
    #print i, line
    for cat in cats:
        try:
            url = 'http://' + city + '.ganji.com/' + cat + '/a1b4000e5500h3m1/_' + urlencode({'':keyword}).split('=')[1] + '/'
            print url
            html = BeautifulSoup(requests.get(url).text)
            house = html.findAll('div', {'class':'f-list-item'})[0]
            elm = house.findAll('div', {'class':'dd-item title'})
            title = dict(elm[0].a.attrs)['title']
            href = 'http://' + city + '.ganji.com' + dict(elm[0].a.attrs)['href']

            #Get HouseAttrs
            houseAttrs = house.findAll('div', {'class':'list-word'})[0].findAll('span')
            xiaoquName = houseAttrs[0].findAll('a')[1].contents[0]
            huxing = houseAttrs[1].i.nextSibling
            if hx == huxing.split('室')[0] and dicLastUrl[keyword]!=href:
                myMail.sendEmail(xiaoquName+huxing,href)
            result.write(keyword + '\t' + xiaoquName + '\t'  + huxing + '\t' + title + '\t' + href + '\n')
        except Exception,e:
            print e
            continue
result.close()
