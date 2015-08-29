# -*- coding: utf-8 -*-
import sys
import BeautifulSoup
import html
from commonFunction import replaceSign, dateToday, sleep
import myEmail, sms

sended = []
server = myEmail.connect()

def doubanFollowing(id):
    global sended, sever
    url = 'http://m.douban.com/people/' + str(id) + '/'
    handle = html.Html()
    data = handle.get(url,'')
    sData = BeautifulSoup.BeautifulSoup(data)
    
    lists = sData.div.find('div',{'class':'list'})
    firstDiv = lists.div
    
    userName = firstDiv.a.contents[0]
    content = replaceSign(firstDiv.a.nextSibling,0)
    time = replaceSign(firstDiv.find('span',{'class':'info'}).contents[0])
    
    if time <= dateToday():
        #sms.SMS().sendSMS(content)
        to='814155356@qq.com'
        subj= 'New message from ' + userName + ' in douban'
        text = content
        if text not in sended:
            try:
                myEmail.sendmessage(server,subj,text,to)
                sended.append(text)
            except Exception,e:
                print e
    sleep(10)
    doubanFollowing(id)

if __name__ == '__main__':
    try:
        if sys.argv[1] != '':
            doubanFollowing(sys.argv[1])
    except:
        print "usage: douban.py id \nNow following simimasen_lo(the author's love)"
        doubanFollowing(46068391)
