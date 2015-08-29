#coding:utf-8
import requests

urls = open('urls.txt','r').readlines()



for url in urls[1:]:
    html = requests.get(url[:-1])
    status_code = html.status_code
    if status_code == 404:
        print url,status_code
    else:
        #print url[:-1],status_code
        pass
