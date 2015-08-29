#coding:gbk
import sys,time,os,BeautifulSoup
import html

html = html.Html()

url = 'http://baike.baidu.com/search'

dic = {}
t = 0
with open('xq.txt','r') as words:
    for word in words:
        try:
            t = t + 1
            if t%100 == 0:
                print str(float(t)/45)+'%'
            word = word[:-1].split('\t')
            xq = word[1]
            word = ''.join(word)
            #print xq,word
            params = {
                        'word':word,
                        'type':'0',
                        'pn':'0',
                        'rn':'10',
                        'submit':'search'
                      }
            result = html.get(url, params)
            soup = BeautifulSoup.BeautifulSoup(result, fromEncoding="gb18030")
            for ele in soup.findAll('h2'):
                try:
                    xiaoquName = ""
                    #tmp = unicode(ele.a.strong.contents[0])
                    for e in ele.a.contents:
                        if not isinstance(e, BeautifulSoup.NavigableString):
                            boldKey = unicode(e.contents[0])
                            #print boldKey
                            xiaoquName = xiaoquName + boldKey
                        else:
                            key = unicode(e)
                            xiaoquName = xiaoquName + key
                        #print xiaoquName
                    if str(boldKey) == xq:
                        dic[boldKey] = xiaoquName
                    else:
                        pass
                except Exception,e:
                    print e
        except Exception,e:
            print e
tmp = open('tmp.txt','w')
print len(dic)
for i in dic:
    r.write(i+'\t'+dic[i]+'\n')