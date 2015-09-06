#coding=utf-8  
import smtplib,email,sys  
from email.Message import Message

class Email:
    
    smtpserver='smtp.163.com'  
    smtpuser='hfutsuchao@163.com'  
    smtppass=''  
    smtpport='25'
    to='18600219332@qq.com'  
    server=''
    subj=''
    content=''
    frm=''

    def __init__(self,sender='hfutsuchao@163.com',smtpserver='smtp.163.com',password=''):
        self.smtpserver=smtpserver
        self.smtpuser=sender
        self.smtppass=password
        self.connect()

    def connect(self):  
        "connect to smtp server and return a smtplib.SMTP instance object"  
        self.server=smtplib.SMTP(self.smtpserver,self.smtpport)
        self.server.ehlo()  
        self.server.login(self.smtpuser,self.smtppass)
          
    def sendEmail(self,subj=subj,content=content,to=to,frm=frm): 
        print subj,content
        #"using server send a email"
        msg = Message()  
        msg['Mime-Version']='1.0'  
        if frm == '':
            msg['From'] = self.smtpuser
        else:  
            msg['From'] = frm
        msg['To'] = to  
        msg['Subject'] = subj  
        msg['Date'] = email.Utils.formatdate()          # curr datetime, rfc2822  
        msg.set_payload(content)
        try:
            failed = self.server.sendmail(msg['From'],msg['To'],str(msg))   # may also raise exc  
            print "send success! OK!"  
        except Exception ,ex:
            print Exception,ex  
            print 'Error - send failed'

    def getSummary(self):
        '''
        frm=raw_input('From: ').strip()  
        to=raw_input('To: ').strip()  
        subj=raw_input('Subj: ').strip()
        '''
        print 'Type message text, end with line="."'
        while True:
            line = sys.stdin.readline()  
            if line == '. ': break  
            self.text += line

if __name__=="__main__":     
    myMail = Email()
    myMail.sendEmail('subj','content','814155356@qq.com')
