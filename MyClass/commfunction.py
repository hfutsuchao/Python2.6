#coding:utf-8
import os
import time, datetime
import sys
import requests, re

def sleep(t=0):
    time.sleep(float(t))

def comp_sleep(t=0):
    time.sleep(float(t))
    os.system('shutdown -h')

def date_validate(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        try:
            time.strptime(str, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

def today(format='%Y-%m-%d'):
    today = time.strftime(format,time.localtime(time.time()))
    return today

def replace_sign(str, mode = 0):
    hard = ['\t',' ','~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', ',', '.', '/', ':', '"', ';', '\\', '\'', '[', ']', '{', '}', '|', '<', '>', '?', '，', '。', '、', '《', '》', '？', '，', '；', '‘', '：', '“', '”', '【', '】', '、', '￥', '（', '）', '·', '！', '\n', '\r']
    easy = ['\t','~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '/', '\\', '\'', '[', ']', '{', '}', '<', '>', '、', '《', '》', '，', '‘', '：', '“', '”', '【', '】', '、', '￥', '（', '）', '·', '\n', '\r']
    modeType = (easy, hard)
    for sign in modeType[mode]:
        str = str.replace(sign,'')
    return str

def ip2loc( ip ):  
    return re.search(re.compile("\"ul1.{18}(.*?)</li>"), requests.get('http://www.ip138.com/ips138.asp?ip='+ip).content).group(1)

def date_add(date,delta=1,inFormat='%Y-%m-%d',outFormat='%Y-%m-%d'):
    date = datetime.datetime.strptime(date, inFormat) + datetime.timedelta(days=delta)
    return date.strftime(outFormat)

def date_today_delta(T,format='%b %d, %Y'):
    T = datetime.datetime.strptime(T,format)
    today = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    return (T-today).days+1

if __name__ == '__main__':
    try:
        print ip2loc(sys.argv[1])
    except:
        comp_sleep(5)
