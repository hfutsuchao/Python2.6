#coding:utf-8
a = [1,2,3,4,5,6]
r = {}
for i in a:
    for j in a:
        for k in a:
            if str(i+j+k) not in r:
                r[str(i+j+k)] = 1
            else:
                r[str(i+j+k)] = r[str(i+j+k)] + 1

for k in r:
    print str(k) + '\t' + str(r[k])