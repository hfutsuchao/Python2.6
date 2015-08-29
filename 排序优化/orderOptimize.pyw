#coding:utf-8

from random import randint
import os
os.system("color f0")

rate = 1.05
freeToday = 10
freeHistory = 100
premierToday = 20
premierHistory = 200
premierTodayTotal = 30
premierHistoryAVG = 30

dic = {}

i = 200000

while i >= 0:
    type = randint(1,3)
    timePostTmp = randint(0,336)
    isPersonalTmp = randint(0,1)
    clickTodayTmp = randint(0,20)
    clickFreeTotalTmp = randint(clickTodayTmp,10*clickTodayTmp)
    dic[i] = {'type':type, 'timePost':timePostTmp, 'timeFreeRefresh':timePostTmp - randint(0,timePostTmp), 'timePremierRefresh':randint(0,24), 'clickFreeToday':clickTodayTmp, 'clickFreeHistory':clickFreeTotalTmp, 'clickPremierToday':clickTodayTmp, 'clickPremierHistory':clickFreeTotalTmp, 'clickPremierTodayTotal':randint(clickTodayTmp,2*clickTodayTmp), 'clickPremierHistoryAVG':randint(0,20), 'accusationTimes':randint(0,5), 'showTimes':randint(clickFreeTotalTmp,clickFreeTotalTmp*2+10), 'hasFreePic':randint(0,1), 'hasFreeLatlng':randint(0,1), 'fieldsFree':randint(14,16), 'hasPic':randint(0,1), 'hasLatlng':randint(0,1), 'fields':randint(14,16), 'isPersonal':isPersonalTmp, 'isConfirm':randint(0,isPersonalTmp), 'isWhite':randint(0,1)} 
    #timePost, timeFreeRefresh, timePremierRefresh, clickFreeToday, clickFreeHistory, clickPremierToday, clickPremierHistory, clickPremierTodayTotal, clickPremierHistoryAVG, accusationTimes, showTimes, hasFreePic, hasFreeLatlng, fieldsFree, hasPic, hasLatlng, fields, isPersonal, isConfirm, isWhite
    i = i - 1

dicResult = {}

for i in dic:
    #print dic[i]
    timePost = max(((6+(dic[i]['timePost']/24/7)*7-dic[i]['timePost']/24)/7.0*(5-dic[i]['timePost']/24/7*2)+(5-dic[i]['timePost']/24/7*2)/7.0*(1-(dic[i]['timePost']-dic[i]['timePost']/24*24)/24.0)),0)
    timeFreeRefresh = max(((6+(dic[i]['timeFreeRefresh']/24/7)*7-dic[i]['timeFreeRefresh']/24)/7.0*(5-dic[i]['timeFreeRefresh']/24/7*2)+(5-dic[i]['timeFreeRefresh']/24/7*2)/7.0*(1-(dic[i]['timeFreeRefresh']-dic[i]['timeFreeRefresh']/24*24)/24.0)),0)
    timePremierRefresh = max((1-dic[i]['timePremierRefresh']/24.0)*5,0)
    
    if dic[i]['clickFreeToday'] < freeToday:
        clickFreeToday = (1-dic[i]['clickFreeToday']/float(freeToday))*3
    else:
        clickFreeToday = max(-1.5+(1-dic[i]['clickFreeToday']/float(freeToday))*3,-3)
    if dic[i]['clickFreeHistory']<freeHistory:
        clickFreeHistory = (1-dic[i]['clickFreeHistory']/float(freeHistory))*7
    else:
        clickFreeHistory = max(-3.5+(1-dic[i]['clickFreeHistory']/float(freeHistory))*7,-7)
        
    if dic[i]['clickPremierToday']<premierToday:
        clickPremierToday = (1-dic[i]['clickPremierToday']/float(premierToday))*1
    else:
        clickPremierToday = max(-0.5+(1-dic[i]['clickPremierToday']/float(premierToday))*1,-1)
    if dic[i]['clickPremierHistory']<premierHistory:
        clickPremierHistory = (1-dic[i]['clickPremierHistory']/float(premierHistory))*3
    else:
        clickPremierHistory = max(-1.5+(1-dic[i]['clickPremierHistory']/float(premierHistory))*3,-3)
    if dic[i]['clickPremierTodayTotal']<premierTodayTotal:
        clickPremierTodayTotal = (1-dic[i]['clickPremierTodayTotal']/float(premierTodayTotal))*3
    else:
        clickPremierTodayTotal = max(-1.5+(1-dic[i]['clickPremierTodayTotal']/float(premierTodayTotal))*3,-3)
    if dic[i]['clickPremierHistoryAVG']<premierHistoryAVG:
        clickPremierHistoryAVG = (1-dic[i]['clickPremierHistoryAVG']/float(premierHistoryAVG))*3
    else:
        clickPremierHistoryAVG = max(-1.5+(1-dic[i]['clickPremierHistoryAVG']/float(premierHistoryAVG))*3,-3)
        
    accusationTimes = max(-dic[i]['accusationTimes'],-5)
    if dic[i]['showTimes']>5 and (1-dic[i]['clickFreeHistory']/float(dic[i]['showTimes']))>0.5:
        showTimes = (dic[i]['clickFreeHistory']/float(dic[i]['showTimes'])-1)*5
    else:
        showTimes = 0
        
    if dic[i]['hasFreePic']:
        hasFreePic = 4
    else:
        hasFreePic = 0
    if dic[i]['hasFreeLatlng']:
        hasFreeLatlng = 2
    else:
        hasFreeLatlng = 0
    fieldsFree = max((3-(16-dic[i]['fieldsFree']))/3.0*4,0)
    
    if dic[i]['hasPic']:
        hasPic = 2
    else:
        hasPic = 0
    if dic[i]['hasLatlng']:
        hasLatlng = 1.5
    else:
        hasLatlng = 0
    fields = max((3-(16-dic[i]['fields']))/3.0*1.5,0)
    if dic[i]['isPersonal']:
        isPersonal = 2
    else:
        isPersonal = 0
    if dic[i]['isConfirm']:
        isConfirm = 3
    else:
        isConfirm = 0
    
    if dic[i]['isWhite']:
        isWhite = rate
    else:
        isWhite = 1
    #print timePost, timeFreeRefresh, timePremierRefresh, clickFreeToday, clickFreeHistory, clickPremierToday, clickPremierHistory, clickPremierTodayTotal, clickPremierHistoryAVG, accusationTimes, showTimes, hasFreePic, hasFreeLatlng, fieldsFree, hasPic, hasLatlng, fields, isPersonal, isConfirm, isWhite
    
    timeFree = (timePost + timeFreeRefresh)*10
    clickFree = (clickFreeToday + clickFreeHistory)*7
    clickPremier = (clickPremierToday + clickPremierHistory + clickPremierTodayTotal + clickPremierHistoryAVG)*7
    illegal = (accusationTimes + showTimes)*5
    fields13 = (hasPic + hasLatlng + fields + isPersonal + isConfirm)*3
    fields = (hasFreePic + hasFreeLatlng + fieldsFree)*3
    timePremier = (timePost + timePremierRefresh)*10
    if dic[i]['type'] == 1:
        total = timeFree + clickFree + illegal + fields13
    elif dic[i]['type'] == 2:
        total = timeFree + clickFree + illegal + fields
    elif dic[i]['type'] == 3:
        total = (timePremier + clickPremier + illegal + fields)*isWhite
    #print total
    dicResult[total] = {0:dic[i], 1:timeFree, 2:timePremier, 3:clickFree, 4:clickPremier, 5:illegal, 6:fields13, 7:fields}
    #print total,timeFree,clickFree,illegal,fields13

tmpFile = open('resutl.txt','w')
count = [0,0,0]

for i in sorted(dicResult.items(),cmp=lambda e,y:cmp(e[1][0]['type'],y[1][0]['type']) or cmp(e[0],y[0]),reverse=True):
    count[i[1][0]['type']-1] = count[i[1][0]['type']-1] + 1
    if count[i[1][0]['type']-1] <= 50:
        tmpFile.write(str(i[1][0]['type']) + '\t' + str(i[0]) + '\t' + str(i[1][0]['timePost']) + '\t' + str(i[1][0]['timeFreeRefresh']) + '\t' + str(i[1][0]['timePremierRefresh']) + '\t' + str(i[1][0]['clickFreeToday']) + '\t' + str(i[1][0]['clickFreeHistory']) + '\t' + str(i[1][0]['clickPremierToday']) + '\t' + str(i[1][0]['clickPremierHistory']) + '\t' + str(i[1][0]['clickPremierTodayTotal']) + '\t' + str(i[1][0]['clickPremierHistoryAVG']) + '\t' + str(i[1][0]['accusationTimes']) + '\t' + str(i[1][0]['showTimes']) + '\t' + str(i[1][0]['hasFreePic']) + '\t' + str(i[1][0]['hasFreeLatlng']) + '\t' + str(i[1][0]['fieldsFree']) + '\t' + str(i[1][0]['hasPic']) + '\t' + str(i[1][0]['hasLatlng']) + '\t' + str(i[1][0]['fields']) + '\t' + str(i[1][0]['isPersonal']) + '\t' + str(i[1][0]['isConfirm']) + '\t' + str(i[1][0]['isWhite']) + '\t' + str(i[1][1]) + '\t' + str(i[1][2]) + '\t' + str(i[1][3]) + '\t' + str(i[1][4]) + '\t' + str(i[1][5]) + '\t' + str(i[1][6]) + '\t' + str(i[1][7]) + '\n')
    