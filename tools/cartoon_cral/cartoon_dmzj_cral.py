#coding:utf-8
from BeautifulSoup import BeautifulSoup
import requests,os
from commfunction import sleep

urls = open('urls.txt').readlines()

def pic_download(url,path,filename,headers):
	pic_type = '.jpg'
	ended = False
	if not filename:
		filename = url.split('/')[-1]
	a = open(path+'/'+filename,'wb')
	r = requests.get(url,headers=headers,stream=True)
	if not r.ok:
		r = requests.get(url.replace("jpg","png"),headers=headers,stream=True)
		pic_type = '.png'
		if not r.ok:
			ended = True
	a.write(r.content)
	return [pic_type,ended]

def mkdir(path):
    path=path.strip()
    path=path.rstrip("/")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

if __name__ == '__main__':
	path = '赌博默示录'
	mkdir(path)
	for vn in range(8,9):
		vn =str(vn)
		while len(vn)<2:
			vn = '0' + vn
		headers = {"%3aauthority":"images.dmzj.com","%3amethod":"GET","%3apath":"/d/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95/VOL"+vn+"/0001.jpg","%3ascheme":"https","accept":"image/webp,image/apng,image/*,*/*;q=0.8","accept-encoding":"gzip, deflate, br","accept-language":"zh-CN,zh;q=0.9,en;q=0.8","cache-control":"no-cache","cookie":"UM_distinctid=1657141fb8ac1c-013ccfe4f560fc-3464790b-fa000-1657141fb8b45b; show_tip_1=0","pragma":"no-cache","referer":"https://manhua.dmzj.com/duboqishilu/7088.shtml","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
		img_url = "https://images.dmzj.com/d/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95/VOL"+vn+"/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95%20%E7%AC%AC8%E5%8D%B7_0001.jpg"
		pic_type = pic_download(img_url,path,'VOL01_0001.jpg',headers=headers)[0]
		for i in range(2,1000):
			name = str(i)
			while len(name)<4:
				name = '0' + name
			headers = {"%3aauthority":"images.dmzj.com","%3amethod":"GET","%3apath":"/d/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95/VOL"+vn+"/"+name+".jpg","%3ascheme":"https","accept":"image/webp,image/apng,image/*,*/*;q=0.8","accept-encoding":"gzip, deflate, br","accept-language":"zh-CN,zh;q=0.9,en;q=0.8","cache-control":"no-cache","cookie":"UM_distinctid=1657141fb8ac1c-013ccfe4f560fc-3464790b-fa000-1657141fb8b45b; show_tip_1=0","pragma":"no-cache","referer":"https://manhua.dmzj.com/duboqishilu/7088.shtml","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
			img_url = "https://images.dmzj.com/d/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95/VOL"+vn+"/%E8%B5%8C%E5%8D%9A%E5%90%AF%E7%A4%BA%E5%BD%95%20%E7%AC%AC8%E5%8D%B7_" + name + pic_type
			print img_url
			ended = pic_download(img_url,path,'VOL'+vn+'_'+name+pic_type,headers=headers)[1]
			if ended:
				break
			sleep(0.5)