#coding:utf-8
import html,time
import BeautifulSoup
from urllib import quote

htmlHandle = html.Html()

'''loginUrl = 'http://www.aizhan.com/login.php?refer=http://ci.aizhan.com/'

params = {
            'email':'hfutsuchao@gmail.com',
            'password':'814155356',
            'refer':'http%3A%2F%2Fci.aizhan.com%2F'
          }
htmlHandle.get(loginUrl,'')
htmlHandle.post(loginUrl,params,'')
'''

#fileResult = open('result.txt','w')

dic = {}

with open('stocks.txt','r') as stocks:
    for kw in stocks:
        kw = kw[:-1]
        dic[kw] = {}
        try:
            url = 'http://finance.yahoo.com/q/op?s=' + kw + '+Options'
            print url
            content = htmlHandle.get(url,'')
            content = BeautifulSoup.BeautifulSoup(content)
            datas = content.findAll('div',{'class':'quote-table-overflow'})
            for data in datas:
                optionType = data.findAll('caption')[0].contents[0].replace(' ','').replace('\n','')
                print optionType
                dic[kw][optionType] = {}
            callDatas = datas[0].tbody.findAll('tr')
            putDatas = datas[1].tbody.findAll('tr')
            print len(callDatas)
            for row in callDatas:
                rowdatas = row.findAll('td')
                
                optionName = rowdatas[1].div.a.contents[0]
                optionVolume = rowdatas[7].strong.contents[0]
                print optionName, optionVolume
            
            time.sleep(5)
        except Exception,e:
            print e