# -*- coding: cp936 -*-
import re,time,urllib2,urllib

def main():
    
    #登录博客园
    loginCNblogs()
    pass

#登录博客园
def loginCNblogs():
    try:
        '''#设置 cookie
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        urllib2.install_opener(opener)
        parms = {"UserName":"lixueshi","Domain":"@ganji.com","Password":"mnldfgrxr1Q"}
        loginUrl = "http://sso.ganji.com/Account/LogOn"
        login = urllib2.urlopen(loginUrl,urllib.urlencode(parms))
        #print(login.read())'''
        aid = open('info.txt').readlines()
        #r = open('ph.txt','w')
        #aid = [id.split('\t')[1][:-1] for id in aid]
        for d in aid:
            cid,id = d.split('\t')
            url = 'http://bj.58.com/zufang/?final=1&searchtype=3&key=' + id[:-1]
            html = urllib2.urlopen(url).read()
            s = re.findall('id="numstat">\((.*)\)</i>',html)
            if len(s) == 0:
                pass
                #r.write(cid+'\t'+'0\n')
            else:
                print(cid+'\t'+s[0]+'\n')
                #r.write(cid+'\t'+s[0]+'\n')
    except Exception,e:
        print(e)
    pass
if __name__ == '__main__':
    main()
