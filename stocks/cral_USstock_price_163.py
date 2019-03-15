# coding:utf-8
from __future__ import with_statement
import requests,os,time,math,sys,json
import mySQLClass,datetime
from utc2local import local2utc
#初始化参数

cur = mySQLClass.MySQLClass('127.0.0.1',3306,'root','814155356Mysql')
cur.connectDB()
cur.selectDB('optionAna')

def getMain():
    ctime = int(time.time())
    date = datetime.datetime.today()
    date = str(local2utc(date,-21)).split(' ')[0] + ' 00:00:00'
    typenames = ['nasdaq','newyork']
    for typename in typenames:
        url = 'http://quotes.money.163.com/us/service/usrank.php?host=/us/service/usrank.php&page=0&query=UPDATE:_exists_true;PRICE:_exists_true;typename:' + typename + '&fields=no,SYMBOL,NAME,PRICE,UPDOWN,PERCENT,WEEK52_HIGH,WEEK52_LOW,TCAP,PE,VOLUME&sort=PERCENT&order=desc&count=5000&type=query&callback=callback_1074842233&req=02057'
        response = requests.get(url)
        try:
            dicR = json.loads(response.text[20:-1].replace('\\','').replace('\r','').replace('\n',''))
        except Exception,e:
            print e
            print response.text.split("(")[1].split(")")[0].replace('\\','').replace('\r','').replace('\n','')[99600:1002000]
        for stockDetail in dicR['list']:
            sqlSelect = 'select price from stocks where date=\'' + date +'\' and stockName=\'' + stockDetail['SYMBOL'] +'\';'
            isIn = cur.selectData(sqlSelect)
            if len(isIn)==0:
                sql = 'insert into stocks (stockName,price,vol,date,ctime) values (\'' + stockDetail['SYMBOL'] + '\', ' + str(stockDetail['PRICE']) + ',' + str(stockDetail['VOLUME']) + ', \'' + date + '\',' + str(ctime) + ');'
            elif float('%0.2f'%isIn[0][0])==float('%0.2f'%stockDetail['PRICE']):
                continue
            else:
                print float('%0.2f'%isIn[0][0]),float('%0.2f'%stockDetail['PRICE'])
                sql = 'UPDATE stocks set price=' + str(stockDetail['PRICE']) + ', volume=' + str(stockDetail['VOLUME']) + ', ctime='+ str(ctime) +' WHERE date=\'' + date +'\' and stockName=\'' + stockDetail['SYMBOL'] +'\';'
            try :
                cur.executeDB(sql)
            except Exception,e:
                print e
    cur.closeDB()

'''
#获取最新相关信息
def getInfo():
    
    global avgLasts
    
    stocksDetails = {}
    
    #date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    
    global dates
    #print dates
    
    
    #读取自选股配置文件
    with open("stocks.conf",'r') as stocks:
        for stockNum in stocks:
            print stockNum
            stocksDetails[stockNum] = {}
            stockNum = stockNum[:-1]
            for date in dates:
                date = date[0]
                if date <= '2013-04-01':
                    continue
                for last in avgLasts:
                    try :
                        #dateEarly = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400*(last-1)))
                        sql = 'select priceEnd from zhulidongxiang where stockNum = \'' + stockNum + '\' and date <= \'' + date + '\' order by date desc limit ' + str(last) + ';'
                        #sql = 'select avg(priceEnd),count(1) days from zhulidongxiang where stockNum = \'' + stockNum + '\' and (date between \'' + dateEarly + '\' and \'' + date + '\');'
                        #print sql
                        result = cur.selectData(sql)
                        #print list(result)
                        sum = 0
                        if len(result) == last:
                            for r in result:
                                r = list(r)
                                sum = sum + r[0]
                                #stockNum,date,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent,ma_five,ma_ten,ma_twenty,ma_thirty,ma_sixty = r
                                #print stockNum,date,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent,ma_five,ma_ten,ma_twenty,ma_thirty,ma_sixty
                            avg = sum/len(result)
                        else:
                            avg = 0
                        sqlUpdate = 'update zhulidongxiang set ' + avgLasts[last] + ' = ' + str(avg) + ' where stockNum = \'' + str(stockNum) + '\' and date = \'' + date + '\';'
                        cur.executeDB(sqlUpdate)
                    except Exception,e:
                        print e
                        print sql
                        print sqlUpdate
                        continue
                #sys.exit()
                cur.commit()
                

#计算变化率
def caculateChanges():
    global avgLasts,dates
    with open("stocks.conf",'r') as stocks:
        for stockNum in stocks:
            print stockNum
            stocksDetails[stockNum] = {}
            stockNum = stockNum[:-1]
            for date in dates:
                date = date[0]
                if date <= '2013-04-01':
                    continue
                for last in avgLasts:
                    sql = 'select stockNum,date,priceEnd,priceChange,ma_five,ma_ten,ma_twenty,ma_thirty,ma_sixty'
'''

if __name__ == "__main__":
    getMain()