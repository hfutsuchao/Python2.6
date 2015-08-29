# coding:gbk
import time,sys
from commonFunction import dateToday,sleep
import html

htmlHandle = html.Html()

#{{{ download the day picture
def downloadFenshi(stockNum):
    global htmlHandle
    imageUrl = 'http://image.sinajs.cn/newchart/v5/usstock/wap/min_daily/226/'+ stockNum + '.gif'
    return htmlHandle.download(imageUrl,'fenshi/'+stockNum+dateToday()+'.gif')
#}}}

if __name__ == '__main__':
    downloadFenshi('bidu')
    downloadFenshi('qihu')
    downloadFenshi('sfun')
    downloadFenshi('58')
    downloadFenshi('fb')
    downloadFenshi('TWTR')