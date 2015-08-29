#encoding:utf-8
import json
import html
import time


url = 'http://www.ganji.com/ajax.php?module=streetOptions'



def getDistrictId(districtName,cityId):
    import GJDB
    DB = GJDB.GJDB()
    DB.management()
    DB.selectDB('management')
    DB.selectData('set names utf8')
    return DB.selectData('SELECT district_id FROM district WHERE short_name="'+districtName+'" and city_id='+str(cityId))[0][0]

def getcityDomain(cityName):
    import GJDB
    DB = GJDB.GJDB()
    DB.management()
    DB.selectDB('management')
    DB.selectData('set names utf8')
    return DB.selectData('SELECT domain FROM city WHERE short_name="'+cityName+'"')[0][0]

def getCityId(cityName):
    import GJDB
    DB = GJDB.GJDB()
    DB.management()
    DB.selectDB('management')
    DB.selectData('set names utf8')
    return DB.selectData('SELECT city_id FROM city WHERE short_name="'+cityName+'"')[0][0]


htmlHandle = html.Html()

streetAddFile = open('newds.txt','r').readlines()
for streetAdd in streetAddFile[1:]:
    city, district, street = streetAdd.split('-')
    try:
        data = {
                'district_id':str(getDistrictId(district,getCityId(city))),
        'domain':getcityDomain(city),
        'with_all_option':'1'
                }
    except Exception,e:
        print streetAdd[:-1],'no data',e
        continue
    result = json.loads(htmlHandle.post(url,data,''))
    for i in result:
        tmp = 1
        tmpArr = []
        try:
            if street[:-1] == i[1]:
                tmp = 0
                break
            if i[3] not in tmpArr:
                tmpArr.append(i[3])
            else:
                print streetAdd[:-1],"script_index error!"
        except:
            print result
    if tmp:
        print streetAdd[:-1],"error!"
    #time.sleep(1)
