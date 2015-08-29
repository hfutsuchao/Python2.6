#coding: gbk
ours = open('C:\\Users\\suchao\\Desktop\\1.txt').readlines()
haves = open('C:\\Users\\suchao\\Desktop\\2.txt').readlines()

resultdiff = open('C:\\Users\\suchao\\Desktop\\diff.txt','w')

dicours = [o[:-1] for o in ours]
dichaves = [h[:-1] for h in haves]
print len(dichaves)
for our in dicours:
    if our not in dichaves:
        resultdiff.write(our+'\n')
        continue
resultdiff.close()