#coding:utf-8
import mySQLClass,sys

cur = mySQLClass.MySQLClass('localhost',3306,'root','814155356Mysql')
cur.connectDB()
cur.selectDB('optionAna')
sql = 'drop table stocks;'
cur.selectData(sql)
sql = 'CREATE TABLE stocks(id int auto_increment primary key not null,stockName VARCHAR(30) NOT NULL,price float NOT NULL,dif float DEFAULT 0.0 NOT NULL,dea float DEFAULT 0.0 NOT NULL,macd float DEFAULT 0.0 NOT NULL,vol int not NULL,date datetime not NULL,ctime int NOT NULL);'
cur.selectData(sql)
cur.closeDB()
