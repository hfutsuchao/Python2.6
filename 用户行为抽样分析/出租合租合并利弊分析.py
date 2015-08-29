#coding:gbk
import re

source = open("C:\Users\suchao\Desktop\chouqu.txt").readlines()

users = {}

sum = 0

for s in source:
    user,time,category,url,refer = s.split("\t")
    if user in users:
        users[user][time] = url+'\t'+refer
    else:
        users[user] = {}
        users[user][time] = url+'\t'+refer

for user in users:
    #print user
    istrue = 0
    for time in users[user]:
        url,refer = users[user][time].split("\t")
        if url.find('fang3') != -1 and url.find('.htm') != -1:
            istrue = 1
        if istrue == 1 and url.find('m1')!= -1:
            istrue = 2
    if istrue == 2:
        sum = sum + 1
        for time in users[user]:
            print user,users[user][time][:-1]
        continue
print sum