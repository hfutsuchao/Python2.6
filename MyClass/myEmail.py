#coding=utf-8  
  
import smtplib,email,sys  
from email.Message import Message  
  
  
smtpserver='smtp.163.com'  
smtpuser='hfutsuchao@163.com'  
smtppass=''  
smtpport='25'  
  
def connect():  
    "connect to smtp server and return a smtplib.SMTP instance object"  
    server=smtplib.SMTP(smtpserver,smtpport)  
    server.ehlo()  
    server.login(smtpuser,smtppass)  
    return server  
      
def sendmessage(server,subj,content,to,frm=''): 
    #"using server send a email"
    msg = Message()  
    msg['Mime-Version']='1.0'  
    if frm == '':
        msg['From'] = smtpuser
    else:  
        msg['From'] = frm
    msg['To'] = to  
    msg['Subject'] = subj  
    msg['Date'] = email.Utils.formatdate()          # curr datetime, rfc2822  
    msg.set_payload(content)
    try:
        failed = server.sendmail(msg['From'],msg['To'],str(msg))   # may also raise exc  
        print "send success! OK!"  
    except Exception ,ex:
        print Exception,ex  
        print 'Error - send failed'

def getSummary():
    '''
    frm=raw_input('From: ').strip()  
    to=raw_input('To: ').strip()  
    subj=raw_input('Subj: ').strip()
    '''
    print 'Type message text, end with line="."'
    while True:
        line = sys.stdin.readline()  
        if line == '. ': break  
        text += line
    return text

if __name__=="__main__":     
    to='18600219332@qq.com'  
    subj='test'  
    text = 'test'
    server=connect()
    sendmessage(server,subj,text,to)
