# -*- coding: utf8 -*-
import urllib2
import time
import datetime
import re

print time.strftime('当前时间是：%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
t = datetime.datetime.now()
month = t.month
day = t .day
# print month,day

patt = 'www\.fenxs\.com\/\d+\.html" \S+ ' + str(month) + '\S\S\S' + str(day) + '\S\S\S'

# print patt
url = 'http://www.fenxs.com/'

try:
    f = urllib2.urlopen(url,timeout=5).read()
except urllib2.URLError,e:
    print e.reason
# print f
# temp = f.decode('utf8')
m = re.search(patt,f)
if m:
    # print m.group()
    print "found!!!"
else:
    print "not found"

url = 'http://' + str(re.match('www\.fenxs\.com\/\d+\.html',m.group()).group())
print url
try:
    f = urllib2.urlopen(url,timeout=5).read()
except urllib2.URLError,e:
    print e.reason
# print f
print '####################################################'
# patt = '\w{6,}:[12]\\xb7\\xd6\\xcf\\xed\\xc9\\xe7\\xd1\\xb8\\xc0\\xd7\\xbb\\xe1\\xd4\\xb1\\xc3\\xdc\\xc2\\xeb\d+<'
patt = '[\\x80-\\xff]+\w{6,}:[12][\\x80-\\xff]+\w+<'
# patt = '\w{6,}:[12]\S+\d+<'
m = re.findall(patt,f)
z = open('xunlei.txt','a')
z.write(time.strftime('当前时间是：%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
for x in m:
    print x[:-1]
    z.write(x[:-1]+'\n')
z.close()
