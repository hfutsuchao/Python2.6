#coding:utf-8

dic = {}
tmpFile = open('tmpFile.txt','w')
xqxxs = open('C:/users/suchao/desktop/xqq.txt','r').readlines()

listIn = []

#bjs = ['宝润苑','名都园','保利蔷薇','长城溪溪小镇','10AM新坐标','栖美国际','东方财富','幸福东园','鑫融皓月家园','冠城名敦道','滨河小区','水上公园华城','东一时区','波特兰花园','龙山新新家园','韩庄子二里','红螺家园','远洋德邑','MOMA万万树','朝阳新城','北郊农场','人济庄园','左安浦园','长河湾','于家园二区','万科四季花城','沿海赛洛城','左安漪园','青春苑西区','金台园','万科假日风景','上海康城','春申景城','鑫都城仁和花苑','皇都花园','万科朗润园','牡丹新村(七宝)','上海春城','爱庐世纪新苑','银都新村','东方花园','虹中路2弄','夏朵小城(华银坊)','天籁园','莘建一村','龙柏四村','莘闵花园','昆阳小区','保利名苑','昆阳住宅三区','君临天下花园','万兆家园','金榜新苑','大上海国际花园','众众德尚世嘉(众众德尚世家)','东苑米蓝城','日月华庭','碧林湾','龙柏西郊公寓','红旗新村','万商电脑城','万托家园','一冶花园','东方皇宫','东方广场大厦','东海大厦','万象城','东佳大厦','万事达名苑一期','万科俊园','东湖豪庭','东莞外贸大厦','东湖大厦','东乐大厦','上步大厦','上沙花园','鸿基大厦','龙秋村','龙福居','龙溪花园','鼎盛时代','鼎城国际','黄都广场','鸿昌广场','黄木岗','黄埔雅苑四期','黄埔雅苑二期','黄埔雅苑三期','黄埔雅苑一期','鹏盛村','金龙苑','金雅阁','银丰花园','金门大厦','逸泉山庄','银都大厦','龙湖大厦','黄花新村','黄田','黄华路大院房改电梯','黄华路公安厅宿舍','黄华路','金鹿山庄','金迪城市花园','金碧雅苑','金碧绿洲','金碧新城','金德苑','金桂园凌云居','金泉山庄','金满苑','金满花园','麓苑阁','粤溪苑','紫来居','紫竹苑','翠榕居','翠逸家园','聚景雅居','腾龙阁']
for xqxx in xqxxs:
    try:
        city, district, xiaoquId, name, pinyin    = xqxx.split('\t')
    except:
        print xqxx
    
    '''for xq in bjs:
        if pinyin.find(xq) != -1:
            if city+district+pinyin not in dic:
                dic[city+'\t'+district+'\t'+pinyin] = {}
                dic[city+'\t'+district+'\t'+pinyin][xiaoquId] = name
            else:
                dic[city+district+pinyin][xiaoquId] = name
            listIn.append(xq)
            break
        '''
    if city+district+pinyin not in dic:
        dic[city+'\t'+district+'\t'+pinyin] = {}
        dic[city+'\t'+district+'\t'+pinyin][xiaoquId] = name
    else:
        dic[city+district+pinyin][xiaoquId] = name
for i in sorted(dic.items(), key= lambda y:y[0], reverse=False):
    for key in i[1]:
        tmpFile.write(i[0][:-1] + '\t' + key + '\t' + i[1][key] + '\n')

for i in set(listIn):
    print i