#coding:utf-8
from GJDB import GJDB

DB = GJDB()

DB.management()

DB.selectDB('management')

DB.selectData("set names utf8;")

#print DB.selectData("SELECT city.domain,street.street_id,street.script_index,street.street_name,street.url FROM street INNER JOIN district INNER JOIN city ON district.district_id=street.district_id AND city.city_id=district.city_id where city.short_name='北京' and district.short_name='海淀' and street.street_name='西二旗'")

with open('districtStreetM.txt','r') as streetAddFile:
    for streetAdd in streetAddFile:
        try:
            city, district, streets = streetAdd.split('\t')
        except:
            continue
        streetDic = streets[:-1].split(',')
        for street in streetDic:
            sql = "SELECT city.domain,street.street_id,street.script_index,street.street_name,street.url FROM street INNER JOIN district INNER JOIN city ON district.district_id=street.district_id AND city.city_id=district.city_id where city.short_name='" + city + "' and district.short_name = '" + district + "' and street.street_name='" + street + "'"
            sql2 = "SELECT city.domain FROM district INNER JOIN city ON city.city_id=district.city_id where city.short_name='" + city + "' and district.short_name = '" + district + "'"
            if len(DB.selectData(sql)) == 0:
                if len(DB.selectData(sql2)) >=0:
                    print city, district, street
                    #pass
                else:
                    #print sql2
                    pass
        #print city, district, streetDic
        