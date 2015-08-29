file = open('fang_search_kw-2012-10-05.log','r').readlines()
dic = {}
countPv = 0
for f in file[1:]:
    try:
        cat,uv,v,pv,keyword = f.split('\t')
        countPv = countPv + int(pv)
    except:
        print f
    if cat in dic:
        dic[cat].append(f)
    else:
        dic[cat] = []
        dic[cat].append(f)
print countPv
for key in dic.keys():
    fname = open('1005\\'+key+'.txt','w+')
    for i in sorted(dic[key], key=lambda i:int(i.split('\t')[1]), reverse= True):fname.write(i)
    fname.close()