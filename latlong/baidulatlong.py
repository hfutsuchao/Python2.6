#encoding:gbk
import json
import html
import os
#data = {'ak':'BC5f181e1e57cfe86deac47428b9793b','address':'百度大厦','output':'json','callback':'showLocation'}

os.system('color f0')

url = 'http://api.map.baidu.com/geocoder/v2/'
htmlHandle = html.Html()
xiaoqu = open('jwd.txt').readlines()
for xq in xiaoqu:
    cityName,dist = xq.split('-')
    dist = dist[:-1]
    data = {'ak':'BC5f181e1e57cfe86deac47428b9793b','address':cityName+dist,'output':'json'}
    result = json.loads(htmlHandle.get(url,data))
    try:
        print cityName+'-'+dist+'-b' + str(result['result']['location']['lng'])+","+str(result['result']['location']['lat'])
    except Exception,e:
        print e,result

os.system('pause')
