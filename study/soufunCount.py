# -*- coding: utf-8 -*-
import re,time,urllib2,urllib

def main():
    
    loginCNblogs()
    pass


citys = open('C:\\Users\\suchao\\Desktop\\soufun.txt').readlines()

for city in citys:
    urls = re.findall("http://.{0,30}/",city)

print len(urls)
sum = 0

def loginCNblogs():
    dic = {}
    global sum
    for domain in urls:
        try:
            url = domain +'housing/'
            #print url
            html = urllib2.urlopen(url).read()
            #print html
            s = re.findall('<span class=\"number orange\">(\d*)</span>',html,re.S)
            print s
            sum = sum + int(s[0])
            dic[domain] = int(s[0])
            
        except Exception,e:
            print url,e
    print sum
    for d in dic:
        print d,dic[d]
if __name__ == '__main__':
    main()
    pass
