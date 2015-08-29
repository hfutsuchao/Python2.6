#coding:utf-8
import MySQLdb,urllib,re

comments = open('C:\\Users\\suchao\\Desktop\\pj.txt').readlines()
result = open('C:\\Users\\suchao\\Desktop\\commentResult.txt','w')

conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="utf8")
for comment in comments:
    ip,t,curTime,pRef,phone,cookie,sRef,caName,keyword,houseId,date = comment.split('\t')
    cursor = conn.cursor()
    sql = 'select replace(content,char(10),\'\'),comment_type,audit_status,ip,uuid from house_premier.house_comment where house_id='+houseId+' and user_phone='+phone
    #+' and post_at>='+str(int(int(curTime)/1000)-10)+' and post_at<='+str(int(int(curTime)/1000)+10)
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.write(t+'\t'+pRef+'\t'+sRef+'\t'+caName+'\t'+keyword+'\t'+row[0]+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])+'\n')
    except:
        print sql