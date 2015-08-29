# -*- coding: cp936 -*-
import re,time,urllib2,urllib

def main():
    
    #登录博客园
    loginCNblogs()
    pass

#登录博客园

cityNames = ['bj','sh','sz','w','cd','xa','cq','gz']

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
        for domain in cityNames[:1]:
            url = 'http://'+domain+'.58.com/xiaoqu/'
            html = urllib2.urlopen(url).read()
            print html
            s = re.findall('<dl class="searchitem cl"><dt>\S*</dt>\n <dd><a id="\S*" href="/xiaoqu/">\S*</a>(<a id="\S*" href="(/xiaoqu/\S*/)">(\S*)</a>)</dd>\n</dl>',html,re.S)
            if len(s) == 0:
                print s
            else:
                print s
    except Exception,e:
        print(e)
    pass
if __name__ == '__main__':
    main()
