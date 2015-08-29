#!/usr/bin/python
#coding:gbk
import mySQLClass

class GJDB(mySQLClass.MySQLClass):
    def __init__(self):
        pass
    
    def qa(self):
        mySQLClass.MySQLClass.__init__(self,'10.3.255.21',3310,'lixueshi','i14p4Dkyd')
        mySQLClass.MySQLClass.connectDB(self)
        
    def ms(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3310,'yangyu','c1b78739d')
        mySQLClass.MySQLClass.connectDB(self)
        
    def management(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3311,'yangyu','c1b78739d')
        mySQLClass.MySQLClass.connectDB(self)
    
    def crawl(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3382,'suchao','CE7w7pTNB')
        mySQLClass.MySQLClass.connectDB(self)
    
    def rp(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3380,'lixueshi','i14p4Dkyd')
        mySQLClass.MySQLClass.connectDB(self)
    
    def tg(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3328,'suchao','CE7w7pTNB')
        mySQLClass.MySQLClass.connectDB(self)
    
    def gcrm(self):
        mySQLClass.MySQLClass.__init__(self,'g1-off-ku-real.dns.ganji.com',3320,'lixueshi','i14p4Dkyd')
        mySQLClass.MySQLClass.connectDB(self)
    
    def bin(self):
        mySQLClass.MySQLClass.__init__(self,'192.168.128.9',3306,'suchao','CE7w7pTNB')
        mySQLClass.MySQLClass.connectDB(self)  
    
if __name__ == "__main__":
    sqlHandle = GJDB()
    sqlHandle.qa()
    sqlHandle.selectDB('archive')
    print sqlHandle.selectData('select * from house_source_rent limit 1;')