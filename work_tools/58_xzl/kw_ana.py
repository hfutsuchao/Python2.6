#coding:utf-8
from BeautifulSoup import BeautifulSoup
import requests 
from commfunction import sleep
urls = open('urls.txt')
#exit()
import re
import httplib
#httplib._is_legal_header_name = re.compile(r'\A[^:\s][^:\r\n]*\Z').match
httplib._is_legal_header_name = re.compile(r'\A[^\s][^\r\n]*\Z').match

def get_house_num(url,headers):
	districts = BeautifulSoup(requests.get(url,headers=headers,verify=False).content).find(id='qySelectFirst').findAll(para='local')
	nums = {}
	for d in districts:
		d_name = d.contents[0]
		nums[d_name] = {}
		nums[d_name]['total'] = 1
		d_url = u.split('.com')[0] + '.com' + d.get('href')
		try:
			bs = BeautifulSoup(requests.get(d_url,headers=headers,verify=False).content)
			streets = bs.find(id='qySelectSecond').findAll('a')
		except Exception,e:
			print e
			streets = ''
		try:
			pages = bs.findAll('div',{'class':'pager'})[0].findAll('a')[-2].contents[0].contents[0]
			nums[d_name]['total'] = int(pages)
		except Exception,e:
			print e
			pages = 1
		
		sum_street = 0
		for s in streets:
			d_url = u.split('.com')[0] + '.com' + s.get('href')
			s = s.contents[0]
			try:
				sbs = BeautifulSoup(requests.get(d_url,headers=headers,verify=False).content)
				s_pages = sbs.findAll('div',{'class':'pager'})[0].findAll('a')[-2].contents[0].contents[0]
			except Exception,e:
				print e
				s_pages = 1
			sleep(1)
			nums[d_name][s] = int(s_pages)
			sum_street = sum_street + int(s_pages)

		if pages == '70' and streets:
			nums[d_name]['total'] = sum_street
		sleep(1)

	return nums

if __name__ == '__main__':
	for u in urls:
		host = (u.split('.com')[0] + '.com').replace('http://','')
		headers = {
		":authority": host,
		":method": "GET",
		":path": "/zhaozu/pve_1092_0/",
		":scheme": "https",
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"accept-encoding": "gzip, deflate, br",
		"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
		"cache-control": "no-cache",
		"cookie": "f=n; userid360_xml=922B9F0E550AF1BA00F919A88A57BBD0; time_create=1541913109176; commontopbar_new_city_info=304%7C%E7%A6%8F%E5%B7%9E%7Cfz; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; cookieuid=cad056bf-7f0e-499c-8947-0c90963a036d; gr_user_id=934d32a4-afd9-4898-b880-07d83dca668c; _ga=GA1.2.2025838593.1452417562; id58=c5/nn1nu80a1kZqRBx1FAg==; xxzl_deviceid=F3CxmWXVf%2Fg5YsiIFgQ6kSTdy%2Flop2TMmDtTp5yRVodhG0II7AhOjBylarIJXogf; 58tj_uuid=6778a066-058c-44be-bb09-8201dfbe8a30; als=0; xxzl_smartid=e2524f2fb5f331331ed1e26ee8ad3e21; UM_distinctid=1633d608b39474-0792a6b1031de-33667f05-fa000-1633d608b3a3c2; wmda_uuid=478a81068109904a6db80e4778ac4fef; __utmz=253535702.1536557268.28.22.utmcsr=bj.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/xiaoqu/; wmda_visited_projects=%3B2385390625025%3B1409632296065%3B1732030748417%3B1731916484865%3B6333604277682; __utma=253535702.2025838593.1452417562.1536557268.1538116994.29; Hm_lvt_3f405f7f26b8855bc0fd96b1ae92db7e=1536737138,1539075468; Hm_lpvt_3f405f7f26b8855bc0fd96b1ae92db7e=1539075468; city=cq; 58home=cq; ppStore_fingerprint=0323BCFB797E70E06ADC6C87331DD1589AC62AB4A40278E0%EF%BC%BF1539314772440; new_uv=190; utm_source=; spm=; init_refer=; f=n; new_session=0; JSESSIONID=F10B1E4498EF5BB7C3C65F8B7E814D05",
		"pragma": "no-cache",
		"upgrade-insecure-requests": "1",
		"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		nums = get_house_num(u[:-1],headers)
		print host
		for district in nums:
			for street in nums[district]:
				print district,street,nums[district][street]