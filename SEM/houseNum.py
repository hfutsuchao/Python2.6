#coding:utf-8
import requests
from urllib import urlencode
from myThread import MyThread
from BeautifulSoup import BeautifulSoup

urlLists = open('urls.txt','r').readlines()
result = open('result.txt','w')

cats = ['fang6','fang7','fang8','fang9']

for i, line in enumerate(urlLists[1:]):
    try:
        city, keyword = line.split()
    except:
        print line
        continue
    print i, line
    for cat in cats:
        try:
            url = 'http://' + city + '.ganji.com/' + cat + '/_' + urlencode({'':keyword}).split('=')[1] + '/'
            html = BeautifulSoup(requests.get(url[:-1]).text)
            elm = html.findAll('span', {'class':'fr'})
            num = elm[0].strong.contents[0].split('条')[0]
            result.write(line[:-1] + '\t'  + cat + '\t' + url + '\t' + str(num) + '\n')
        except:
            print line
            continue
#xqs = open('qgxq.txt','r').readlines()

'''dic = {}
for xq in xqs:
    try:
        city, xiaoqu, rent, sell = xq.split('\t')
        dic[city+xiaoqu] = rent + '\t' + sell[:-1]
    except:
        print xq'''



'''for line in esfs:
    city, xq, url, nums = line.split('\t')
    url = url.split('_')[0] + '_' + urlencode({'':xq.split('二手房')[0]}).split('=')[1] + '/'
    result.write(city + '\t' + xq + '\t' + url + '\t' + str(nums[:-1]) + '\n')'''
