#coding:utf-8
import sys
import html,time
import BeautifulSoup
import sms
import os

htmlHandle = html.Html()

sms = sms.SMS()

#url = 'http://store.apple.com/cn/browse/finance/installments'
url = 'http://store.apple.com/cn_cmb/browse/finance/installments/cmb'

dic = {}
def checkRate():
    try:
        content = htmlHandle.get(url,'')
        content = BeautifulSoup.BeautifulSoup(content)
        
        for tr in content.findAll('tr',{'class':'row-container-upper'}):
            tds = tr.findAll('th')
            for i,td in enumerate(tds):
                times = td.contents[0]
                dic[i] = times.strip()
        
        for tr in content.findAll('tr',{'class':'row-container-percentage'}):
            tds = tr.findAll('td')
            for i,td in enumerate(tds):
                rate = td.contents[0]
                dic[dic[i]] = rate.strip()
                print dic[i],dic[dic[i]]
                del dic[i]
        if dic[u'18期'] == '0%':
            sms.sendSMS("MBP免18期手续费啦！",6)
            sys.exit()
        elif dic[u'24期'] == '0%':
            sms.sendSMS("MBP免24期手续费啦！",6)
            sys.exit()
    except Exception, e:
        print e
        #sms.sendSMS("MBP rate Change!"+str(e),6)
    time.sleep(20)
    os.system('cls')
    checkRate()
checkRate()