#-*- coding:utf-8 -*-
import os
import imp
import sys
import time
from Cheetah.Template import Template
import json
import logging
import traceback
import random
import zipfile
import shutil
from xml.etree import ElementTree
import multiprocessing
import mimetypes
import mimetools

import config
from common import base
from common import net

FastpyAutoUpdate = True
reload(sys)
sys.setdefaultencoding('utf8')

loger = base.FeimatLog("logs/sendfile.log")
savedir = "./static/sendfile_dir/"
try:
    os.makedirs(savedir)
except Exception, e:
    pass

class sendfile():
    def __init__(self):
        try:
            pass
        except Exception, e:
            print str(e)+base.getTraceStackMsg()

    def upload(self, request, response_head):
        try:
            seek_start = request.form.get("seek_start", None)
            filename = request.form.get("filename", None)
            data = request.filedic.get("data", None)
            if seek_start == None and filename != None:
                filepath = os.path.join(savedir, filename)
                cmd = "rm -rf %s; touch %s" % (filepath, filepath)
                os.popen(cmd).read()
                return "suc"
            elif data != None and filename != None and seek_start != None:
                filepath = os.path.join(savedir, filename)
                seek_start = int(seek_start)
                f = open(filepath, "r+")
                f.seek(seek_start)
                f.write(data.file.read())
                f.close()
                return "suc"
            else:
                return "empty"
        except Exception, e:
            loger.log(str(e)+base.getTraceStackMsg())
            return str(e)+base.getTraceStackMsg()



