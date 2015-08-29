# -*- coding: utf-8 -*-
import re,time,urllib2,urllib,cookielib

class Html:
    
    params = ''
    url = ''
    headers = {}
    cj = ''
    req = ''
    cookie = ''
    opener = ''
    filename = ''
    addHeaders = {}
    response = ''
    
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.cookie = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie)
        urllib2.install_opener(self.opener)
    
    def get(self,url,params):
        self.url = url
        self.params = urllib.urlencode(params)
        self.url = (self.url,self.url + '?' + self.params)[self.params!=""]
        self.response = urllib2.urlopen(self.url)
        #self.headers = dict(self.response.info())
        return self.response.read()
    
    def post(self,url,params,headers):
        self.url = url
        self.params = urllib.urlencode(params)
        try:
            if not headers:
                #self.headers = headers
                self.req = urllib2.Request(
                    url = self.url,
                    data = self.params
                    )
            else:
                self.req = urllib2.Request(
                    url = self.url,
                    data = self.params,
                    headers = headers
                    )
            
            if len(self.addHeaders)>=1:
                for name in self.addHeaders:
                    if not self.req.has_header(name):
                        self.req.add_header(name, self.addHeaders[name])
            self.response = urllib2.urlopen(self.req)
            #self.headers = dict(self.response.info())
            return self.response.read()
        except Exception,e:
            return e
    
    def headerConf(self,headerDic):
        for name in headerDic:
            self.addHeaders[name] = headerDic[name]
    
    def download(self,url,filename):
        tStart = time.time()
        self.url = url
        self.filename = filename
        self.response = urllib2.urlopen(self.url)
        with open(self.filename, "wb") as down:
                down.write(self.response.read())
                down.close()
        tEnd = time.time()
        return str(int((tEnd - tStart)*1000)/1000.0)
        
    def clear(self):
        self.cj = ""
        self.params = ''
        self.url = ''
        self.headers = {}
        self.req = ''
        self.cookie = ''
        self.opener = ''
        self.filename = ''
        self.addHeaders={}
        return True
if __name__ == '__main__':
    import sys
    h = Html()
    try:
        h.download(sys.argv[1],sys.argv[2])
    except Exception, e:
        print e
