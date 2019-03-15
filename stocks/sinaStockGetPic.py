# coding:gbk
import time,sys
from commfunction import today,sleep
import requests

#{{{ download the day picture
def downloadFenshi(stockNum):
    imageUrl = 'http://image.sinajs.cn/newchart/v5/usstock/wap/min_daily/226/'+ stockNum + '.gif'
    print imageUrl
    return requests.get(imageUrl,'fenshi/'+stockNum+today()+'.gif')
#}}}

if __name__ == '__main__':
    downloadFenshi('bidu')
    downloadFenshi('qihu')
    downloadFenshi('sfun')
    downloadFenshi('58')
    downloadFenshi('fb')
    downloadFenshi('TWTR')