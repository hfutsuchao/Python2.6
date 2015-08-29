file = open('house_complain.txt').readlines()
r = open('house_complain_reslut.txt','w')
dic = {}
arr = []
for i in file[1:]:
    arr = i.split('\t')
    if arr[0] in dic:
        dic[arr[0]]['mon'] = dic[arr[0]]['mon'] + arr[1][5:6]
        dic[arr[0]]['count'] =  dic[arr[0]]['count'] + int(arr[2])
        dic[arr[0]]['count7'] = dic[arr[0]]['count7'] + int(arr[3])
        dic[arr[0]]['count8'] = dic[arr[0]]['count8'] + int(arr[4])
        dic[arr[0]]['house'] = dic[arr[0]]['house'] + int(arr[5])
        dic[arr[0]]['ip'] = dic[arr[0]]['ip'] + int(arr[6])
    else:
        dic[arr[0]]= {}
        dic[arr[0]]['count'] =  int(arr[2])
        dic[arr[0]]['mon'] = arr[1][5:6]
        dic[arr[0]]['count7'] = int(arr[3])
        dic[arr[0]]['count8'] = int(arr[4])
        dic[arr[0]]['house'] = int(arr[5])
        dic[arr[0]]['ip'] = int(arr[6])
for i in sorted(dic.iteritems(), key=lambda d:d[1]['count'],reverse = True):
    r.write(i[0]+'\t'+i[1]['mon']+'\t'+str(i[1]['count'])+'\t'+str(i[1]['count7'])+'\t'+str(i[1]['count8'])+'\t'+str(i[1]['house'])+'\t'+str(i[1]['ip'])+'\n')
r.close()
