# coding:utf-8
from __future__ import with_statement
#from PyWapFetion import Fetion, send2self, send
import urllib2,re,os,time,math,sys


myurl = 'http://in.finance.yahoo.com/d/quotes.txt?s=QIHU,BIDU&f=sl1d1t1c1ohgvj1pp2owern&e=1.txt'
#for key in buys:
#    myurl = myurl + key + ','
response = urllib2.urlopen(myurl)
html = response.read()
for line in html.split('\n'):
    print len(line.split(','))
