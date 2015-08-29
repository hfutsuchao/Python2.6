import threading,requests
from time import sleep,ctime,time

class MyThread(threading.Thread):
       def __init__(self,func,args,name=''):
              threading.Thread.__init__(self)
              self.name=name
              self.func=func
              self.args=args
       def run(self):
              apply(self.func,self.args)

def loop(nloop,nsec):
       #print 'start loop',nloop,'at:',ctime()
       start = time()
       resp = requests.get('http://45.78.13.14/').status_code
       if resp!=200:
          print resp
       print nloop,str(time()-start)

def main():

       print 'starting at:',ctime()
       threads=[]
       nloops = 250
       for i in xrange(nloops):
              t=MyThread(loop,(i,i),loop.__name__)
              threads.append(t)

       for i in xrange(nloops):
              threads[i].start()

       '''for i in nloops:

              threads[i].join()'''

       print 'all done at:',ctime()

if __name__=='__main__':
       main()


'''
import threading
mylock = threading.RLock()
num=0
 
class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name
        
    def run(self):
        global num
        while True:
            mylock.acquire()
            print '/nThread(%s) locked, Number: %d'%(self.t_name, num)
            if num>=4:
                mylock.release()
                print '/nThread(%s) released, Number: %d'%(self.t_name, num)
                break
            num+=1
            print '/nThread(%s) released, Number: %d'%(self.t_name, num)
            mylock.release()
            
def test():
    thread1 = myThread('A')
    thread2 = myThread('B')
    thread1.start()
    thread2.start()
 
if __name__== '__main__':
    test()
'''