#coding:utf-8

#file line : 2014-01-17    /fang/fang1/phone_hidden@ig_tg=0@agent=0@atype=show

dic = {}

userTypeDic = {'11':'付费端口贴','01':'免费经纪人贴','00':'免费个人贴'}

with open('semphone') as phoneHidden:
    for line in phoneHidden:
        dt, city, gjalog = line.split('\t')
        cat, is_tg, agent, atype = gjalog.split('@')
        cat = cat.split('/')[2]
        is_tg = is_tg.split('=')[1]
        agent = agent.split('=')[1]
        city = city.split('.')[0]
        atype = atype[:-1]
        userType = userTypeDic[is_tg+agent]
        cat = dt + '\t' + cat
        if cat in dic:
            if userType in dic[cat]:
                dic[cat][userType][atype] = dic[cat][userType][atype] + 1
            else:
                dic[cat][userType] = {}
                dic[cat][userType]['atype=show'] = 0
                dic[cat][userType]['atype=click'] = 0
        else:
            dic[cat] = {}
print len(dic)
for cat in dic:
    for userType in dic[cat]:
        print cat, userType, dic[cat][userType]['atype=click'], dic[cat][userType]['atype=show'], float(dic[cat][userType]['atype=click'])/(dic[cat][userType]['atype=show']+0.1)