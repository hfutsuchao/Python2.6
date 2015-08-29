#coding:utf-8
import requests
import BeautifulSoup

rw = open('kwResultNum.txt','w')

with open('C:/Users/suchao/Desktop/111.txt') as kws:
    for line in kws:
        try:
            city,cat, kw, uv, v, pv = line.split('\t')
            url = 'http://' + city + '/fang1/_' + kw + '/'
            html = requests.get(url)
            html = BeautifulSoup.BeautifulSoup(html.text)
            rw.write(line[:-1] + '\t' + html.findAll('span',{'class':'fr'})[0].strong.contents[0] + '\n')
        except:
            print line,url
            continue