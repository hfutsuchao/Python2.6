#coding utf-8

sourceFile = open('re.txt','r')
filter = open('del.xls','r')

dicFilter = {}

for line in filter:
    elements = line.split('\t')
    type = elements[1]
    accountID = elements[3]
    title = elements[8]
    #print title
    try:
        dicFilter[title] = []
    except:
        print line

print len(dicFilter)
dicResutlt = {}

for line in sourceFile:
    elements = line.split('\t')
    type = elements[1]
    accountID = elements[3]
    title = elements[8]
    try:
        if  int(type) not in (7,8,9) and title in dicFilter:
            if title not in dicResutlt:
                dicResutlt[title] = [accountID]
            else:
                dicResutlt[title].append(accountID)
    except:
        print line
r = open('a.txt','w')
for k in dicResutlt:
    for i in dicResutlt[k]:
        r.write(k + '\t' + str(i) + '\n')