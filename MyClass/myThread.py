import threading
from time import sleep,ctime
loops=(4,2)

class MyThread(threading.Thread):
    threads = []
    def __init__(self):
        pass
    def addThread(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
        
    def run(self):
        for em in self.threads:
            em.start()

def loop(nloop,nsec):
    print 'start loop',nloop,'at:',ctime()
    sleep(nsec)

def main():
    nloops=range(len(loops))
    for i in nloops:
        t=MyThread()
        t.addThread(loop,(i,loops[i]),loop.__name__)
        t.threads.append(t)
    t.run()

if __name__=='__main__':
    main()
