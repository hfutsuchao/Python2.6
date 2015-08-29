#coding:utf-8
from GJDB import GJDB

db = GJDB()
db.ms()
db.selectData('set names utf8')

output = open('xiaoquPinyin.txt','w')

with open('xiaoqu.txt','r') as xiaoqu:
    for xq in xiaoqu:
        name = xq[:-1]
        sql = 'select name,pinyin from xiaoqu.xiaoqu_xiaoqu where name="' + name + '" limit 1;'
        #print db.selectData(sql)
        try:
            name,pingyin = db.selectData(sql)[0]
            output.write(name + '|' + pingyin+'\n')
        except:
            pass