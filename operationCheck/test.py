#coding:utf-8
import sys,mySQLClass,time,html,os
import re,time,urllib2,urllib,cookielib,json

html = html.Html()
'''getCookieUrl = 'http://bj.ganji.com/fang1/'
html.get(getCookieUrl, '')
print html.cj
'''
#print a

url = "http://www.aizhufu.cn/taskmanage/save_zhufu.jhtml"

'''
tmp = BeautifulSoup.BeautifulSoup(htmlHandle.get(url, ""))(attrs={"type":"hidden"})[1]

name = tmp['name']

value = tmp['value']
'''

params = {
        'customContent':'Hello',
        'recipients':'13333219452',
        'urlRedirect':''
        }

headers = {
        'Accept':'application/json, text/javascript, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'1040',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'bdshare_firstime=1373544922045; Hm_lvt_be7a708988b27485de9881fd5e3b326a=1373544922,1373544932; Hm_lpvt_be7a708988b27485de9881fd5e3b326a=1373546010; JSESSIONID=51495E803EA447A3816A8095D1F23C38.aizhufu01',
        'Host':'www.aizhufu.cn',
        'Pragma':'no-cache',
        'Referer':'http://www.aizhufu.cn/taskmanage/input_zhufu.jhtml?contentId=26722',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0',
        'X-Requested-With':'XMLHttpRequest'
        }

print html.post(url, params, headers)

print html.cj