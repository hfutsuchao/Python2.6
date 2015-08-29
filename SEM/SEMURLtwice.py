#coding: utf-8
from urllib import urlencode
from GJDB import GJDB

dicType = {'租房':'fang1','个人':'a1','合租':'fang3','写字楼':'fang8','商铺':'fang6'}

othersKws = open('othersKws.txt','r').readlines()

result = open('SEMURLresult.txt','w')

def getCityDistrictStreet(sql=''):
    management = GJDB()
    management.management()
    management.selectDB('management')
    management.executeDB('SET NAMES UTF8;')
    if sql == '':
        sql = 'SELECT city.short_name city_name, city.domain, district.short_name district_name,district.url, street.street_name, street.url FROM street INNER JOIN district INNER JOIN city ON district.district_id=street.district_id AND city.city_id=district.city_id;'
    return management.selectData(sql)

def getCityXiaoqu(sql=''):
    ms = GJDB()
    ms.ms()
    ms.selectDB('xiaoqu')
    ms.executeDB('SET NAMES UTF8;')
    if sql == '':
        sql = 'SELECT distinct city, name FROM xiaoqu_xiaoqu;'
    return ms.selectData(sql)

xiaoqus = getCityXiaoqu()

sql = 'SELECT city.short_name city_name, city.domain, district.short_name district_name,district.url FROM district INNER JOIN city ON city.city_id=district.city_id;'
quyu = getCityDistrictStreet(sql)
diyu = getCityDistrictStreet()

dicCity = {}

for line in diyu:
    city, domain, district, districtUrl, street, streetUrl = line
    if city in dicCity:
        if district not in dicCity[city]['districts']:
            dicCity[city]['districts'][district] = districtUrl
        if street not in dicCity[city]['streets']:
            dicCity[city]['streets'][street] = streetUrl
    else:
        dicCity[city] = {}
        dicCity[city]['domain'] = domain
        dicCity[city]['districts'] = {}
        dicCity[city]['streets'] = {}
        dicCity[city]['xiaoqus'] = {}
        dicCity[city]['districts'][district] = districtUrl
        dicCity[city]['streets'][street] = streetUrl

for line in quyu:
    city, domain, district, districtUrl = line
    if city in dicCity:
        if district not in dicCity[city]['districts']:
            dicCity[city]['districts'][district] = districtUrl
    else:
        dicCity[city] = {}
        dicCity[city]['domain'] = domain
        dicCity[city]['districts'] = {}
        dicCity[city]['streets'] = {}
        dicCity[city]['xiaoqus'] = {}
        dicCity[city]['districts'][district] = districtUrl

for line in xiaoqus:
    city, xiaoqu = line
    for cityName in dicCity:
        if city ==  dicCity[cityName]['domain']:
            if xiaoqu not in dicCity[cityName]['xiaoqus']:
                dicCity[cityName]['xiaoqus'][xiaoqu] = ''

for line in othersKws:
    cat1, cat2, kw = line.split('\t')
    #column 1 check
    url = ''
    haveCity = False
    districtStreet = ''
    category = 'fang1'
    agent = ''
    
    for city in dicCity:
        if cat1.find(city) != -1:
            haveCity = True
            #column 2 check
            domain = dicCity[city]['domain']
            for type in dicType:
                if cat1.find(type) != -1:
                    category = dicType[type]
                if cat2.find(type) != -1:
                    category = dicType[type]
                    if type == '个人':
                        category = 'fang1'
                        agent = 'a1'
                    break
            
            for city in dicCity:
                if kw.find(city) != -1:
                    domain = dicCity[city]['domain']
                    break
            
            if kw.find('合租') != -1 and category == 'fang1':
                category = 'fang3'
            if kw.find('个人') != -1:
                agent = 'a1'
                
            
            #{{{xiaoqu
            for xiaoqu in dicCity[city]['xiaoqus']:
                if kw.find(xiaoqu) != -1:
                    districtStreet = xiaoqu
                    if not agent:
                        url = 'xiaoqu' + 'http://' + domain + '.ganji.com/' + category + '/_' + urlencode({'':xiaoqu}).split('=')[1] + '/'
                    else:
                        url = 'xiaoqu' + 'http://' + domain + '.ganji.com/' + category + '/' + agent + '/_' + urlencode({'':xiaoqu}).split('=')[1] + '/'
                    break
            #xiaoqu end}}}
            
            if url == '':
                for street in dicCity[city]['streets']:
                    if kw.find(street) != -1:
                        districtStreet = street
                        if not agent:
                            url = 'street' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['streets'][street] + '/'
                        else:
                            url = 'street' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['streets'][street] + '/' + agent +'/'
                        break
            if url == '':
                for district in dicCity[city]['districts']:
                    if kw.find(district) != -1:
                        districtStreet = district
                        if not agent:
                            url = 'district' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['districts'][district] + '/'
                        else:
                            url = 'district' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['districts'][district] + '/' + agent +'/'
                        break
            if url == '':
                if not agent:
                    url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/'
                else:
                    url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/' + agent + '/'
            result.write(line[:-1] + '\t' + url + '\n')
            break
    if cat1.find('通用') != -1 and url == '' and not haveCity:
        domain = 'www'
        for city in dicCity:
            haveCity = False
            if cat1.find(type) != -1:
                category = dicType[type]
            if cat2.find(city) != -1:
                haveCity = True
                domain = dicCity[city]['domain']
                
                for city in dicCity:
                    if kw.find(city) != -1:
                        domain = dicCity[city]['domain']
                        break
                
                if kw.find('合租') != -1 and category == 'fang1':
                    category = 'fang3'
                if kw.find('个人') != -1:
                    agent = 'a1'
                
                for city in dicCity:
                    if kw.find(city) != -1:
                        domain = dicCity[city]['domain']
                        break
                
                #{{{xiaoqu
                for xiaoqu in dicCity[city]['xiaoqus']:
                    if kw.find(xiaoqu) != -1:
                        districtStreet = xiaoqu
                        if not agent:
                            url = 'xiaoqu' + 'http://' + domain + '.ganji.com/' + category + '/_' + urlencode({'':xiaoqu}).split('=')[1] + '/'
                        else:
                            url = 'xiaoqu' + 'http://' + domain + '.ganji.com/' + category + '/' + agent + '/_' + urlencode({'':xiaoqu}).split('=')[1] + '/'
                        break
                #xiaoqu end}}}
                
                if url is '':
                    for street in dicCity[city]['streets']:
                        if kw.find(street) != -1:
                            districtStreet = street
                            if not agent:
                                url = 'street' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['streets'][street] + '/'
                            else:
                                url = 'street' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['streets'][street] + '/' + agent + '/'
                            break
                
                if url is '':    
                    for district in dicCity[city]['districts']:
                        if kw.find(district) != -1:
                            districtStreet = district
                            if not agent:
                                url = 'district' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['districts'][district] + '/'
                            else:
                                url = 'district' + 'http://' + domain + '.ganji.com/' + category + '/' + dicCity[city]['districts'][district] + '/' + agent + '/'
                            break
                if url == '':
                    if not agent:
                        url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/'
                    else:
                        url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/' + agent +'/'
                result.write(line[:-1] + '\t' + url + '\n')
                break
        #通用内不含城市
        if not haveCity :
            
            for city in dicCity:
                if kw.find(city) != -1:
                    domain = dicCity[city]['domain']
                    break
            
            if kw.find('合租') != -1 and category == 'fang1':
                category = 'fang3'
            if kw.find('个人') != -1:
                agent = 'a1'
                
            if url == '':
                if not agent:
                    url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/'
                else:
                    url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/' + agent + '/'
            result.write(line[:-1] + '\t' + url + '\n')
    elif url == '' and not haveCity:
        domain = 'www'
        
        for city in dicCity:
            if kw.find(city) != -1:
                domain = dicCity[city]['domain']
                break
        
        if kw.find('合租') != -1 and category == 'fang1':
            category = 'fang3'
        if kw.find('个人') != -1:
            agent = 'a1'
        if not agent:
            url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/'
        else:
            url = 'city' + 'http://' + domain + '.ganji.com/' + category + '/' + agent + '/'
        result.write(line[:-1] + '\t' + url + '\n')
        