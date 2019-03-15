#coding:utf-8
from BeautifulSoup import BeautifulSoup
import requests 

urls = open('urls.txt')

for u in urls:
	contents = requests.get(u[:-1])
	print u[:-1],BeautifulSoup(contents.content).title