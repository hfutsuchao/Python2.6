#coding:utf-8

import requests
import time
import md5
import json
import warnings
warnings.filterwarnings("ignore")

def ifRegged(domain):
    t = str(time.time()).split('.')
    t = t[0] + t[1] + t[1][:1]
    t2 = int(t) + 30
    m1 = md5.new()   
    m1.update(t)   
    hashT = m1.hexdigest().upper() 
    url = "https://checkapi.aliyun.com/check/checkdomain?callback=jQuery111103447876243447301_1467883490844&domain="+domain+"&token=check-web-hichina-com%3Aq4ndvr4dw4e0zz6tlgntg2we2cf2doou&_=1467883490899"
    #print url
    return json.loads(requests.get(url).text.split("(")[1].split(")")[0])['module'][0]['avail']

#print ifRegged('kaonve.com')
