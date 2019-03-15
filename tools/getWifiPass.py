#coding:utf-8
import requests
pwd = requests.get('http://netlogin.guazi-corp.com/net/setpass.php').text
print pwd.split(': ')[1].replace('</b>','')