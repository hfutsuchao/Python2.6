#coding=utf-8
'''import urllib
import sys
import http.cookiejar

cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)             
opener = urllib.request.build_opener(cjhdr)


url = "http://options.sogotrade.com/Services/ChainService.asmx/GetOptions"
data = {
'chainType':'1',
'expiration':'"131213W"',
'isRotated':'false',
'showBinary':'true',
'showNonStandard':'false',
'strike':'null',
'strikes':'null',
'strikesRange':'"1"',
'underlyingSymbol':'"QIHU"'
}
headers = {
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"172",
"Content-Type":"application/json; charset=utf-8",
"Cookie":"__utma=243156864.2140095760.1377925186.1386249149.1386331890.40; __utmz=243156864.1381236194.8.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=site%3Asogotrade.com%20%E6%8F%90%E6%AC%BE; BureauSwitcher=SOGO; __utmc=243156864; PSSO=gBx%c3%9c8%c2%a2x%5e%c3%a6p%c2%aa%c3%9b%c3%9b%c3%ac%c3%a6%c2%81%c2%baY%0e%e2%80%9d%c3%91%5cF%c3%8b%3a%e2%80%9a%c3%a1%c3%a4A%0d%c6%92s%c3%a5%e2%80%9e!%c2%81%c2%b1%08W%c2%8d%07R%c3%86%c3%bb%13W%1c%c2%b6%c3%a9%c2%90%c3%96o%c3%af0%083%07%c5%93%c2%a7r%c2%bc%07%c2%90%c3%92C%c3%bc%cb%86%1bK1%c3%84%1c%00%e2%80%b0kUSE%c5%a1T%c3%8a%2bT%03%c3%aa%c3%ab%c3%99S%e2%80%b9%c2%ad%c2%a5%c3%be%c3%927%17j%c2%a2b%3f%c3%bd%c3%91%cb%86%c2%a0%27%c3%92%c2%bb%e2%80%98%cb%86m%23%c3%8b%c3%a7%3a%3d%c3%85%25%c3%ab%cb%9c%3c%c3%87%c2%bf%c3%87T%c2%bf%e2%80%9c%c3%a9%c2%b7%c3%89%5b%1c%3bJt.%c2%b9V%c3%89%c3%9fC%c2%ac%c3%ae%3c%c3%97%1dc%c2%ac%c3%b68QEc%c3%9d%c2%b8%2b%c3%95a%c3%99%c3%84%c3%a6%c2%af%c2%a80)%c2%a0%c2%81%c3%95e%c3%9fp%e2%80%9a%16%cb%864%25%c3%97%c5%bd%11%15%c5%be8%c3%8fC%3f%c3%a5%3c%c3%88!y%c3%bf%00PPJrq%c3%95ay%c3%b5%5b%c3%b8%3bg%c2%a6%e2%80%a6%c2%b9c%03%60q%00%06Z%09_%16%c3%a1%c2%b6%c3%b1t%c3%b7%c3%94%c3%bb%c3%b6%00%e2%80%9e%c2%81u8%c3%84!%c3%9c%14%c3%8d9%7e%01%e2%80%98e%c3%80%5e%c3%bdk%c2%aaZ%c3%abW%c3%8c%c3%93%c3%8a%14%24%40p%c3%95%13; StockSelectAuthCookie=CBEE392FAE0F367E5BDE20DD89E8EC7D20967CAA52314ACFE014A335B5E53C7D13DD6D49E574910F1DD6F2EF137AE58695DB4EC559D89DE6F346463885FE1DADD64BA1BC40769434F5C3CB6DA432E721FE24F83B23B47B7E4DBAAAE68238DAA9B2C18FD42BE10DA9EDDF22CE7E3CB6A23F8A7584C9DC8B58864FBFC91AD599C590A9EF63C5355B649419272FB30783EE78AC5FE9; ASP.NET_SessionId=h4bxrbbpt1mgbtlj5vl5hlic; TradeBottomTabIndex=0; ctl00_mc_ac_QuickQuotePane_QuickQuote1_stockChartGOOG=0; __utmb=243156864.1.10.1386331890; UserCulture=en-us; CurrentCulture=en-us; Exp=false",
"Host":"options.sogotrade.com",
"Pragma":"no-cache",
"Referer":"http://options.sogotrade.com/Chain.aspx",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0"
           }
#print (urlopen(url).read().decode("gbk"))                              #输出登录页面    

params = urllib.parse.urlencode(data).encode(encoding='UTF8')                            #将用户名、密码转换为 “username=admin&pwd=123456”的形式
#opener.open(url,params)                                                     #开始登录
full_url=urllib.request.Request(url,params)  
full_url.request.Request(url,params,headers)
print (opener.open(full_url).read().decode("gbk"))   #登录成功后，访问其它页面

'''




from urllib.error import URLError,HTTPError  
import urllib.request  
import urllib.parse  
url='http://options.sogotrade.com/Services/ChainService.asmx/GetOptions'  
data = {
'chainType':'1',
'expiration':'"131213W"',
'isRotated':'false',
'showBinary':'true',
'showNonStandard':'false',
'strike':'null',
'strikes':'null',
'strikesRange':'"1"',
'underlyingSymbol':'"QIHU"'
}
headers = {
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"172",
"Content-Type":"application/json; charset=utf-8",
"Cookie":"__utma=243156864.2140095760.1377925186.1386335636.1386850224.42; __utmz=243156864.1381236194.8.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=site%3Asogotrade.com%20%E6%8F%90%E6%AC%BE; BureauSwitcher=SOGO; __utmc=243156864; UserCulture=en-us; CurrentCulture=en-us; PSSO=%40%c2%a78F%c3%86%c2%b1%c5%92%26%e2%80%a6%c3%9c%c2%be%08%c2%bf%3a%09Q%40%c2%aetf%c3%93%18%e2%80%a0%1c%c2%b0%13%c2%9d%c5%bdB%04%c2%a5%c3%80%c2%aa%c2%b6%c3%8f%c6%92R%40%c3%81%c2%b5x%c3%a8b%c3%82b%c3%bb%07A%c3%a1%1fx%0ei%23%c3%8b%c3%b9%c3%ad%c3%b8%c3%8a%c2%9d%c2%ad%c3%9c%02%c3%82%c3%8fA%c3%80%c3%b8%c3%bbE%c2%a6%2ce%5d%c2%b5%c3%89%c2%afm%c2%b9Cq%27TD%c5%bd%c2%bd3%c3%b74%e2%80%a0%c3%b5CQ%06O%c3%a8q%c3%8c%c3%ba-m%e2%80%a6%14%15%e2%80%b97S%c3%8c%c3%a6%c3%ba%c3%83%c3%a1%e2%80%93%e2%80%ba%1b-T%19%c2%be%00%c3%af%c3%8bkk%07x3%1e%3f%c3%b4%c2%acI%c3%81%e2%80%a1%c3%92%e2%80%9a%00Z%e2%80%a6%c2%a9b%c2%a9%3b%c2%ac%11i%1fu%e2%80%a6%c3%9c2J%c3%a0%7c%e2%80%9d%15%c3%b0N9%c3%b0%c2%ae%e2%84%a2%06%23%7fV%c3%b6%c3%99%c3%b1%c2%a3%c2%ba%c2%8f%c2%90%c3%ab%00e%2b%c3%99%40%c2%be%16O%c3%b7%c2%aa%2f%c2%b5%c3%bf%c3%9e%c3%85%25%c3%a7j%c2%b9qW%e2%80%b0%c2%bdN%c3%b1%c3%86tR%e2%80%94a%e2%80%93%c2%b8%16%c3%bc)%c5%93%3b%2cn%c2%ad%c3%b3r0m%c3%a3%c2%bf%02%c3%a19%c2%81%c5%be%c3%bc!%c2%bcw%c3%8e%c3%b5%e2%80%94%c2%ab%02X%c3%9f%c3%b3%23%c2%90%e2%80%a1%c3%b0%c3%ab%c2%af%c2%b0%c2%acK%c2%b57F%c2%a8%3c%c5%92d0%c5%a0f; StockSelectAuthCookie=B93B2A719E01475CC32738C5B1590E9A3491F58433CE11454E18F1AEB80CC184213C600301F3381C9DB3E666AB88717D1F1DAA9D3403EB00560961DEF684BFE8A0E5969F9BF13F89EBD3C0415E0569F74ED3542E154D6C2379AEE6C8FE007DE9F78F9546FCA948B7C1BFBC1CE18BF0B7D58CDD950943DA6B8B991E2927D5EC793A78A4910DEE87A701A1DD10AC1E9ADF6405AF26; ASP.NET_SessionId=okx1hvgg5akyqtd1djzh2xi3; Exp=false; TradeBottomTabIndex=0; ctl00_mc_ac_QuickQuotePane_QuickQuote1_stockChartGOOG=0",
"Host":"options.sogotrade.com",
"Pragma":"no-cache",
"Referer":"http://options.sogotrade.com/Chain.aspx",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0"
           } 
url_values=urllib.parse.urlencode(data)  
#print(url_values)  
  
url_values=url_values.encode(encoding='UTF8')  
full_url=urllib.request.Request(url,url_values,headers)  
#or ony one sentense:full_url=url+'?'+url_values  
  
try:  
    response=urllib.request.urlopen(full_url)   #open=urlopen  
except HTTPError as e:  
    print('Error code:',e.code)   
except URLError as e:  
    print('Reason',e.reason)  
the_page=response.read()  
print(the_page)