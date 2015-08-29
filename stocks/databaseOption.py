#coding:utf-8
import mySQLClass,sys

cur = mySQLClass.MySQLClass('localhost',3306,'root','814155356Mysql')
cur.connectDB()
cur.selectDB('optionAna')
sql = 'drop table option_most_active;'
cur.selectData(sql)
sql = 'CREATE TABLE option_most_active(id int auto_increment primary key not null,stockName VARCHAR(30) NOT NULL,optionSymbol VARCHAR(50) NOT NULL,expired datetime not NULL,strike float not NULL,optionType char(4) NOT NULL,bid float NOT NULL,ask float NOT NULL,vol int not NULL,openInt int not NULL,date datetime not NULL,ctime int NOT NULL);'
cur.selectData(sql)
sys.exit()
