#coding:utf-8
import re, requests

fw = open("/Users/NealSu/Downloads/ips2loc",'w')

def ip2loc( ip ):  
    return re.search(re.compile("\"ul1.{18}(.*?)</li>"), requests.get('http://www.ip138.com/ips138.asp?ip='+ip).content).group(1)

f = open("/Users/NealSu/Downloads/ips",'r').readlines()

for ip in f:
    fw.write(ip[:-1] + '\t' + ip2loc(ip[:-1]) + '\n')
