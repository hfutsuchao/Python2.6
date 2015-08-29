import qd
dic = qd.getDetail()
dateList = qd.getDates(qd.day_dt_stat_date,qd.day_dt_end_date)
for source in dic:
    for detail in dic[source]:
        for dt in dateList:
            if dt not in dic[source][detail]:
                dic[source][detail][dt] = {'uv':0,'pv':0}

print dic

datas = {}
for source in dic:
    for detail in dic[source]:
        if detail not in ['avg','total']:
            datas[detail] = ''
            for dt in dateList:
                datas[detail] = str(datas[detail]) + ',' + str(dic[source][detail][dt]['uv'])
            datas[detail] = datas[detail].split(',')[1]
print datas