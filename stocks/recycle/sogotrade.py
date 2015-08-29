#coding: utf-8
import requests
import html
import json
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

url = 'http://options.sogotrade.com/Services/ChainService.asmx/GetOptions'

h2 = html.Html()
#url = 'https://account.sogotrade.com/Account/Default.aspx'
#html = requests.post(url,data=data,headers=headers)
#print h2.post(url,data,headers)

html = requests.get(url)
print html.text
