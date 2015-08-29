#coding:utf-8
import html,os

headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Cookie":"gj_inner_acc=1-3218; __utma=32156897.922795486.1373282254.1373349227.1373356621.4; __utmz=32156897.1373282254.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ganji_uuid=7317481816123928727508-287307261; _gl_tracker=%7B%22sid%22%3A50026929814%7D; __utmc=32156897; GDNETSSOC=userm=VyTZ2dihqf8gf7TmQ8GB7CmmvYA4/HaXRZacxgYV8yx0wz9zEoGogNK4dHdnukt5; GANJISESSID=b058a88bc6b334435358979b235d67d4",
            "Host":"stat.corp.ganji.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"
            }

#url = "http://stat.corp.ganji.com/CustomBaseReportManagement/CustomBaseReportManager?reportId=20035" 
url = "http://stat.corp.ganji.com/" 
post = {
        'page':'1',
        'para_filter':'"day_dt_stat_date":"2013/7/8","day_dt_end_date":"2013/7/8","city_key":"0","category_key":"7","source":"total"',
        'size':'20'
        }

statHandle = html.Html()

print statHandle.post(url,"",headers)

#print statHandle.get('http://stat.corp.ganji.com//SEOTrace/KeywordManagement','')

#os.system('start ' + url)