#coding:utf-8
import sys,mySQLClass,time,html,os
import re,time,urllib2,urllib,cookielib,json
from config import gjname,gjpwd

os.system("color f0")

cur = mySQLClass.MySQLClass('g1-off-ku-real.dns.ganji.com',3328,'suchao','CE7w7pTNB')
cur.connectDB()
cur.selectDB('house_premier')

import html

params = {"UserName":gjname,"Domain":"@ganji.com","Password":gjpwd}
url = "http://sso.ganji.com/Account/LogOn"

crm = html.Html()
crm.post(url,params,"")

email = raw_input('Customer acount:')

if not email :
    sys.exit()

params = {'[Equal]Email':email,'accountListType':'2','page':'1','pagesize':'20','sortname':'CreatedTime','sortorder':'desc','unnamed':'none'}
url = "http://gcrm.ganji.com/HousingAccount/Items?listType=ForManagers"

accountId = json.loads(crm.post(url,params,""))['Rows'][0]['Id']
print accountId

crm.clear()

url = "http://fangvip.ganji.com/auth.php?do=login&"
post = {"username":"aba3@163.com","password":"586586","no_cookie_test":"1"}
headers = {
        "Cookie":"GANJISESSID=2ea75b586f70b447b88094f665ed2b94; need_captcha=1; __utma=32156897.437889441.1373031223.1373031223.1373031223.1; __utmb=32156897.1.10.1373031223; __utmc=32156897; __utmz=32156897.1373031223.1.1.utmcsr=fangvip.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/auth.php"
        }

'''try:
    cookie = cookielib.CookieJar()
    cookies = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    #parms = {"UserName":"suchao","Domain":"@ganji.com","Password":"hahaha"}
    #loginUrl = "http://sso.ganji.com/Account/LogOn"
    html = urllib2.Request(
        url = url,
        data = urllib.urlencode(post),
        headers = headers
        )
    urllib2.urlopen(html)
except Exception,e:
    print(e)
    pass'''

commentHandle = html.Html()

commentHandle.post(url,post,headers)

sql = 'SELECT id,owner_id,Content,audit_status,comment_type,operate_reason,c.user_phone,c.UUID,c.user_id,FROM_UNIXTIME(post_at)  FROM house_comment c WHERE owner_id IN (' + accountId + ')'

cur.executeDB('set names gbk;')

comments = cur.selectData(sql)

bads = {}

for comment in comments:
    id,owner_id,Content,audit_status,comment_type,operate_reason,user_phone,UUID,user_id,post_at = list(comment)
    print str(id) + '\t' + str(owner_id) + '\t' + str(Content) + '\t' + str(audit_status) + '\t' + str(comment_type) + '\t' + str(operate_reason) + '\t' + str(user_phone) + '\t' + str(UUID) + '\t' + str(user_id) + '\t' + str(post_at)
    #print str(comment).encode('gbk')
    if audit_status == 0 and comment_type == 3:
        bads[str(id)] = str(id) + '\t' + str(owner_id) + '\t' + str(Content) + '\t' + str(audit_status) + '\t' + str(comment_type) + '\t' + str(operate_reason) + '\t' + str(user_phone) + '\t' + str(UUID) + '\t' + str(user_id) + '\t' + str(post_at)

print "Bad comment:"

for id in bads:
    print bads[id]

bads = ','.join(bads.keys())

print bads

ids = 'a'
#ids = raw_input("ToDo ID:")

if ids:
    if ids == 'a':
        ids = bads
    for id in ids.split(','):
        post = {'person':'苏超','reason':'恶意差评',}
        url = "http://www.ganji.com/housing/comment_management.php?action=audit&id=" + str(id)
        #ret = commentHandle.post(url,post,"")
        #print ret
        print commentHandle.post(url,post,"")
        ret = json.loads(commentHandle.post(url,post,""))
        print ret['id'] + ':' + ret['txt']
'''sql2 = 'SELECT id,owner_id,c.Content,audit_status,comment_type,c.operate_reason,c.user_phone,c.UUID,c.user_id,FROM_UNIXTIME(post_at) FROM house_comment c INNER JOIN (SELECT UUID,user_phone,user_id,content FROM house_comment WHERE id=31277) d ON (c.uuid = d.uuid OR c.user_phone = d.user_phone OR c.user_id = d.user_id OR c.content = d.content)'
tmp = cur.selectData(sql2)
print tmp'''

os.system("comment.py")

cur.closeDB()
