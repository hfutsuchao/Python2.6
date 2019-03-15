#!/usr/bin/python
#coding:gbk
import mySQLClass

class WMDB(mySQLClass.MySQLClass):
    def __init__(self):
        pass
        
    def ms(self):
        mySQLClass.MySQLClass.__init__(self,'10.88.23.11',3306,'wanduoduo-r','v&sU+9IcUU')
        mySQLClass.MySQLClass.connectDB(self)
        
    def rp(self):
        mySQLClass.MySQLClass.__init__(self,'10.88.23.107',3306,'tongji-r','lqRZbkx=kM')
        mySQLClass.MySQLClass.connectDB(self)  
    
if __name__ == "__main__":
    sqlHandle = WMDB()
    sqlHandle.ms()
    #sqlHandle.selectDB('ms')
    print sqlHandle.selectData('select * from house_source_rent limit 1;')
