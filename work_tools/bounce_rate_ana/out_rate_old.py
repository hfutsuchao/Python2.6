#coding:utf-8
import json
pvs = open('/Users/NealSu/GoogleDisk/MyWorkInHaozu/Data/pvuv','r').readlines()
import re

pv_counts = {}
out_rate = {}
in_rate = {}
rate_counts = {}

regex = ['\?.*','\d', '.*?//', '\.haozu.com/\w{2}', '\.haozu.com']

#TOP 页面
for line in pvs:
    date,uid,category,subcategory,url = line[:-1].split('\t')
    if 'sem' not in url:
        continue
    for i in regex:
        url = re.sub(i, '', url)
    if date not in pv_counts:
        pv_counts[date] = {}
        out_rate[date] = {}
        in_rate[date] = {}
    if url not in pv_counts[date]:
        pv_counts[date][url] = [uid]
        out_rate[date][url] = 0
        in_rate[date][url] = 0
    else:
        pv_counts[date][url].append(uid)
        out_rate[date][url] = 0
        in_rate[date][url] = 0
'''
for date in pv_counts:
    for url in pv_counts[date]:
        print date+'\t'+url+'\t'+str(len(set(pv_counts[date][url])))
'''

#核心跳出率
for line in pvs:
    date,uid,category,subcategory,url = line[:-1].split('\t')
    if 'sem' not in url:
        continue
    for i in regex:
        url = re.sub(i, '', url)
    if date not in rate_counts:
        rate_counts[date] = {}
    if uid not in rate_counts[date]:
        rate_counts[date][uid] = [url]
    else:
        rate_counts[date][uid].append(url)

for date in rate_counts:
    for uid in rate_counts[date]:
        if len(rate_counts[date][uid]) == 1:
            out_rate[date][rate_counts[date][uid][0]] = out_rate[date][rate_counts[date][uid][0]] + 1
        else:
            in_rate[date][rate_counts[date][uid][0]] = in_rate[date][rate_counts[date][uid][0]] + 1

total_land = {}
for date in out_rate:
    for url in out_rate[date]:
        try:
            total_land[url]['total'] = total_land[url]['total'] + out_rate[date][url]+in_rate[date][url]
            total_land[url]['out'] = total_land[url]['out'] + out_rate[date][url]
        except:
            total_land[url] = {}
            total_land[url]['total'] = out_rate[date][url]+in_rate[date][url]
            total_land[url]['out'] = out_rate[date][url]

for url in total_land:
    try:
        print url+'\t'+ str(total_land[url]['total']) + '\t' + str(total_land[url]['out'])
    except:
        pass
