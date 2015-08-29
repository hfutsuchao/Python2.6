#coding:utf-8
import sys

our = open('our.txt','r').readlines()
their = open('their.txt','r').readlines()

dic = {}

for line in our[1:]:
    city, c1 = line.split('\t')
    if city not in dic:
        dic[city] = []
        dic[city].append(c1[:-1])
    else:
        dic[city].append(c1[:-1])

dicTheir = {}

for line in their[1:]:
    city, c1 = line.split('\t')
    if city not in dicTheir:
        dicTheir[city] = []
        dicTheir[city].append(c1[:-1])
    else:
        dicTheir[city].append(c1[:-1])

DR = {}

for city in dicTheir:
    print city
    if city not in DR:
        DR[city] = []
    for company in dicTheir[city]:
        tmp = 0
        try:
            for comp in dic[city]:
                if company.find(comp) != -1 or comp.find(company) != -1:
                    tmp = 1
                    #print city,company[:-1],comp[:-1]
                    break
            if tmp == 0:
                DR[city].append(company)
        except:
            print city
            pass

result = open('result.txt','w')


for city in DR:
    for company in DR[city]:
        result.write(city + '\t' + company + '\n')
        