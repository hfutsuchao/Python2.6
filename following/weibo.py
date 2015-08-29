# -*- coding: utf-8 -*-
import sys
import BeautifulSoup
import html
from commonFunction import replaceSign, dateToday, sleep
import myEmail, sms
import urllib2, httplib    
import StringIO, gzip

sended = []
server = myEmail.connect()

def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read()
    return data2

def weiboFollowing(id):
    global sended, sever
    url = 'http://m.weibo.cn/u/' + str(id)
    
    headers = {
               
               "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
                "Accept-Encoding" : "gzip,deflate,sdch", 
                "Accept-Language" : "zh-CN,zh;q=0.8", 
                "Cache-Control" : "max-age=0", 
                "Connection" : "keep-alive", 
                "Cookie" : "_T_WM=67482dd32c104ee6452160ff87248f3b; M_WEIBOCN_PARAMS=featurecode%3D20000181%26rl%3D1%26luicode%3D10000011%26lfid%3D1005051843543427%26fid%3D1005051843543427%26uicode%3D10000011", 
                "Host" : "m.weibo.cn", 
                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER"
               
               }
    
    print url
    handle = html.Html()
    #data = handle.get(url,'')
    data = handle.post(url,{'':''},headers)
    #print gzdecode(data)
    
    url = 'http://m.weibo.cn/page/card?itemid=1005051843543427_-_WEIBO_INDEX_PROFILE_WEIBO_GROUP_OBJ'
    data = handle.get(url,'')
    data = data.replace('"}','').replace('{"ok":"1","data":"','')
    #sys.exit()
    sData = BeautifulSoup.BeautifulSoup(data)
    
    lists = sData.find('article',{})
    firstDiv = lists.div
    print firstDiv
    sys.exit()
    userName = firstDiv.a.contents[0]
    content = replaceSign(firstDiv.a.nextSibling,0)
    time = replaceSign(firstDiv.find('span',{'class':'info'}).contents[0])
    
    if time <= dateToday():
        #sms.SMS().sendSMS(content)
        to='814155356@qq.com'
        subj= 'New message from ' + userName + ' in weibo'
        text = content
        if text not in sended:
            try:
                myEmail.sendmessage(server,subj,text,to)
                sended.append(text)
            except Exception,e:
                print e
    sleep(10)
    weiboFollowing(id)

if __name__ == '__main__':
    try:
        if sys.argv[1] != '':
            weiboFollowing(sys.argv[1])
    except:
        print "usage: weibo.py id \nNow following __moka__(the author's love)"
        weiboFollowing(1843543427)