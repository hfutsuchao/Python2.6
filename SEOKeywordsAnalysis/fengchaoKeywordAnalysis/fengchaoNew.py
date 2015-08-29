# coding:utf-8
from pycurl import *
from StringIO import StringIO
import urllib
import json
import sys

cookie = 'BAIDUID=CF96835AE39DDE37C7D27B29DA46A6B6:FG=1; BAIDU_WISE_UID=7C87C87C3EA2C3FE8576400096B3DFAD; BDREFER=%7Burl%3A%22http%3A//news.baidu.com/%22%2Cword%3A%22%22%7D; BDUSS=VjT2JNZFgxZTNPZWk5Q3lkVW5jSXNLYTB0b2pzOHRoWFNNaUNaMTBLaHlLakJSQVFBQUFBJCQAAAAAAAAAAAEAAACjKaUEeXlseXN1Y2hhbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHKdCFFynQhRZ3; BDUT=847jCF96835AE39DDE37C7D27B29DA46A6B613a5e658ef21; Hm_lvt_1ae9a937a87d1c46cd8eed1d4d2a95f0=1371637736; MCITY=-%3A; locale=zh; SFSSID=0760abd27e0e7e13e88aa7f4d336f401; H_PS_PSSID=3360_2776_1466_2975_3089_3311; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a01290590100; __cas__st__3=fb3b94b560de43f84fb21ddbca55fefd71f361cf5dd56041a29bb39d5ffe878f78c3d628d060c3b98e231277; __cas__id__3=6560846; __cas__rn__=129059010; SAMPLING_COOKIE=6560846; SAMPLING_USER_ID=6560846'
token = 'fb3b94b560de43f84fb21ddbca55fefd71f361cf5dd56041a29bb39d5ffe878f78c3d628d060c3b98e231277'

userid = '6560846'

def curl(url, post_field):
#{{{
    s = StringIO()
    c = Curl()
    c.setopt(URL, url)
    c.setopt(WRITEFUNCTION, s.write)
    c.setopt(POSTFIELDS, post_field)
    c.setopt(COOKIE, cookie)
    c.setopt(TIMEOUT, 30)
    c.perform()
    c.close()
    return s.getvalue()
#}}}

cityDic = {}
matchedCityDic = {}

f = open('output.txt', 'w')
cityAll = open('cityAll.txt','w')
matchedKw = open('matched.txt','w')
matchedCityAll = open('matchedCityAll.txt','w')

for i, line in enumerate(open(sys.argv[1])):
    city = line.rstrip().split('\t')[0]
    try:
        keyword = line.rstrip().split('\t')[1]
    except:
        continue
    if keyword.find('二手房') != -1:
        continue    
    
    if city not in cityDic:
        cityDic[city] = 0
        matchedCityDic[city] = 0
    print i, city, keyword,
    post_field = urllib.urlencode({
        'params': '{"logid":933389882,"planid":0,"unitid":0,"entry":"kr_tools","query":"%s","regions":"","rgfilter":0,"device":"0","querytype":1}' % keyword,
        'path': 'GET/kr/word',
        'token': token,
        'userid': userid,

    })

    while 1:
        try:
            data = curl('http://fengchao.baidu.com/nirvana/request.ajax?path=GET/kr/suggestion', post_field)
            break
        except:
            pass

    if 'wordid' not in data:
        print data
        continue
    j = 0
    for group in json.loads(data)['data']['group']:
        for line in group['resultitem']:
            kw = line['word'].encode('utf-8')
            if kw == keyword:
                selfKw = '1'
            else:
                selfKw = '0'
            search = str(line['pv'])
            id = str(line['wordid'])
            kwc = str(line['kwc'])
            j += 1
            cityDic[city] = cityDic[city] + int(search)
            f.write('\t'.join([city, kw, search, selfKw, id, kwc])+'\n')
            if selfKw == '1':
                try:
                    matchedCityDic[city] = matchedCityDic[city] + int(search)
                    matchedKw.write('\t'.join([city, kw, search, selfKw, id, kwc])+'\n')
                except Exception, e:
                    print e
    print j

for city in cityDic:
    try:
        print city,cityDic[city]
        cityAll.write('\t'.join([city, str(cityDic[city])])+'\n')
    except Exception, e:
        print e
for city in matchedCityDic:
    try:
        print city,matchedCityDic[city]
        matchedCityAll.write('\t'.join([city, str(matchedCityDic[city])])+'\n')
    except Exception, e:
        print e
