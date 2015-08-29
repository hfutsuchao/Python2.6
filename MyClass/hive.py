#coding:utf-8
import html,time
from BeautifulSoup import BeautifulSoup

dateToday = time.strftime('%Y-%m-%d',time.localtime(time.time()))

class Hive():
    
    paramsLogin = {"UserName":"suchao","Domain":"@ganji.com","Password":""}
    urlLogin = "http://sso.ganji.com/Account/LogOn"
    urlPost = 'http://hive.corp.ganji.com:8080/portal/job/create.do'
    urlGet = 'http://hive.corp.ganji.com:8080/portal/job/history.do'
    params = ''
    sql = ''
    desc = ''
    session_name = ''
    outContent = ''
    hive = ''
    
    def __init__(self):
        #Login
        self.hive = html.Html()
        self.hive.post(self.urlLogin,self.paramsLogin,"")
    
    def select(self,sql,desc,session_name):
        
        self.sql = sql
        self.desc = desc
        self.session_name = session_name
        
        #Execute SQL
        self.params = {
                    'commit':'commit',
                    'description':self.desc,
                    'session_name':self.session_name,
                    'sql':self.sql
                   }
        
        self.hive.post(self.urlPost,self.params,"")
        
    def getList(self):
        return self.hive.get(self.urlGet,"")

    def getData(self):
        soup = BeautifulSoup(self.getList())
        for tr in soup.tbody.findAll('tr'):
            trs = tr.findAll('td')
            try:
                outDesc = trs[1].contents[0]
                outTime = trs[3].contents[0]
                outUrl = trs[4].contents[0].get('href')
            except Exception,e:
                print e
                continue
            #Loop To Get Data
            if outDesc == self.desc:
                if outTime >= dateToday:
                    return self.hive.download(outUrl,'data/'+self.desc+'.txt')
                else:
                    time.sleep(5)
                    return self.getData()
                break

#使用示例
if __name__ == "__main__":
    sql = 'select * from web_pv_log_detail3 where dt = "2012-08-08" limit 10;'
    desc = 'SEOCount'
    session_name = 'SEOCountS'
    
    hive = Hive()
    hive.select(sql, desc, session_name)
    print hive.getData()
