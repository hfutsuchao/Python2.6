#from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import threading,requests
from time import sleep,ctime,time

print 'starting at:',ctime()

urls = [
    'http://www.python.org',
    'http://www.python.org',
    'http://www.python.org'
    ]

pool = ThreadPool(4)
results = pool.map(requests.get, urls)
print results
#pool.close()
#pool.join()

print 'all done at:',ctime()
#exit()
