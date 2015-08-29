#coding:utf-8

resultFile = open('F:/BaiduYunDownload/tianya/tianya.txt','w')

for i in xrange(1,51):
    print 'F:/BaiduYunDownload/tianya/tianya_'+str(i)+'.txt'
    tmpFile = open('F:/BaiduYunDownload/tianya/tianya_'+str(i)+'.txt','r')
    resultFile.write(tmpFile.read())
    resultFile.write('\n')