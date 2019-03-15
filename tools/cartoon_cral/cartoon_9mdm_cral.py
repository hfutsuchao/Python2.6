#coding:utf-8
from BeautifulSoup import BeautifulSoup
import requests,os
from commfunction import sleep

urls = open('urls.txt').readlines()

def pic_download(url,path,filename):
	if not filename:
		filename = url.split('/')[-1]
	a = open(path+'/'+filename,'wb')
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

def get_img(url,path):
	global title
	contents = requests.get(url)
	bs = BeautifulSoup(contents.content)
	page = bs.find('div',{'class':'pages'}).b.contents[0]
	last_page = bs.find('div',{'class':'pages'}).findAll('a')[-1].contents[0]
	img_url = bs.find('div',{'class':'mh_list'}).p.a.img.get('src')
	pic_download(img_url,path,title+'_'+str(page+'.jpg'))
	if not last_page.isdigit():
		url = url.split('.html')[0].split('_')[0] + '_' + str(int(page)+1) + '.html'
		sleep(0.5)
		get_img(url,path)

if __name__ == '__main__':
	for line in urls:
		url, title = line[:-1].split('\t')
		print url, title
		path = '黑瞳'
		mkdir(path)
		get_img(url,path)