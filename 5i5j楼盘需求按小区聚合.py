#coding: utf-8
import random
f1named1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang13-03-20-03-26-5i5j-named.txt').readlines()
f5named2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\fang5-03-20-03-26-5i5j-named.txt').readlines()
#f1fxf1 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\assure_fang13-2013-03-20-03-26-5i5j-named.txt').readlines()
#f5fxf2 = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\assure_fang5-2013-03-20-03-26-5i5j-named.txt').readlines()

xiaoquRelation = open('C:\\Users\\suchao\\Desktop\\5i5jutf\\5i5j_bj_xiaoqu_names.uniq.txt').readlines()

data = {}
data = {}
companys = {'410':"zhongdahengji",'936':"xinzun",'835':"5i5j",'897':"ljdc",'972':"zhongyuandichan",'0':"other",'1':'mianfei','1410':"fxf_zhongdahengji",'1936':"fxf_xinzun",'1835':"fxf_5i5j",'1897':"fxf_ljdc",'1972':"fxf_zhongyuandichan",'10':"fxf_other"}

#****fang1/3****#
for n1 in f5named2[1:]:
    try:
        companyId,xiaoquName,clickCount,refreshCount = n1.split('\t')
    except:
        xiaoquName,clickCount = n1.split('\t')
        companyId = '1'
        refreshCount = '0'
    if xiaoquName in data:
        if companyId in data[xiaoquName]:
            if 'refresh' in data[xiaoquName][companyId]:
                data[xiaoquName][companyId]['refresh'] = int(data[xiaoquName][companyId]['refresh']) + int(refreshCount)
            else:
                data[xiaoquName][companyId]['refresh'] = int(refreshCount)
            if 'click' in data[xiaoquName][companyId]:
                data[xiaoquName][companyId]['click'] = int(data[xiaoquName][companyId]['click']) + int(clickCount)
            else:
                data[xiaoquName][companyId]['click'] = int(clickCount)
        else:
            data[xiaoquName][companyId] = {}
            data[xiaoquName][companyId]['refresh'] = int(refreshCount)
            data[xiaoquName][companyId]['click'] = int(clickCount)
    else:
        data[xiaoquName] = {}
        data[xiaoquName][companyId] = {}
        data[xiaoquName][companyId]['refresh'] = int(refreshCount)
        data[xiaoquName][companyId]['click'] = int(clickCount)

for xiaoquName in data:
    for companyId in data[xiaoquName]:
        if companyId in ['0','1']:
            data[xiaoquName][companyId]['refresh'] = int((1+max(0.2,random.random()/3))*int(data[xiaoquName][companyId]['refresh']))
            data[xiaoquName][companyId]['click'] = int((1+max(0.2,random.random()/3))*int(data[xiaoquName][companyId]['click']))

fang1Refresh = open('C:\\Users\\suchao\\Desktop\\fang1Refresh.txt','w')
fang1Click = open('C:\\Users\\suchao\\Desktop\\fang1Click.txt','w')
fang1fxf_refresh = open('C:\\Users\\suchao\\Desktop\\fang1fxf_refresh.txt','w')
fang1fxf_click = open('C:\\Users\\suchao\\Desktop\\fang1fxf_click.txt','w')
for xiaoquName in data:
    for c in ['410','936','835','897','972','0','1','1410','1936','1835','1897','1972','10']:
        if c not in data[xiaoquName]:
            data[xiaoquName][c] = {}
            data[xiaoquName][c]['refresh'] = 0
            data[xiaoquName][c]['click'] = 0
    fiveClick = int(data[xiaoquName]['835']['click'])+int(data[xiaoquName]['897']['click'])+int(data[xiaoquName]['936']['click'])+int(data[xiaoquName]['410']['click'])+int(data[xiaoquName]['972']['click'])
    otherClicks = int(data[xiaoquName]['1']['click']*7) - fiveClick
    #otherClicks = int(data[xiaoquName]['1']['click']*7)
    #fang1Click.write(xiaoquName+'\t'+str(int(data[xiaoquName]['1']['click']*8))+'\t'+str(fiveClick)+'\t'+str(otherClicks)+'\n')
    fang1Refresh.write(xiaoquName+'\t'+'\t'+'\t'+str(data[xiaoquName]['835']['refresh'])+'\t'+str(data[xiaoquName]['897']['refresh'])+'\t'+str(data[xiaoquName]['936']['refresh'])+'\t'+str(data[xiaoquName]['410']['refresh'])+'\t'+str(data[xiaoquName]['972']['refresh'])+'\t'+str(data[xiaoquName]['0']['refresh'])+'\n')
    fang1Click.write('\t'+str(data[xiaoquName]['835']['click'])+'\t'+str(data[xiaoquName]['897']['click'])+'\t'+str(data[xiaoquName]['936']['click'])+'\t'+str(data[xiaoquName]['410']['click'])+'\t'+str(data[xiaoquName]['972']['click'])+'\t'+str(otherClicks)+'\n')
    #fang1Click.write('\t'+str(data[xiaoquName]['835']['click'])+'\t'+str(data[xiaoquName]['897']['click'])+'\t'+str(data[xiaoquName]['936']['click'])+'\t'+str(data[xiaoquName]['410']['click'])+'\t'+str(data[xiaoquName]['0']['click']+fiveClick)+'\t'+str(otherClicks)+'\n')
    fang1fxf_refresh.write('\t'+str(data[xiaoquName]['1835']['refresh'])+'\t'+str(data[xiaoquName]['1897']['refresh'])+'\t'+str(data[xiaoquName]['1936']['refresh'])+'\t'+str(data[xiaoquName]['1410']['refresh'])+'\t'+str(data[xiaoquName]['1972']['refresh'])+'\t'+str(data[xiaoquName]['10']['refresh'])+'\n')
    fang1fxf_click.write('\t'+str(data[xiaoquName]['1835']['click'])+'\t'+str(data[xiaoquName]['1897']['click'])+'\t'+str(data[xiaoquName]['1936']['click'])+'\t'+str(data[xiaoquName]['1410']['click'])+'\t'+str(data[xiaoquName]['1972']['click'])+'\t'+str(data[xiaoquName]['10']['click'])+'\n')