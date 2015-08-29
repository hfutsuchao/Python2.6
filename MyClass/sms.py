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
from random import randint
from datetime import datetime,timedelta
class SMS:
    minutes = randint(1,20)*10
    mail = 'hfutsuchao@gmail.com'
    password = ''
    title = ''
    content = ''
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    reminder = '15'
    last = '1'
    
    def addCalendar(self, title, date='', last='30', content="", reminder='30'):
        try:
            self.year, date = date.split('y')
        except:
            pass
        try:
            self.month, date = date.split('mon')
        except Exception, e:
            pass
        try:
            self.day, date = date.split('d')
        except:
            pass
        try:
            self.hour, date = date.split('h')
        except Exception, e:
            print e
            pass
        try:
            self.minute, date = date.split('min')
        except:
            pass
        self.last = last
        if title:
            self.title = title
        if content:
            self.content = content
        self.reminder = reminder
        
        self.start_time = str(self.year) + '-' + str(self.month) + '-' + str(self.day) + 'T' + str(self.hour) + ':' + str(self.minute) + ':00.000Z'
        print self.start_time
        start_time_tmp = datetime.strptime(self.start_time,'%Y-%m-%dT%H:%M:%S.000Z')
        start_time_timestamp = time.mktime(start_time_tmp.timetuple())
        self.start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(start_time_timestamp))
        self.end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(start_time_timestamp + int(self.last)*60))
        
        print self.start_time,self.end_time
        
        '''self.start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + (1+1)*60)) 
        self.end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + (1+31)*60))
        
        print self.start_time,self.end_time'''
        
        cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
        cal_client.ClientLogin(self.mail, self.password, cal_client.source)
        event = gdata.calendar.data.CalendarEventEntry()
        event.title = atom.data.Title(text=self.title) 
        event.content = atom.data.Content(text=self.content)
        event.where.append(gdata.data.Where(value='')) 
        event.when.append(gdata.data.When(start=self.start_time,end=self.end_time))
        new_event = cal_client.InsertEvent(event)
        for a_when in new_event.when:
            if len(a_when.reminder) > 0:
                a_when.reminder[0].minutes = self.reminder
            else:
                a_when.reminder.append(gdata.data.Reminder(minutes=str(self.reminder)))
        cal_client.Update(new_event)
    #{{{usage:sendSMS(message)
    def sendSMS(self, title, minutes = "5", content = ""):
        print title,minutes,content
        if title:
            self.title = title
        if content:
            self.content = content
        if minutes:
            self.minutes = int(minutes)
        self.start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + (self.minutes+1)*60)) 
        self.end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime(time.time() + (self.minutes+31)*60))
        cal_client = gdata.calendar.client.CalendarClient(source='Google-Calendar_Python_Sample-1.0')
        cal_client.ClientLogin(self.mail, self.password, cal_client.source)
        event = gdata.calendar.data.CalendarEventEntry()
        event.title = atom.data.Title(text=self.title) #Title
        event.content = atom.data.Content(text=self.content)    #Content
        event.where.append(gdata.data.Where(value='')) #place
        event.when.append(gdata.data.When(start=self.start_time,end=self.end_time))
        new_event = cal_client.InsertEvent(event)
        for a_when in new_event.when:
            if len(a_when.reminder) > 0:
                a_when.reminder[0].minutes = self.minutes
            else:
                a_when.reminder.append(gdata.data.Reminder(minutes=str(self.minutes)))
        cal_client.Update(new_event)
    #}}}
if __name__ == '__main__':
    sms = SMS()
    #sms.sendSMS("test",5)
    sms.addCalendar('title', '9mon15d13h50min', '30', 'content', '1')
