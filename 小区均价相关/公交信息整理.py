#coding:gbk
import re
#source = open('C:\\Users\\suchao\\Desktop\\fangrentnew.txt','r').readlines()
#result = open("gjresult2.txt",'w')
source = open('C:\\Users\\suchao\\Desktop\\1.txt','r').readlines()
result = open("gjresult.txt",'w')
for s in source:
    info = s.split('|')
    iLen = len(info)
    x = 0
    for i in info:
        x = x + 1
        iBefore = i.split("^")
        dt = iBefore[7]
        gj = i.split("^")[9]
        del iBefore[9]
        #print "^".join(iBefore)
        print dt
        lx = re.findall("([0-9]+)",gj)
        #print i,lx,len(lx)
        if len(lx) >= 2:
            tmplx = str(lx[0])+'路'+','+str(lx[1])+'路'
        elif len(lx) == 1:
            tmplx = str(lx[0])+'路'
        else:
            if dt == '-':
                tmplx = '暂无'
            else:
                tmplx = ''
        
        if x != iLen:
            if (x != 1) and (len(lx) == 0) and (dt == '-'):
                pass
            else:
                result.write("^".join(iBefore)+'^'+tmplx+'|')
        else:
            if (len(lx) == 0) and (dt == '-'):
                result.write('\n')
            else:
                result.write("^".join(iBefore)+'^'+tmplx+'\n')
        '''    
        if x != iLen:
            result.write("^".join(iBefore)+'^'+tmplx+'|')
        else:
            result.write("^".join(iBefore)+'^'+tmplx+'\n')
        '''