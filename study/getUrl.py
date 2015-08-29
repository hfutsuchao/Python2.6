import urllib2
proxyConfig = 'http://%s:%s@%s' % ('sc', '123654', '192.168.60.242:808')
print proxyConfig
opener = urllib2.build_opener( urllib2.ProxyHandler({'http':proxyConfig}))
urllib2.install_opener(opener)
inforMation = urllib2.urlopen("http://www.baidu.com")
print inforMation.read()