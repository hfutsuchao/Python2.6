#coding:utf-8
from sqlalchemy import create_engine
import tushare as ts
from sqlalchemy.orm import sessionmaker
df = ts.get_stock_basics()
df = df.ix[:]['timeToMarket']
DB_CONNECT_STRING = 'sqlite:///stock_CN_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
df.to_sql('publish_date',engine,if_exists='append')
r = session.execute('select * from publish_date;').fetchall()
print len(r)