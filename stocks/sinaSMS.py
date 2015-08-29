#coding:utf-8
from SOAPpy import WSDL
import json
#wsdlFile = 'http://smsinter.sina.com.cn/ws/smswebservice0101.wsdl'
wsdlFile = 'http://202.108.35.168/ws/smswebservice0101.wsdl'
server = WSDL.Proxy(wsdlFile)

server.soapproxy.config.dumpSOAPOut = 1
server.soapproxy.config.dumpSOAPIn = 1
server.soapproxy.config.debug = 9


#data = ['sina','18600219332','240611310','18600219332','Hello,world!','new']
data = {'Carrier':'Union', 'Id':'hfutsuchao@gmail.com' , 'Password':'240611310' , 'ToMobile':'18600219330' , 'Message':'Hello,world!' , 'MsgType':'Text' }
#data = json.dumps(data)
'''for i in server.methods['sendXml'].inparams:
    print i.name,i.type'''
#print sever.__getattr__('sendXml')
#data = "sina,18600219332,240611310','18600219332','Hello,world!','new'"
#print server.sendXml("sina","18600219332","240611310","18600219332","Hello","new")

print server.sendXml(str(json.dumps(data)))