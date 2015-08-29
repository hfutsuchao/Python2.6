#coding:gbk
import random
xiaoquIn58 = open('C:\\Users\\suchao\\Desktop\\58xiaoqu.txt','r').readlines()
cds = open('cds.txt','r').readlines()

dic={}

for c in cds:
    cityId,cityName,districtId,districtName,streetId,streetName = c.split('\t')
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
    else:
        dic[cityName]={}

for xiaoqu in xiaoquIn58:
    xiaoquAfter = xiaoqu.replace("暂无数据","-")
    xiaoquAfter = xiaoquAfter.replace(" 元/㎡","")
    city,district,street,xiaoqu_name,year,buildingType,subway,sellAvg,sellCount,rent1,rent2,rent3,renCount = xiaoquAfter.split('\t')
    renCount = renCount[:-1]
    sellCount = sellCount.replace("套","")
    renCount = renCount.replace("套","")
    if len(subway.split(','))>=1:
        subway = subway.split(',')[0]
    if subway == "":
        subway = "-"
        print "-"
    buildingType = "住宅"
    '''if rent1 == "-":
        if rent2 == "-":
            if rent3 == "-":
                continue'''
    try:
        if xiaoqu_name in dic[city][district][street]:
            print "小区重复",xiaoqu[:-1]
            dic[city][district][street][xiaoqu_name] = sellAvg + ',' + rent1 + ',' + rent2 + ',' + rent3 + ',' + year + ',' + buildingType + ',' + subway + ',' + sellCount + ',' + renCount
        else:
            dic[city][district][street][xiaoqu_name] = sellAvg + ',' + rent1 + ',' + rent2 + ',' + rent3 + ',' + year + ',' + buildingType + ',' + subway + ',' + sellCount + ',' + renCount
    except:
        #print 'error',xiaoqu[:-1]
        pass
    #print xiaoqu[:-1]
    #print city,district,street,xiaoqu_name,year,buildingType,subway,sellAvg,sellCount,rent1,rent2,rent3,renCount

result = open("jieguo.txt",'w')
for city in dic:
    for district in dic[city]:
        for street in dic[city][district]:
            x = 1
            for xiaoqu_name in dic[city][district][street].keys():
                tmp = dic[city][district][street][xiaoqu_name]
                avg1 = tmp.split(",")[1]
                avg2 = tmp.split(",")[2]
                avg3 = tmp.split(",")[3]
                if (street != "其他") and ("all" not in dic[city][district][street][xiaoqu_name]):
                    if avg1 != "-":
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
                        dic[city][district][street][xiaoqu_name] = {}
                        dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + ',' + tmp.split(",")[4] + ',' + tmp.split(",")[5] + ',' + tmp.split(",")[6]
                        result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                        x= x + 1
                    elif avg2 != "-":
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
                        dic[city][district][street][xiaoqu_name] = {}
                        dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + ',' + tmp.split(",")[4] + ',' + tmp.split(",")[5] + ',' + tmp.split(",")[6]
                        result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                        x= x + 1
                    elif avg3 != "-":
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
                        dic[city][district][street][xiaoqu_name] = {}
                        dic[city][district][street][xiaoqu_name]["all"] = avg1 + ',' + avg2 + ',' + avg3 + ',' + avgShare + ',' + tmp.split(",")[4] + ',' + tmp.split(",")[5] + ',' + tmp.split(",")[6]
                        result.write(city + ',' + district + ',' + street + ',' + xiaoqu_name + ',' + dic[city][district][street][xiaoqu_name]["all"]+'\n')
                        x= x + 1
                else:
                    pass