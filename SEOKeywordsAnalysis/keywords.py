#coding:utf-8
import html,time
import BeautifulSoup
from urllib import quote

htmlHandle = html.Html()

loginUrl = 'http://www.aizhan.com/login.php?refer=http://ci.aizhan.com/'

params = {
            'email':'hfutsuchao@gmail.com',
            'password':'814155356',
            'refer':'http%3A%2F%2Fci.aizhan.com%2F'
          }

htmlHandle.get(loginUrl,'')
htmlHandle.post(loginUrl,params,'')

fileSEO = open('SEOKeywordsUV.txt','w')

with open('keywords.txt','r') as keywords:
    for kw in keywords:
        try:
            print "http://ci.aizhan.com/" + kw[:-1] + '/'
            content = htmlHandle.get("http://ci.aizhan.com/" + quote(kw[:-1]) + '/','')
            content = BeautifulSoup.BeautifulSoup(content)


            searchesSum = 0
            includesSum = 0
            searchesSum1 = 0
            includesSum1 = 0
            searchesSum2 = 0
            includesSum2 = 0
            searchesSum3 = 0
            includesSum3 = 0
            score1 = 0
            score2 = 0
            score3 = 0
            rowSum = 0
            
            for tr in content.table.findAll('tr')[1:]:
                tds = tr.findAll('td')
                rowNum = tds[0].contents[0]
                keywordTag = tds[1].a.contents
                #print 'tds',tds
                keyword = ''
                if len(keywordTag) >= 2:
                    #print keywordTag
                    for c in keywordTag:
                        if isinstance(c, BeautifulSoup.Tag):
                            keyword = keyword + c.contents[0]
                        else:
                            keyword = keyword + c
                else:
                    try:
                        keyword = keywordTag[0].contents[0]
                        #print keyword
                    except Exception,e:
                        #print keywordTag
                        print e
                searches = tds[2].contents[0]
                if searches[:1] == '<':
                    searches = '25'
                includes = tds[3].contents[0]
                loc1 = tds[4].a.contents[0]
                loc2 = tds[5].a.contents[0]
                if loc1[-9:] == 'ganji.com':
                    score = '1'
                    score1 = score1 + 1
                    includesSum1 = includesSum1 + int(includes)
                    searchesSum1 = searchesSum1 + int(searches)
                elif loc2[-9:] == 'ganji.com':
                    score = '2'
                    score2 = score2 + 1
                    includesSum2 = includesSum2 + int(includes)
                    searchesSum2 = searchesSum2 + int(searches)
                else:
                    score = '>3'
                    score3 = score3 + 1
                    includesSum3 = includesSum3 + int(includes)
                    searchesSum3 = searchesSum3 + int(searches)
                rowSum = rowSum + 1
                searchesSum = searchesSum + int(searches)
                includesSum = includesSum + int(includes)
                
                fileSEO.write(kw[:-1] + '\t' + rowNum + '\t' + keyword + '\t' + searches + '\t' + includes + '\t' + loc1 + '\t' + loc2 + '\t' + score + '\n')
            fileSEO.write(kw[:-1] + '_sumAll\t' + str(rowSum) + '\t' + kw[:-1] + '\t' + str(searchesSum) + '\t' + str(includesSum) + '\n')
            fileSEO.write(kw[:-1] + '_sum1\t' + str(score1) + '\t' + kw[:-1] + '\t' + str(searchesSum1) + '\t' + str(includesSum1) + '\n')
            fileSEO.write(kw[:-1] + '_sum2\t' + str(score2) + '\t' + kw[:-1] + '\t' + str(searchesSum2) + '\t' + str(includesSum2) + '\n')
            fileSEO.write(kw[:-1] + '_sum3\t' + str(score3) + '\t' + kw[:-1] + '\t' + str(searchesSum3) + '\t' + str(includesSum3) + '\n')
            time.sleep(2)
        except Exception,e:
            print e
