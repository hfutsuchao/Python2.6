#coding:gbk
import random
xiaoquIn58 = open('xiaoqujj.txt','r').readlines()
cds = open('cds.txt','r').readlines()

dic={}

for c in cds:
    cityId,cityName,districtId,districtName,streetId,streetName = c.split('\t')
    #cityName,districtName,streetName = c.split('\t')
    cityName = cityName[:4]
    streetName = streetName[:-1]
    if cityName in dic:
        if districtName in dic[cityName]:
            if streetName in dic[cityName][districtName]:
                pass
            else:
                dic[cityName][districtName][streetName]={}
        else:
            dic[cityName][districtName]={}
            dic[cityName][districtName][streetName]={}
    else:
        dic[cityName]={}
        dic[cityName][districtName] = {}
        dic[cityName][districtName][streetName]={}

'''for c in dic:
    for d in dic[c]:
        print len(dic[c][d])'''
error = 0
ok = 1

result = open("jieguo.txt",'w')

for xiaoqu in xiaoquIn58:
    try:
        city,district,street,xiaoqu_name,huxing_shi,avgPrice,rentCount,year,buildingType,subway = xiaoqu.split('\t')
    except:
        print xiaoqu,xiaoqu.split('\t'),len(xiaoqu.split('\t'))
        error = error1 + 1
    subway = subway[:-1]
    try:
        if xiaoqu_name in dic[city][district][street]:
            ok = ok + 1
            dic[city][district][street][xiaoqu_name][huxing_shi] = avgPrice + ',' + year + ',' + buildingType + ',' + subway
            #result.write(dic[city][district][street][xiaoqu_name][huxing_shi])
        else:
            ok = ok + 1
            dic[city][district][street][xiaoqu_name] = {}
            dic[city][district][street][xiaoqu_name][huxing_shi] = avgPrice + ',' + year + ',' + buildingType + ',' + subway
            #print dic[city][district][street][xiaoqu_name][huxing_shi]
    except:
        error = error + 1

for city in dic:
    #print district,len(dic[city])
    for district in dic[city]:
        #print street,len(dic[city][district])
        for street in dic[city][district]:
            x = 1
            for xiaoqu_name in dic[city][district][street]:
            #print street
                '''if len(dic[city][district][street])>=1:
                    result.write(city+","+district+","+street+":")'''
                '''for i in sorted(dic[city][district][street].iteritems(), key = lambda asd:int(str(asd).split(',')[9]) ,reverse = True):
                    i = "".join(i)
                    print street,str(i).split(',')[0],int(str(i).split(',')[8]),int(str(i).split(',')[9])
                    result.write(city+","+district+","+street+","+str(i)+"\n")'''
                for huxing_shi in dic[city][district][street][xiaoqu_name].keys():
                    if (street != "其他") and ("all" not in dic[city][district][street][xiaoqu_name]):
                        if huxing_shi == "1":
                            tmp = dic[city][district][street][xiaoqu_name][huxing_shi]
                            avg1 = tmp.split(",")[0]
                            avg2 = str(float(avg1)*1.2)
                            avg3 = str(float(avg1)*1.44)
                            if avg1.find(".") != -1:
                                avg1 = avg1[:avg1.find(".")]
                            if avg2.find(".") != -1:
                                avg2 = avg2[:avg2.find(".")]
                            if avg3.find(".") != -1:
                                avg3 = avg3[:avg3.find(".")]
                            avgShare = str(float(avg1)*10/random.randint(12,18))
                            if avgShare.find(".") != -1:
                                avgShare = avgShare[:avgShare.find(".")]
                            dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + tmp.replace(tmp.split(",")[0],"")
                            result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                            x= x + 1
                        elif huxing_shi == "2":
                            tmp = dic[city][district][street][xiaoqu_name][huxing_shi]
                            avg2 = tmp.split(",")[0]
                            avg1 = str(float(avg2)/1.2)
                            avg3 = str(float(avg2)*1.2)
                            if avg1.find(".") != -1:
                                avg1 = avg1[:avg1.find(".")]
                            if avg2.find(".") != -1:
                                avg2 = avg2[:avg2.find(".")]
                            if avg3.find(".") != -1:
                                avg3 = avg3[:avg3.find(".")]
                            avgShare = str(float(avg1)*10/random.randint(12,18))
                            if avgShare.find(".") != -1:
                                avgShare = avgShare[:avgShare.find(".")]
                            dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + tmp.replace(tmp.split(",")[0],"")
                            result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                            x= x + 1
                        elif huxing_shi == "3":
                            tmp = dic[city][district][street][xiaoqu_name][huxing_shi]
                            avg3 = tmp.split(",")[0]
                            avg2 = str(float(avg3)/1.2)
                            avg1 = str(float(avg3)/1.44)
                            if avg1.find(".") != -1:
                                avg1 = avg1[:avg1.find(".")]
                            if avg2.find(".") != -1:
                                avg2 = avg2[:avg2.find(".")]
                            if avg3.find(".") != -1:
                                avg3 = avg3[:avg3.find(".")]
                            avgShare = str(float(avg1)*10/random.randint(12,18))
                            if avgShare.find(".") != -1:
                                avgShare = avgShare[:avgShare.find(".")]
                            dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + tmp.replace(tmp.split(",")[0],"")
                            result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                            x= x + 1
                    else:
                        pass
                    #result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + str(huxing_shi) + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                    #print dic[city][district][street][xiaoqu_name][huxing_shi]
                    '''#print i
                    result.write(city+","+district+","+street+","+str(i)+"\n")
                    '''
    