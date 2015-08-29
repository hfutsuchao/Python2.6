#coding:gbk
import sys,mySQLClass,time,json,os

os.system("color f0")

#print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
dateToday = time.strftime('%Y-%m-%d',time.localtime(time.time()))
dateYesterday = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400))
cur = mySQLClass.MySQLClass('192.168.116.20',3320,'lixueshi','i14p4Dkyd')
cur.connectDB()
cur.selectDB('house_premier')

if len(sys.argv)>1:
    dateSerch = sys.argv[1]
    email = sys.argv[2]
else:
    dateSerch = raw_input('刷新专用，只查当月，输入查询日期，（3~27号之间）示例 14:\n')
    email = raw_input('Customer acount:')

if dateSerch == '':
    dateSerch = dateYesterday
elif len(dateSerch) == 2:
    dateSerch = dateToday[:-2] + dateSerch
elif len(dateSerch) == 1:
    dateSerch = dateToday[:-2] + '0' + dateSerch

day = [31, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 ,31]

dateStart = dateSerch[:-2] + str (day[int(dateSerch[-2:]) - 3])

dateEnd = dateSerch[:-2] + str (day[int(dateSerch[-2:]) + 1])

#print dateStart,dateEnd

import html

params = {"UserName":"suchao","Domain":"@ganji.com","Password":"hFuT814155356134"}
url = "http://sso.ganji.com/Account/LogOn"

crm = html.Html()
crm.post(url,params,"")

if not email :
    sys.exit()

params = {'[Equal]Email':email,'accountListType':'2','page':'1','pagesize':'20','sortname':'CreatedTime','sortorder':'desc','unnamed':'none'}
url = "http://gcrm.ganji.com/HousingAccount/Items?listType=ForManagers"

creatorId = json.loads(crm.post(url,params,""))['Rows'][0]['Id']

crm.clear()

#operationTypeNum = raw_input('查找操作类型: 0->精品刷新     1->放心房刷新     2->发布/删除帖子     3->推广/取消推广     4->自定义\n')

operationTypes = {"user-edit":"编辑房源","user-add-refresh":"新增精品刷新","user-del-refresh":"取消精品刷新", "user-add-refresh-assure":"新增放心房刷新","user-del-refresh-assure":"取消放心房刷新", "user-add":"发布房源","user-delete":"删除房源", "user-start-premier":"参与推广","user-cancel-premier":"取消推广",'user-del-repeat-house':"取消选择推广期内重复刷新",'user-add-repeat-house':"设置推广期内重复刷新"}

cur.executeDB('set names "gbk";')

#if operationTypeNum != "4":
    #sql = 'select creatorName,operationType,createdTime from house_source_operation where creatorId= '+ creatorId +' and operationType in (' + operationTypes[operationTypeNum] + ') and (createdTime BETWEEN \"' + dateStart + '\" and \"' +dateEnd  + '\") and (message LIKE \"' + dateSerch + '%\" or createdTime = \"' + dateSerch + '\" )'
#sql = "SELECT SUBSTR(CreatedTime,1,10) 日期,creatorname 客户名称,operationtype 操作类型,COUNT(1) 刷新次数 FROM house_premier.house_source_operation WHERE creatorID=" + creatorId + " AND (createdTime BETWEEN \'" + dateStart + "\' and \'" +dateEnd  + "\') AND (message LIKE \'" + dateSerch + "%\' or createdTime LIKE \'" + dateSerch + "%\') GROUP BY SUBSTR(CreatedTime,1,10),OperationType ORDER BY createdtime DESC;"
sql = "SELECT SUBSTR(CreatedTime,1,10),creatorname,operationtype,COUNT(1) FROM house_premier.house_source_operation WHERE creatorID=" + creatorId + " AND (createdTime BETWEEN \'" + dateStart + "\' and \'" +dateEnd  + "\') AND (message LIKE \'" + dateSerch + "%\' or createdTime LIKE \'" + dateSerch + "%\') GROUP BY SUBSTR(CreatedTime,1,10),OperationType ORDER BY createdtime DESC;"
#sql = "SELECT SUBSTR(CreatedTime,1,10) 日期,creatorname 客户名称,operationtype 操作类型,COUNT(1) 操作次数 FROM house_premier.house_source_operation WHERE creatorID=184105 AND (createdTime BETWEEN '2013-08-1' AND '2013-09-1') AND (message LIKE '2013-08-%' OR createdTime LIKE '2013-08-%') GROUP BY SUBSTR(CreatedTime,1,10),OperationType ORDER BY createdtime DESC;"
#print sql

tmpFile = open("tmpFile.csv",'w')

print "\n\n日期\t客户姓名\t操作类型\t操作次数"
tmpFile.write("日期,客户姓名,操作类型,操作次数\n")
for r in cur.selectData(sql):
    try:
        print r[0] + '\t' + r[1] + '\t' + operationTypes[r[2]] + '\t' + str(r[3])
        tmpFile.write(r[0] + ',' + r[1] + ',' + operationTypes[r[2]] + ',' + str(r[3]) + '\n')
    except:
        print r[0] + '\t' + r[1] + '\t' + r[2] + '\t' + str(r[3])
        tmpFile.write(r[0] + ',' + r[1] + ',' + r[2] + ',' + str(r[3]) + '\n')
print "\n\n" + sql

tmpFile.close()
os.system('start tmpFile.csv')
os.system('refreshCheck.py')

cur.closeDB()