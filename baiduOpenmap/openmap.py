#coding:utf-8
import html

handle = html.Html()

selecturl = 'http://api.map.baidu.com/geodata/v2/poi/list'

delurl = 'http://api.map.baidu.com/geodata/v2/poi/delete'
addurl = 'http://api.map.baidu.com/geodata/v2/poi/upload'

data = {'ak':'BC5f181e1e57cfe86deac47428b9793b','geotable_id':38979}
adddata = {'ak':'BC5f181e1e57cfe86deac47428b9793b','geotable_id':38979,'poi_list':'data.csv'}
print handle.get(selecturl,data)
'''
for i in range(1,8):
    handle.post(delurl,data,'')
'''
#print handle.post(addurl,adddata,'')
'''
createurl = 'http://api.map.baidu.com/geodata/v2/poi/create'
with open('data_one.csv','r') as datas:
    for data in datas:
        title,address,longitude,latitude,coord_type,expired,xiaoqu_id,xiaoqu_url,sell_num,rent_num,avg_price,sell_houses,rent_houses,picture = data.split('\t')
        #print  title
        data = {'ak':'BC5f181e1e57cfe86deac47428b9793b','geotable_id':38979,'title':title,'address':address,'longitude':longitude,'latitude':latitude,'coord_type':coord_type,'expired':expired,'xiaoqu_id':xiaoqu_id,'xiaoqu_url':xiaoqu_url,'sell_num':sell_num,'rent_num':rent_num,'avg_price':avg_price,'sell_houses':sell_houses,'rent_houses':rent_houses,'picture':picture}
        #print data
        print handle.post(createurl,data,'')
'''
'''
import MultipartPostHandler, urllib2, cookielib
addurl = 'http://api.map.baidu.com/geodata/v2/poi/upload'
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
MultipartPostHandler.MultipartPostHandler)
params = { 'ak':'BC5f181e1e57cfe86deac47428b9793b','geotable_id':'38979',
"poi_list" : open("data.csv", "r") }
a = opener.open(addurl, params)
print help(a)
print a.read()
'''