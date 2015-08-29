# coding:gbk
from __future__ import with_statement
#from PyWapFetion import Fetion, send2self, send
import time,sys
import sms
from commonFunction import dateToday,sleep
import html
from myThread import MyThread
from BeautifulSoup import BeautifulSoup

sys.setrecursionlimit(100000)

header = {
          'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Host':'hq.sinajs.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
          }

headerOption = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'YM=v=2&u=qjjOLtiPsy7pXio7PK9qzesIpfMEGuWd04IIew--&d=&f=CAA&t=6Cq3RB&s=48uT; DK=v=2&p=NnwyMzMwfFZpcnR1YWx8RGVza3RvcCBCcm93c2VyfHw-; B=ejb8t3d8tt85q&b=4&d=Ttv38YxpYFSNLwtnQHNVTA--&s=36&i=M0ZjKI7WKsEIbtERiDQv; Y=v=1&n=86klq4qqtui0v&l=5x1zsx3v1tvx0sv0z52wzruwwyvxv5zx/o&p=02qvvcn002000000&iz=&r=ro&lg=en-US%2Czh-Hans-CN%2Czh-CN&intl=cn&np=1; T=z=6Cq3RB6WR8RBL0H1s.K/mw9&a=YAE&sk=DAAXwtEc.FpIXn&ks=EAAUZdV4z.p3QoFTVE2LDYOtQ--~E&d=YQFZQUUBZwFLSEhMN05XR0taN1pSSFI2UlZCNVRVTVlNNAFzY2lkAWtLSmRkankyT01aOThQU0tMSlZrRGNTa05Qby0Bb2sBWlcwLQFhbAFoZnV0c3VjaGFvQGdtYWlsLmNvbQFzYwFtd2ViAXp6ATZDcTNSQkE3RQF0aXABaWhJT3VE&af=QkJBQzhaOGEmdHM9MTM3MzU0NDYzNCZwcz1NS1o2Si54Vm40UC5ZT2U0WXZwQ3VnLS0-; PRF=&t=BIDU&bid=sogo; ucs=bnas=0; ywadp10001840545256=3922551523; fpc10001840545256=ZWkKGWn1|mETNEVvNaa|fses10001840545256=|Yr6u7wrNaa|ZWkKGWn1|fvis10001840545256=|8Mo1H7so11|8Mo1H7so11|8Mo1H7so11|8|8Mo1H7so11|8Mo1H7so11; RMBX=ejb8t3d8tt85q&b=4&d=Ttv38YxpYFSNLwtnQHNVTA--&s=36&i=M0ZjKI7WKsEIbtERiDQv&t=251; fpc1000911397279=ZfeZCW8I|fkKFEVvNaa|fses1000911397279=|fkKFEVvNaa|ZfeZCW8I|fvis1000911397279=|8Mo1H7soM0|8Mo1H7soM0|8Mo1H7soM0|8|8Mo1H7soM0|8Mo1H7soM0; U=mt=CTnXoZ2MhYiREBb0ZmFNxn2Bk0Bl37vsqP0jy5fu&ux=MVYmSB&un=86klq4qqtui0v; ypcdb=491eab95295a54d471d92b9311a4854e',
'Host':'finance.yahoo.com',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
                }
htmlHandle = html.Html()  
smsHandle = sms.SMS()

#{{{ price get
def stockDetail(stockNum):
    global htmlHandle,header
    myurl = 'http://hq.sinajs.cn/?_=0.7342358745470643&list=gb_' + stockNum

    html = htmlHandle.get(myurl,'')
    detail = html.split('="')[1].split(',')
    stockName = detail[0]
    nowPrice = detail[1]
    yesterdayPrice = detail[26]
    maxPrice = detail[8]
    minPrice = detail[7]
    changeRate = detail[2]
    return stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate
#}}}

#{{{ download the day picture
def downloadFenshi(stockNum):
    global htmlHandle
    imageUrl = 'http://image.sinajs.cn/newchart/v5/usstock/wap/min_daily/226/'+ stockNum + '.gif'
    return htmlHandle.download(imageUrl,'fenshi/'+stockNum+dateToday()+'.gif')
#}}}

#{{{ special price monitor
def stockPriceAlert(stockNum,priceAlert,type=-1):
    print stockNum,priceAlert,type
    priceAlert = float(priceAlert)
    type = int(type)
    stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate = stockDetail(stockNum)
    #print stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate
    msg = ''
    if (type == -1)  and (priceAlert >= float(nowPrice)):
        msg = stockNum + ' fall bellow ' + str(priceAlert) + ',Now:' + str(nowPrice)
    elif (type == 1) and (priceAlert <= float(nowPrice)):
        msg = stockNum + ' goes over ' + str(priceAlert) + ',Now:' + str(nowPrice)
    if msg != '':
        print msg
        smsHandle.sendSMS(msg)
        #stockPriceAlert(stockNum,priceAlert*(1-1/100.0),-1)
        
        threads=[]
        t = MyThread(stockPriceAlert,(stockNum,priceAlert*(1-1/100.0),-1),stockPriceAlert.__name__)
        threads.append(t)
        t = MyThread(stockPriceAlert,(stockNum,priceAlert*(1+1/100.0),1),stockPriceAlert.__name__)
        threads.append(t)
        for i in threads:
            i.start()
    else:
        sleep(5)
        stockPriceAlert(stockNum,priceAlert,type)
#}}}

#{{{ stock price monitor
def stockPriceMonitor(stockNum,AVGPrice,rate=0.01):
    AVGPrice = float(AVGPrice)
    rate = float(rate)
    stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate = stockDetail(stockNum)
    nowPrice = float(nowPrice)
    #print stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate
    change = (nowPrice - AVGPrice)/AVGPrice
    msg = ''
    if abs(change) >= rate:
        msg = stockNum + ' change:' + str(int(change*10000)/100.0) + '% | ' + str(AVGPrice) + ' -> ' + str(nowPrice)
    if msg != '':
            print msg
            smsHandle.sendSMS(msg)
            stockPriceMonitor(stockNum,float(nowPrice))
    else:
        sleep(5)
        stockPriceMonitor(stockNum,float(AVGPrice))
#}}}

#{{{ options price get
def getOptionDetails(stockNum):
    global htmlHandle,headerOption
    #url = 'http://finance.yahoo.com/q/op?s=BIDU&m=2014-02'
    url = 'http://finance.yahoo.com/q/os?s=' + stockNum + '&m=2013-12'
    htmls = BeautifulSoup(htmlHandle.get(url,''))
    datas = htmls.findAll('table',{'class':'yfnc_datamodoutline1'})[0].tr.td.table.findAll('tr')
    
    dic = {}
    for data in datas[2:]:
        details = data.findAll('td')
        strikePrice = details[7].b.a.contents[0]
        agreementCall = details[0].a.contents[0]
        agreementPut = details[8].a.contents[0]
        
        dic[agreementCall] = {}
        dic[agreementPut] = {}
        
        #dic[agreementCall]['change'] = details[2].b.span.contents
        dic[agreementCall]['bid'] = float(details[3].span.contents[0])
        dic[agreementCall]['ask'] = float(details[4].span.contents[0])
        dic[agreementCall]['AVGPrice'] = (dic[agreementCall]['bid'] + dic[agreementCall]['ask'])/2
        dic[agreementCall]['volume'] = int(details[5].span.contents[0])
        dic[agreementCall]['openInt'] = int(details[6].contents[0])
        dic[agreementCall]['strikePrice'] = float(strikePrice)
    
        dic[agreementPut]['strikePrice'] = float(strikePrice)
        dic[agreementPut]['bid'] = float(details[11].span.contents[0])
        dic[agreementPut]['ask'] = float(details[12].span.contents[0])
        dic[agreementPut]['volume'] = int(details[13].span.contents[0])
        dic[agreementPut]['openInt'] = int(details[14].contents[0])
        dic[agreementPut]['AVGPrice'] = (dic[agreementPut]['bid'] + dic[agreementPut]['ask'])/2
        
        try:
            lastCall = details[1].b.span.contents[0]
        except:
            lastCall = 'N/A'
        try:
            lastPut = details[9].b.span.contents[0]
        except:
            lastPut = 'N/A'
    return dic
#}}}

#{{{ options price monitor
def optionPriceMonitor(stockNum,agreementName,numbers,AVGPrice):
    AVGPrice = float(AVGPrice)
    numbers = int(numbers)
    dic = getOptionDetails(stockNum)
    nowAVGPrice = dic[agreementName]['AVGPrice']
    change = (nowAVGPrice - AVGPrice)/AVGPrice
    msg = ''
    if abs(change) >= -0.3:
        msg = agreementName + ' change:' + str(int(change*10000)/100.0) + '% | ' + str(AVGPrice) + ' -> ' + str(nowAVGPrice)
    return msg
#}}}

#{{{ options expect gains calculate
def optionExpectGains(stockNum,agreementName,AVGPrice,stockPrice=''):
    AVGPrice = float(AVGPrice)
    dic = getOptionDetails(stockNum)
    strikePrice = dic[agreementName]['strikePrice']
    if stockPrice == '':
        stockName,nowPrice,yesterdayPrice,maxPrice,minPrice,changeRate = stockDetail(stockNum)
        stockPrice = nowPrice
    stockPrice = float(stockPrice)
    if agreementName.find('C0') != -1:
        k = 1
    else:
        k = -1
    for i in range(-20,21):
        expectPrice = float(stockPrice) * (1+i/100.0)
        expectGain = (expectPrice - strikePrice)*k/AVGPrice - 1
        print str(i)+'%',expectGain
#}}}

#{{{ check some stocks option expect gains
def getNowOptionsExpectGains(stockNum):
    
    dic = getOptionDetails(stockNum)
    for agreementName in dic:
        print agreementName
        optionExpectGains(stockNum,agreementName,dic[agreementName]['AVGPrice'])
        sleep(5)

#}}}

def main():
    threads=[]
    t = MyThread(stockPriceAlert,('bidu',172.5,-1),stockPriceAlert.__name__)
    threads.append(t)
    t = MyThread(stockPriceAlert,('bidu',177.5,1),stockPriceAlert.__name__)
    threads.append(t)
    t = MyThread(stockPriceAlert,('yy',58.5,1),stockPriceAlert.__name__)
    threads.append(t)
    t = MyThread(stockPriceAlert,('yy',56.2,-1),stockPriceAlert.__name__)
    threads.append(t)
    #t = MyThread(stockPriceAlert,('qihu',81.5,1),stockPriceAlert.__name__)
    #threads.append(t)
    #t = MyThread(stockPriceAlert,('bidu',176,-1),stockPriceAlert.__name__)
    #threads.append(t)
    for i in threads:
        i.start()


'''myOptions = open('options.txt','r').readlines()
for line in myOptions[1:]:
    stockNum, agreementName, numbers, AVGPrice = line.split('\t')
    print optionPriceMonitor(stockNum,agreementName,numbers,AVGPrice)


myStocks = open('shares.conf','r').readlines()
for line in myStocks[1:]:
    stockNum,AVGPrice,numbers,isBuy = line.split('\t')
    if int(isBuy) == 1:
        stockPriceMonitor(stockNum,AVGPrice)
'''
#getNowOptionsExpectGains('bidu')
#downloadFenshi('qihu')
#getOptionDetails('bidu')
#stockPriceAlert('bidu',170.13,1)
#stockPriceAlert('bidu',172.01,-1)
#downloadFenshi('bidu')
'''myOptions = open('options.txt','r').readlines()
for line in myOptions[1:]:
    stockNum, agreementName, numbers, AVGPrice = line.split('\t')
    optionExpectGains(stockNum,agreementName,AVGPrice)'''
'''
if __name__ == '__main__':
    argvs = sys.argv
    stockNum = argvs[1]
    AVGPrice = '''

if __name__ == '__main__':
    main()
    #downloadFenshi('bidu')
