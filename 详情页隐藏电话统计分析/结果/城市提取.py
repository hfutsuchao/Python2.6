dateNow = "2012-11-11"
#resultShow = open(dateNow+'resultShow.txt','r')
#resultClick = open(dateNow+'resultClick.txt','r')
resultShowGeren = open(dateNow+'resultShowGeren.txt','r')
resultClickGeren = open(dateNow+'resultClickGeren.txt','r')
#resultShowmfzj = open(dateNow+'resultShowmfzj.txt','r')
#resultClickmfzj = open(dateNow+'resultClickmfzj.txt','r')

#resultShow1 = open(dateNow+'resultShow1.txt','w')
#resultClick1 = open(dateNow+'resultClick1.txt','w')
resultShowGeren1 = open(dateNow+'resultShowGeren1.txt','w')
resultClickGeren1 = open(dateNow+'resultClickGeren1.txt','w')
#resultShowmfzj1 = open(dateNow+'resultShowmfzj1.txt','w')
#resultClickmfzj1 = open(dateNow+'resultClickmfzj1.txt','w')
'''
for d in resultShow:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultShow1.write(d)
for d in resultClick:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultClick1.write(d)'''
for d in resultShowGeren:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultShowGeren1.write(d)
for d in resultClickGeren:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultClickGeren1.write(d)
for d in resultShowmfzj:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultShowmfzj1.write(d)
for d in resultClickmfzj:
    city = d.split('\t')[1]
    if city == "bj_fang1":
        resultClickmfzj1.write(d)
