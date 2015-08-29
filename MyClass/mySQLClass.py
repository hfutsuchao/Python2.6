#!/usr/bin/python
#coding:utf-8
import MySQLdb
class MySQLClass:
        user = ''
        host = ''
        passwd = ''
        port = 3306
        DB = ''
        cur = ''
        sql = ''

        def __init__(self,host,port,user,passwd):
                self.user = user
                self.host = host
                self.passwd = passwd
                self.port = port
        def connectDB(self):
                self.conn=MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd)
                self.cur=self.conn.cursor() 
        def selectDB(self,DB):
                self.DB = DB
                self.conn.select_db(self.DB)

#提交      
        def commit(self):
                self.conn.commit()   #提交

#Create, Insert, Drop,Delete,Alter,等SQL语句

        def executeDB(self,sql):
                self.sql = sql
                result = self.cur.execute(self.sql)
                self.commit()
                return result 
                
#Select查询
        def selectData(self,sql):
                self.sql = sql
                self.cur.execute(self.sql)
                return self.cur.fetchall()  #返回结果集
#关闭库，关闭游标      
        def closeDB(self):
                self.cur.close()   #关闭游标   
                #print self.cur    #查看游标状态
                self.conn.close() #关闭数据库
                #print self.conn  #查看数据库
#析构函数
        def __del__(self):
                #print "析构成功！"
                pass
