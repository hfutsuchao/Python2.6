#coding:gbk
import GJDB,MySQLdb,os,time

db = GJDB.GJDB()

citys={}
conn=MySQLdb.connect(host="192.168.116.20",user="yangyu",passwd="c1b78739d",port=3311,db="management",charset="gbk")
cursor = conn.cursor()
cursor.execute('SELECT domain,pinyin FROM city;')
for row in cursor.fetchall():
    citys[row[0]]=row[1]
cursor.close()
citys['others']='others'


xiaoquResult = open('xiaoquResult.txt','w')

db.ms()
for city in citys.values():
    try:
        db.selectDB(city)
    except:
        #print city
        continue
    db.selectData('set names "gbk";')
    datas = db.selectData('select city,xiaoqu_id,district_name,street_name,xiaoqu from house_source_rent where show_time>=unix_timestamp("2013-06-20");')
    
    dic = {}
    
    for data in datas:
        city = data[0]
        xiaoqu_id = data[1]
        district_name = data[2]
        street_name = data[3]
        xiaoqu = data[4]
        group = str(city) + '_' + str(xiaoqu_id) + '_' + district_name + '_' + street_name + '_' + xiaoqu
        if group in dic:
            dic[group] = dic[group] + 1
        else:
            dic[group] = 1
    
    for group in dic:
        if dic[group] >= 3:
            data = group.split('_')
            xiaoqu_id = data[1]
            if xiaoqu_id == '0':
                xiaoquResult.write(group + '\t\t\t' + str(dic[group]) + '\n')
time.sleep(120)
#os.system('shutdown -h')