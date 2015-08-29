# coding:gbk
from __future__ import with_statement
#from PyWapFetion import Fetion, send2self, send
import urllib2,re,os,time,math,sys,mySQLClass

#初始化参数

cur = mySQLClass.MySQLClass('127.0.0.1',3306,'root','123654')
cur.connectDB()
cur.selectDB('mystocks')

#获取主力资金排行



def getMain():
    url = 'http://data.eastmoney.com/zjlx/data.aspx?type=detail&cate=0&day=1&sortType=6&sortRule=-1&jsname=jLRntlCa&pageSize=50000&page=1&rt=45738765'
    
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except:
        print url,'open error!'
        pass
    stocksDetails = html.split('["')[1].split('"]')[0].split('","')
    #print len(stocksDetail)
    
    stockSource = open("stocks.conf",'w')
    
    for stockDetail in stocksDetails:
        stockNum,r1,r2,stockName,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent = stockDetail.split(',')
        stockSource.write(stockNum + '\n')
    stockSource.close()

#获取最新相关信息
def getInfo():
    
    #读取自选股配置文件
    with open("stocks.conf",'r') as stocks:
        for stockNum in stocks:
            stockNum = stockNum[:-1]
            
            myurl = 'http://data.eastmoney.com/zjlx/'+ stockNum +'.html'
            try:
                response = urllib2.urlopen(myurl)
                html = response.read()
            except:
                print stockNum
                continue
            #print html
            #tmp = re.findall("<tr (class=\"odd\" )?onmouseover=\"this.className=\'over\'\"  onmouseout=\"this.className=\'(odd)?\'\">\s*<td>(.{10}?)</td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"red\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\"green\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"green\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\"green\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\"green\">(.*?)%</span></td>\s*</tr>",html)
            tmp = re.findall("<tr (class=\"odd\" )?onmouseover=\"this.className=\'over\'\"  onmouseout=\"this.className=\'(odd)?\'\">\s*<td>(.{10}?)</td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)%</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)</span></td>\s*<td class=\"tdnumber\"><span class=\".{0,5}\">(.*?)%</span></td>\s*</tr>",html)
            for t in tmp:
                t = list(t)
                #print t
                for i in range(0,len(t)):
                    if t[i].find("万") != -1:
                        t[i] = t[i][:-2]
                    if t[i].find("亿") != -1:
                        t[i] = str(float(t[i][:-2])*10000)
                    if t[i].find("%") != -1:
                        t[i] = t[i][:-1]
                #print t,ss
                r1,r2,date,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent = t
                #sql = 'insert into zhulidongxiang (stockNum,date,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent) values( \'' + stockNum + '\',\'' + date + '\',' + priceEnd + ',' + priceChange[:-1] + ',' + zl_countAll[:-2] + ',' + zl_countPercent + ',' + cd_countAll[:-2] + ',' + cd_countPercent + ',' + d_countAll[:-2] + ',' + d_countPercent + ',' + z_countAll[:-2] + ',' + z_countPercent + ',' + x_countAll[:-2] + ',' + x_countPercent + ');'
                sql = 'insert into zhulidongxiang (stockNum,date,priceEnd,priceChange,zl_countAll,zl_countPercent,cd_countAll,cd_countPercent,d_countAll,d_countPercent,z_countAll,z_countPercent,x_countAll,x_countPercent) values( \'' + stockNum + '\',\'' + date + '\',' + priceEnd + ',' + priceChange + ',' + zl_countAll + ',' + zl_countPercent + ',' + cd_countAll + ',' + cd_countPercent + ',' + d_countAll + ',' + d_countPercent + ',' + z_countAll + ',' + z_countPercent + ',' + x_countAll + ',' + x_countPercent + ');'
                try :
                    cur.executeDB(sql)
                except:
                    print t,sql
                    pass
                cur.commit()
        cur.closeDB()

if __name__ == "__main__":
    getMain()
    getInfo()