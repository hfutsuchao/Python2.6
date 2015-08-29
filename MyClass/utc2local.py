#coding:utf-8
import time
import datetime

def utc2local(utc_st,timedelta=0):
    if timedelta==0:
        #UTC时间转本地时间（+8:00）
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        timedelta = local_time - utc_time
    else:
        timedelta = datetime.timedelta(hours=timedelta)
    local_st = utc_st + timedelta
    return local_st

def local2utc(local_st,timedelta=0):
    time_struct = time.mktime(local_st.timetuple())
    if timedelta==0:
        #本地时间转UTC时间（-8:00）
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    else:
        timedelta = datetime.timedelta(hours=timedelta)
        utc_st = datetime.datetime.fromtimestamp(time_struct) + timedelta
    return utc_st
'''
local_time = datetime.datetime.today()
print local_time

#本地转utc
utc_tran = local2utc(local_time,-21.5)
utc_time = utc_tran.strftime("%Y-%m-%d %H:%M:%S")
print utc_time
# output：2014-09-18 10:42:16

#utc转本地
local_time = utc2local(utc_tran,21.5)
print local_time.strftime("%Y-%m-%d %H:%M:%S")
#output：2014-09-18 18:42:16
'''
