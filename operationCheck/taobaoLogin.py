# -*- coding: gbk -*-  


import urllib, urllib2, socket, cookielib
import json, re, os
import time, datetime

# from gzipSupport import ContentEncodingProcessor

# set timeout
timeout = 20
timesleep = 10
socket.setdefaulttimeout(timeout)

httpHandler = urllib2.HTTPHandler()
httpsHandler = urllib2.HTTPSHandler()

# cookie support
cookie = cookielib.CookieJar()
cookie_support= urllib2.HTTPCookieProcessor(cookie)

# gzip support
# gzip_support = ContentEncodingProcessor

opener = urllib2.build_opener(cookie_support, httpHandler, httpsHandler)
urllib2.install_opener(opener)

def get_headers():
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13",
        #"User-Agent" = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-cn,zh;q=0.5",
        #"Accept-Encoding":"gzip,deflate",
        "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive":"115",
        "Connection":"keep-alive"
    }

    return headers

def get_login_data():
    login_data = {
            'TPL_username':u'594爱你'.encode('gbk'),
            'action':'Authenticator',
            'event_submit_do_login':'anything',
            'TPL_redirect_url':'',
            'from':'tb',
            'fc':'2',
            'style':'default',
            'css_style':'',
            'tid':'',
            'support':'000001',
            'CtrlVersion':'1,0,0,7',
            'loginType':'3',
            'minititle':'',
            'minipara':'',
            'pstrong':'3',
            'longLogin':'-1',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'from_encoding':''
            }
    return login_data

def login(source=None):
    """ login """
    url = 'https://login.taobao.com/member/login.jhtml'
    if not source:
        source = request(url=url)
    token_list = re.findall(r"input name='_tb_token_' type='hidden' value='([a-zA-Z0-9]+)'", source)
    login_data = get_login_data()
    login_data['_tb_token_'] = token_list[0] if token_list else ''
    login_data['TPL_password'] = raw_input("input password:")

    source = request(url=url, data=login_data)
    r = re.findall(r'window.location = "([\w\W]+)";', source)
    if r:
        redirect_url = r[0]
    else:
        print "login failed, valid password and try again"
        return False

    request(url=redirect_url)
    return True

def request(url, headers=None, data=dict()):
    if headers is None:
        headers = get_headers()
    
    data = urllib.urlencode(data) if data else None
    req = urllib2.Request(
            url = url,
            data = data,
            headers = headers
            )
    try:
        request = urllib2.urlopen(req)
        source = request.read()
        # print url
        # print request.code,request.msg
        request.close()
    except:
        source = None
        print "connect timeout"

    return source

if __name__=="__main__":
    login()
