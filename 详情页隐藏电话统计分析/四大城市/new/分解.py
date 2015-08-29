#coding:gbk
CityClickDuankou = open('resultCityClickDuankou.txt','r')
CityClickMianfei = open('resultCityClickMianfei.txt','r')
CityXianshiDuankou = open('resultCityXianshiDuankou.txt','r')
CityXianshiMianfei = open('resultCityXianshiMianfei.txt','r')

dic = {}

for dClick in CityClickDuankou:
    city = dClick.split('\t')[1]
    category = dClick.split('\t')[2]
    shenfen = dClick.split('\t')[3]
    houseId = dClick.split('\t')[4]
    filename = city+'_'+category+'_'+shenfen
    if filename in dic:
        dic[filename][houseId] = dClick
    else:
        dic[filename] = {}
        dic[filename][houseId] = dClick

for dClick in CityClickMianfei:
    try:
        city = dClick.split('\t')[1]
    except:
        print dClick
    category = dClick.split('\t')[2]
    shenfen = dClick.split('\t')[3]
    houseId = dClick.split('\t')[4]
    filename = city+'_'+category+'_'+shenfen
    if filename in dic:
        dic[filename][houseId] = dClick
    else:
        dic[filename] = {}
        dic[filename][houseId] = dClick

for filename in dic:
    file = open(filename+'Click.txt','w')
    for houseId in dic[filename]:
        file.write(dic[filename][houseId])
    file.close()

for dXianshi in CityXianshiDuankou:
    city = dXianshi.split('\t')[1]
    category = dXianshi.split('\t')[2]
    shenfen = dXianshi.split('\t')[3]
    houseId = dXianshi.split('\t')[4]
    filename = city+'_'+category+'_'+shenfen
    if filename in dic:
        dic[filename][houseId] = dXianshi
    else:
        dic[filename] = {}
        dic[filename][houseId] = dXianshi

for dXianshi in CityXianshiMianfei:
    city = dXianshi.split('\t')[1]
    category = dXianshi.split('\t')[2]
    shenfen = dXianshi.split('\t')[3]
    houseId = dXianshi.split('\t')[4]
    filename = city+'_'+category+'_'+shenfen
    if filename in dic:
        dic[filename][houseId] = dXianshi
    else:
        dic[filename] = {}
        dic[filename][houseId] = dXianshi

for filename in dic:
    file = open(filename+'Xianshi.txt','w')
    for houseId in dic[filename]:
        file.write(dic[filename][houseId])
    file.close()