# -*- coding: utf-8 -*-
import re,time,urllib2,urllib

def main():
    
    loginCNblogs()
    pass


citys = open('C:\\Users\\suchao\\Desktop\\58.txt').readlines()

for city in citys:
    urls = re.findall("co\('(.{1,15})'\)",city)

print len(urls)
sum = 0

def loginCNblogs():
    dic = {}
    global sum
    for domain in urls:
        try:
            url = 'http://'+domain+'.58.com/xiaoqu/'
            #print url
            html = urllib2.urlopen(url).read()
            #print html
            s = re.findall('<span class="tbfilter_l fl">共&nbsp;<b class="filternum">(.*)</b>&nbsp;条小区信息</span>',html,re.S)
            sum = sum + int(s[0])
            dic[domain] = int(s[0])
            #print s
        except Exception,e:
            print url,e
    print sum
    for d in dic:
        print d,dic[d]
if __name__ == '__main__':
    main()
    pass
