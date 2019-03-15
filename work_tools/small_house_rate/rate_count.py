#coding:utf-8
datas = open('./data.txt','r').readlines()

cid = {}
for line in datas:
    city,source,telephone,new_status,ctime = line.split('\t')
    if city not in cid:
        cid[city] = {}
        cid[city][telephone] = {}
        cid[city][telephone][new_status] = [[ctime,source]]
    elif telephone not in cid[city]:
        cid[city][telephone] = {}
        cid[city][telephone][new_status] = [[ctime,source]]
    elif new_status not in cid[city][telephone]:
        cid[city][telephone][new_status] = [[ctime,source]]
    else:
        cid[city][telephone][new_status].append([ctime,source])

counts = {}
sourcesCount = {}

for city in cid:
    sourcesCount[city] = {}
    sourcesCount[city]['1'] = {}
    sourcesCount[city]['3'] = {}
    sourcesCount[city]['1']['1'] = 0
    sourcesCount[city]['1']['3'] = 0
    sourcesCount[city]['3']['1'] = 0
    sourcesCount[city]['3']['3'] = 0
    counts[city] = {}
    counts[city]['done'] = {}
    counts[city]['undo'] = {}
    counts[city]['done']['order'] = 0
    counts[city]['done']['customer'] = 0
    counts[city]['undo']['order'] = 0
    counts[city]['undo']['customer'] = 0

for city in cid:
    for telephone in cid[city]:
        tmp = 0
        try:
            for new_status in cid[city][telephone]:
                for elm in cid[city][telephone][new_status]:
                    if int(elm[0]) > int(cid[city][telephone]['3'][0][0]):
                        tmp = tmp + 1
                        if new_status != '3':
                            sourcesCount[city][cid[city][telephone]['3'][0][1]][elm[1]] = sourcesCount[city][cid[city][telephone]['3'][0][1]][elm[1]] + 1

            if tmp and len(cid[city][telephone]['3']) < 2:
                counts[city]['undo']['order'] = counts[city]['undo']['order'] + tmp - len(cid[city][telephone]['3']) + 1
                counts[city]['undo']['customer'] = counts[city]['undo']['customer'] + 1
            elif tmp:
                counts[city]['done']['order'] = counts[city]['done']['order'] + len(cid[city][telephone]['3']) - 1
                counts[city]['done']['customer'] = counts[city]['done']['customer'] + 1
        except Exception, e:
            print telephone,e

for city in counts:
    for t in counts[city]:
        print city,t,counts[city][t]['order'],counts[city][t]['customer']

for city in sourcesCount:
    print city,sourcesCount[city]['1']['1'],sourcesCount[city]['1']['3'],sourcesCount[city]['3']['1'],sourcesCount[city]['3']['3']
