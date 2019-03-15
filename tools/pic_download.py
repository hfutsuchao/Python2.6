#coding:utf-8
import requests
import os
urlist = open('1000','r').readlines()

def pic_download(path,url):
	print "Downloading " + url
	a = open(path+'/'+url.split('/')[-1],'wb')
	r = requests.get(url,stream=True)
	a.write(r.content)

def mkdir(path):
    path=path.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

for line in urlist:
	path, f_id, url = line[:-1].split('\t')
	mkdir(path)
	pic_download(path,url)