#coding:utf-8

tmpF = open('C:\\Users\\suchao\\Desktop\\tmpData.txt','w')
for i in xrange(1,31):
    with open('C:\\Users\\suchao\\Desktop\\data.txt','r') as tmp:
        for line in tmp:
            tmpF.write('2013-11-' + str(i) + ' ' + line)