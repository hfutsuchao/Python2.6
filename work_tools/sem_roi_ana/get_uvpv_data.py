#coding:utf-8
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import sessionmaker
date = [('2018-02-22','2018-03-22'),('2019-02-11','2019-03-11')]
#date = [('2017-01-01','2017-07-01'),('2017-07-01','2018-01-01'),('2018-01-01','2018-07-01'),('2018-07-01','2019-03-01')]
#date = [('2017-07-01','2017-07-15'),('2017-07-15','2017-08-01')]
#date = [('2017-08-01','2017-08-15'),('2017-08-15','2017-09-01')]
df = pd.DataFrame()

def get_data(sql):
	DB_CONNECT_STRING = 'mysql+pymysql://suchao:8573b7c@bw-real-db-01.corp.haozu.com:3301/operation'
	engine = create_engine(DB_CONNECT_STRING,echo=False)
	DB_Session = sessionmaker(bind=engine)
	session = DB_Session()
	df = pd.read_sql(sql,engine)
	session.close()
	print df.head()
	return df

for d in date:
	#sql = "select date,ctime,cityId,uid,keywordId,url,refer from sem_action_log where date>='" + d[0] + "' and date<'" + d[1] + "' order by date asc;"
	sql = "select substr(date,1,10) dt,uid from sem_action_log where date>='" + d[0] + "' and date<'" + d[1] + "' and cityId in (45) and category in (1) and keywordId<>'';"
	df = pd.concat([df,get_data(sql)])
df.to_csv('./uvlog.csv')