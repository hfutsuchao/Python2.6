#coding:gbk
import re
source = open('C:\\Users\\suchao\\Desktop\\bbb.txt','r').readlines()
result = open("dibiaoresult.txt",'w')
city = {}
district = {}
street = {}
for s in source:
    info = s.split(',')
    iLen = len(info)
    if iLen == 2:
        if info[0] not in city:
            city[info[0]] = info[1][:-1]
        else:
            city[info[0]] = city[info[0]] + '/' + info[1][:-1]
    elif iLen ==3:
        if info[0] not in district:
            district[info[0]] = {}
            district[info[0]][info[1]] = info[2][:-1]
        else:
            if info[1] not in district[info[0]]:
                district[info[0]][info[1]] = info[2][:-1]
                continue
            else:
                district[info[0]][info[1]] = district[info[0]][info[1]] + '/' + info[2][:-1]
    elif iLen ==4:
        if info[0] not in street:
            street[info[0]] = {}
            street[info[0]][info[1]] = {}
            street[info[0]][info[1]][info[2]] = info[3][:-1]
        else:
            if info[1] not in street[info[0]]:
                street[info[0]][info[1]] = {}
                street[info[0]][info[1]][info[2]] = info[3][:-1]
            else:
                if info[2] not in street[info[0]][info[1]]:
                    street[info[0]][info[1]][info[2]] = info[3][:-1]
                    continue
                else:
                    street[info[0]][info[1]][info[2]] = street[info[0]][info[1]][info[2]] + '/' + info[3][:-1]
for c in city:
    result.write(c+'-'+c+'-'+c+'\t'+city[c]+'\n')
for city in district:
    for dist in district[city]:
        result.write(city+'-'+dist+'-'+dist+'\t'+district[city][dist]+'\n')
for city in street:
    for dist in street[city]:
        for st in street[city][dist]:
            result.write(city+'-'+dist+'-'+st+'\t'+street[city][dist][st]+'\n')