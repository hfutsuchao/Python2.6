from html import Html
import json

url = 'http://api.map.baidu.com/?qt=bd&c=131&wd=%E5%85%AC%E4%BA%A4%E8%BD%A6%E7%AB%99&ar=(12951331.56%2C4850348.73%3B12952531.6%2C4851548.59)&rn=10&l=18&key=&ie=utf-8&oue=1&res=api&callback=BMap.DataMgr.RawDispatcher._cbk49467'

htmlHandle = Html()
a = json.loads(htmlHandle.get(url,'').split('cbk49467(')[1][:-1])
#print json.dumps(a, indent=1)
print a['content'][0]['addr']