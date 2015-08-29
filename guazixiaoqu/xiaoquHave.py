#coding:gbk
import html
import json

urlopener = html.Html()
with open('bjxiaoqu.txt','r') as xiaoqus:
    for xiaoqu in xiaoqus:
        try:
            xiaoquId,name = xiaoqu.split('\t')
            url = 'http://guazi.ganji.com/openapi/getPostByGeo/?token=1309227240229108184&lid=' + xiaoquId + '&type=1,2,3,4'
            result = json.loads(urlopener.get(url,''))
            if result['data']['total'] > 0:
                print xiaoquId,name[:-1],result['data']['total'],result['data']['list'].keys()
            else:
                #print xiaoquId,name[:-1],result['data']['total']
                pass
        except Exception, e:
            print e
