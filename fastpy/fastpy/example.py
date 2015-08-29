#-*- coding:utf-8 -*-
import os
import imp
import sys
import time
#from Cheetah.Template import Template
import json
import hashlib
import logging
import traceback
import urllib
import multiprocessing
from urllib import unquote
import thread

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            try:
                method = getattr(cls._instance, "single_init")
                method()
            except Exception,e:
                print "single_init is null"
        return cls._instance

def done(request, response_head, res):
    time.sleep(1)
    res += "second"
    request.ret(res)

class example(Singleton):

    def single_init(self):
        self.a = 1
        print "init"

    def test_alive(self, request, response_head):
        return str(self.a)
        res = "first "
        thread.start_new_thread(done, (request, response_head, res))

