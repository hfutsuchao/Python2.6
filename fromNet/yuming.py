#coding:utf-8

import requests
import time
import md5
import json

def ifRegged(domain):
    t = str(time.time()).split('.')
    t = t[0] + t[1] + t[1][:1]
    t2 = int(t) + 30
    m1 = md5.new()   
    m1.update(t)   
    hashT = m1.hexdigest().upper() 
    url = 'http://pandavip.www.net.cn/check/checkdomain?callback=jQuery111105198426728602499_'+str(t)+'&domain=' + domain + '&token=check-web-hichina-com%3Aztiroovmmgenjc6nd6x2eq32kemltlnb&_='+str(t2)+'&isg2='+hashT
    url = 'http://pandavip.www.net.cn/check/checkdomain?callback=jQuery1111020866977865807712_1438845551739&domain=' + domain + '&token=check-web-hichina-com%3Akxavs1cy1q1tgusrod2gzh1zcd478o7q&_=1439615728291'
    return json.loads(requests.get(url).text[43:-2])['module'][0]['avail']

print ifRegged('asdsdadabc.com')
