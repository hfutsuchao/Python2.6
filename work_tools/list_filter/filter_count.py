#coding:utf-8
pvs = open('/Users/NealSu/Downloads/list_pv','r').readlines()
#result = open('/Users/NealSu/GoogleDisk/MyTools/Python2.6/tools/result.txt','w')

pv_counts = {}
pv_counts['total'] = {}
pv_counts['total']['total'] = []
for line in pvs:
    dt, uuid, pt = line.split('\t')
    pt_elms = pt[:-1].replace('/item/list@','').split('@')
    for elm in pt_elms:
        cat = elm.split('=')[0]
        pv_counts['total']['total'].append(uuid)
        if cat not in pv_counts:
            pv_counts[cat] = {}
            pv_counts[cat]['total'] = [uuid]
        if elm not in pv_counts[cat]:
            pv_counts[cat][elm] = [uuid]
        else:
            pv_counts[cat][elm].append(uuid)
        pv_counts[cat]['total'].append(uuid)
cat = 'productCategorys'
for elm in pv_counts[cat]:
    break
    print elm,len(set(pv_counts[cat][elm])),len(pv_counts[cat][elm])

for cat in pv_counts:
    print cat,len(set(pv_counts[cat]['total']))

#result.close()
