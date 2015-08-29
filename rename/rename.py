#coding:gbk

import os
print os.listdir('./image')

name = open('name.txt', 'r').readlines()

for line in name[1:]:
    id, xqName = line[:-1].split('\t')
    print 'rename image\\' + xqName + '.jpg ' + id + '.jpg'
    print 'rename image\\' + xqName + '.png ' + id + '.jpg'
    os.system('rename image\\' + xqName + '.jpg ' + id + '.jpg')
    os.system('rename image\\' + xqName + '.png ' + id + '.jpg')
