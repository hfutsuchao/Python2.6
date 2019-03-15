# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys,os

#new
msg = MIMEMultipart()

#add att
if len(sys.argv) == 1:
    print "Add Att"
    exit()
for i in range(1,len(sys.argv)):
    fp = sys.argv[i]
    fn = fp.split('/')[-1]
    att = MIMEText(open(fp, 'rb').read(), 'base64', 'gb2312')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="' + fn + '"'
    print fn
    msg.attach(att)

#mail head
msg['to'] = 'nealspw3@kindle.cn'
msg['from'] = 'hfutsuchao@163.com'
msg['subject'] = 'convert'

#send mail
try:
    server = smtplib.SMTP()
    server.connect('smtp.163.com')
    server.login('hfutsuchao','814155356')
    server.sendmail(msg['from'], msg['to'],msg.as_string())
    server.quit()
    print 'Success!'
except Exception, e:  
    print str(e)