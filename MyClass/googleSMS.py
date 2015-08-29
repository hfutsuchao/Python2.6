#-*- coding:utf-8 -*-
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
mail = 'hfutsuchao@gmail.com' #google账号
password = 'yyLY891229'  #密码
minutes = 5 #在个事件开始前5分钟开始提醒
def sendSMS(title,content = ""):
    cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
    cal_client.ClientLogin(mail,password, cal_client.source)
    event = gdata.calendar.data.CalendarEventEntry()
    event.title = atom.data.Title(text=title) #事件的标题
    event.content = atom.data.Content(text=content)#事件的内容
    event.where.append(gdata.data.Where(value='')) #事件的地点
    start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + 360)) #开始时间是当前时间延后6分钟
    end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + 3600)) #结束时间是当前时间延后1个小时
    event.when.append(gdata.data.When(start=start_time,end=end_time))
    new_event = cal_client.InsertEvent(event)
    for a_when in new_event.when:
        if len(a_when.reminder) > 0:
            a_when.reminder[0].minutes = minutes
        else:
            a_when.reminder.append(gdata.data.Reminder(minutes=str(minutes)))
    cal_client.Update(new_event)
if __name__ == '__main__':
    if len(sys.argv) != 3 :
        print '\nUsage: googleSMS.py title content'
        sys.exit()
    title = sys.argv[1]
    try:
        content = sys.argv[2]
    except:
        content = ""
    sendSMS(title)