#-*- coding:utf-8 -*-
import os
import sys
import httplib
import json
import mimetypes
import mimetools
import threading
import Queue
import traceback
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf8')


host = "game.coolplay123.com"
port = 8992



domain = "%s:%s" % (host, port)
def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg

def get_content_type(filepath):
    return mimetypes.guess_type(filepath)[0] or 'application/octet-stream'

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filepath) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = "------8f8289fwur280hfoit9073u89428h"
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (filename, content) in files.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (filename, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(content)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

filename = sys.argv[1]

if not os.path.exists(filename):
    print filename, "not exist"
    exit(0)

def send_sub(filename, data, seek_start):
    fields = {}
    fields["filename"] = filename
    fields["seek_start"] = str(seek_start)
    files = {}
    files["data"] = data
    content_type, body = encode_multipart_formdata(fields, files)

    headers = {}
    headers["Content-Type"] = content_type

    httpClient = httplib.HTTPConnection(domain)
    httpClient.request('POST', '/sendfile.upload', body, headers)
    response = httpClient.getresponse()
    status = response.status
    if status != 200:
        return ""
    else:
        res = response.read()
        return res

def send_clear(filename):
    fields = {}
    fields["filename"] = filename
    files = {}
    content_type, body = encode_multipart_formdata(fields, files)

    headers = {}
    headers["Content-Type"] = content_type

    httpClient = httplib.HTTPConnection(domain)
    httpClient.request('POST', '/sendfile.upload', body, headers)
    response = httpClient.getresponse()
    status = response.status
    if status != 200:
        return ""
    else:
        res = response.read()
        return res

finish_count = 0

class SendThread(threading.Thread):
    def __init__(self, sub_data_list, list_size, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.sub_data_list = sub_data_list
        self.list_size = list_size
        self.setDaemon(True)

    def run(self):
        while True:
            try:
                sub_filename, seek_start, sub_read_len = self.sub_data_list.get(block=False)
                while True:
                    try:
                        global filename
                        fp = open(filename)
                        fp.seek(seek_start)
                        sub_data = fp.read(sub_read_len)
                        fp.close()
                        res = send_sub(filename, sub_data, seek_start)
                        if res == "suc":
                            global finish_count
                            finish_count += 1
                            per = "%.2f" % (float(finish_count)*100/self.list_size)
                            print "send %s suc, 完成 %s%s" % (sub_filename, per, "%")
                            break
                    except Exception, e:
                        pass
            except Queue.Empty:
                break
            except :
                print "thread error:" + getTraceStackMsg()

sub_data_list = Queue.Queue()
fp = open(filename)
file_index = 1

filesize = os.path.getsize(filename)
seek_start = 0
sub_size = 1024*30
while True:
    if filesize > sub_size:
        sub_read_len = sub_size
    else:
        sub_read_len = filesize
    filesize -= sub_read_len
    sub_filename = "%s_._%s" % (filename, file_index)
    sub_data_list.put((sub_filename, seek_start, sub_read_len))
    file_index += 1
    seek_start += sub_read_len
    if filesize <= 0:
        break

thread_num = 60
sub_size = sub_data_list.qsize()
if sub_size < thread_num:
    thread_num = sub_size

res = send_clear(filename)
if res == "suc":
    print "start send file"
else:
    print res
    exit(0)

threads = []
for i in xrange(0, thread_num):
    thread = SendThread(sub_data_list, sub_size)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print "finish"
