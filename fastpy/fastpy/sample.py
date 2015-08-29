#-*- coding:utf-8 -*-
import os
import imp
import sys
import time
#from Cheetah.Template import Template
import json
import md5
#import redis
import logging
import traceback
import urllib
#from common import base

reload(sys)
sys.setdefaultencoding('utf8')

#rlog = base.FeimatLog("logs/sample.log")

class sample():
    def __init__(self):
        # init here
        #self.up_t = Template(file="templates/upload.html")
        pass

    def test_alive(self, request, response_head):
        recv_data = {}
        recv_data["a"] = request.getdic.get("a", "")
        recv_data["b"] = request.form.get("b", "")
        if "upload_file" not in request.filedic:
            return "别攻击我"
        fileitem = request.filedic["upload_file"]
        if fileitem.filename == "":
            return "请选择文件后再上传"
        fd = open("./static/%s" % fileitem.filename, "w")
        fd.write(fileitem.file.read())
        fd.close()
        return json.dumps(recv_data)