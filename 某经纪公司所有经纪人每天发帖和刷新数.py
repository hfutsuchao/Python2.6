# coding: gbk
import os,MySQLdb,time
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3320,db="house_premier",charset="GBK")

date1 = ['house_source_rent_premier','house_source_share_premier','house_source_sell_premier','house_source_loupan_premier']
date2 = ['house_source_storerent_premier','house_source_storetrade_premier','house_source_officerent_premier','house_source_officetrade_premier']
date3 = ['house_source_plant_premier']
sql = 'SELECT AccountId,accountName,BussinessScope FROM gcrm.customer JOIN gcrm.customer_account USING(CustomerId) WHERE CompanyName = "上海中原房地产经纪有限公司"'
cursor = conn.cursor()
cursor.execute(sql)
dicAccount = {}
for row in cursor.fetchall():
    AccountId = row[0]
    accountName = row[1]
    BussinessScope = row[2]
    dicAccount[AccountId] = accountName + '\t' + str(BussinessScope)
'''
dic = {}
for accountId in dicAccount.keys():
    accountName,BussinessScope = dicAccount[accountId].split('\t')
    for d in range(1,7):
        dic['2012-12-02'] = 1
        dic['post'] = {}
        dic['刷新'] = {}
        dic['post'][accountId] = {}
        dic['刷新'][accountId] = {}
        dic['post'][accountId][d] = 0
        dic['刷新'][accountId][d] = 0
'''
for AccountId in dicAccount.keys():
    accountName,BussinessScope = dicAccount[AccountId].split('\t')
    cursor.execute('SET NAMES GBK;')
    if BussinessScope == '1':
        #print accountName
        for field in date1:
            sql = 'SELECT SUBSTR(FROM_UNIXTIME(post_at),9,2) 日期,COUNT(1) FROM '+field+' WHERE account_id='+str(AccountId)+' AND post_at>=UNIX_TIMESTAMP("2012-12-14") and image_count>=4 GROUP BY 日期'
            #print sql
            cursor.execute(sql)
            for row in cursor.fetchall():
                print('发帖'+'\t'+accountName+'\t'+str(row[0])+'\t'+str(row[1]))
                #pass
    elif BussinessScope == '2':
        for field in date2:
            sql = 'SELECT SUBSTR(FROM_UNIXTIME(post_at),9,2) 日期,COUNT(1) FROM '+field+' WHERE account_id='+str(AccountId)+' AND post_at>=UNIX_TIMESTAMP("2012-12-14") and image_count>=4 GROUP BY 日期'
            cursor.execute(sql)
            for row in cursor.fetchall():
                print('发帖'+'\t'+accountName+'\t'+str(row[0])+'\t'+str(row[1]))
                #pass
    elif BussinessScope == '3':
        for field in date2:
            sql = 'SELECT SUBSTR(FROM_UNIXTIME(post_at),9,2) 日期,COUNT(1) FROM '+field+' WHERE account_id='+str(AccountId)+' AND post_at>=UNIX_TIMESTAMP("2012-12-14") and image_count>=4 GROUP BY 日期'
            cursor.execute(sql)
            for row in cursor.fetchall():
                print('发帖'+'\t'+accountName+'\t'+str(row[0])+'\t'+str(row[1]))
                #pass
'''
sql = 'SELECT SUBSTR(FROM_UNIXTIME(RefreshAt),9,2) 日期,accountId,COUNT(1) FROM house_premier.house_premier_refresh WHERE accountId in (SELECT AccountId FROM gcrm.customer JOIN gcrm.customer_account USING(CustomerId) WHERE CompanyName = "上海中原房地产经纪有限公司") AND RefreshAt>=UNIX_TIMESTAMP("2012-12-14") GROUP BY 日期,accountId'
cursor.execute(sql)
for row in cursor.fetchall():
    print('刷新'+'\t'+str(row[0])+'\t'+str(row[1])+'\t'+str(row[2]))
'''