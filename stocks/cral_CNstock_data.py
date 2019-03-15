#coding:utf-8
from sqlalchemy import create_engine
import tushare as ts
from sqlalchemy.orm import sessionmaker
import time,datetime
from commfunction import today,date_add

fw = open('stock_date.txt','w')
today_date = date_add(str(today()),-1)

DB_CONNECT_STRING = 'sqlite:///stock_CN_data.db'
engine = create_engine(DB_CONNECT_STRING,echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

codeDatas = session.execute('select * from publish_date where code="002230";').fetchall()

for data in codeDatas[:1]:
    code, time_to_market = data
    print code, time_to_market
    try:
        lastdate = session.execute('select date from day_k_data where code="'+code+'" order by date desc limit 1;').first()[0]
    except Exception,e:
        #print e
        try:
            lastdate = date_add(str(time_to_market),0,'%Y%m%d')
        except:
            lastdate = date_add(str(today_date),-1095,'%Y-%m-%d')
    while lastdate<=today_date:
        todate = date_add(str(lastdate),1095,'%Y-%m-%d')
        if todate >= today_date:
            todate = today_date
        print code, lastdate, todate
        df = ts.get_h_data(code,start=lastdate,end=todate)
        df.insert(0,'code',code)
        df.to_sql('day_k_data',engine,if_exists='append')
        lastdate = date_add(str(todate),1,'%Y-%m-%d')
r = session.execute('select code,count(1) from day_k_data group by code order by date desc;').fetchall()
'''for line in r:
    fw.write(str(line) + '\n')'''
print len(r)