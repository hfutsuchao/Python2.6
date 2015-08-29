show = open(dateNow+'resultShow.txt','r')
click = open(dateNow+'resultClick.txt','r')
prices = {}
prices['500'] = 0
prices['1000'] = 0
prices['2000'] = 0
prices['3000'] = 0
prices['4000'] = 0
prices['5000'] = 0
prices['8000'] = 0
prices['8000+'] = 0
shiXing = {}
districts = {}
streets = {}
companys = {}
areas = {}
zhuangxius = {}
pics = {}

#端口贴
for s in click:
    houseId=s.split('\t')[0]
    city=s.split('\t')[1]
    times=s.split('\t')[2]
    uuid=s.split('\t')[3]
    company=s.split('\t')[4]
    images=s.split('\t')[8]
    address=city+'-'+s.split('\t')[5]+'\t'+s.split('\t')[6]
    price=s.split('\t')[11]
    xiaoqu=s.split('\t')[12]
    area=s.split('\t')[14]
    zhuangxiu=s.split('\t')[16]
    shi=s.split('\t')[18]
    ting=s.split('\t')[19]
    wei=s.split('\t')[20]
    peizhi=s.split('\t')[21]
#免费贴
for s in click:
    houseId=s.split('\t')[0]
    city=s.split('\t')[1]
    times=s.split('\t')[2]
    uuid=s.split('\t')[3]
    #company=s.split('\t')[4]
    images=s.split('\t')[7]
    address=city+'-'+s.split('\t')[4]+'\t'+s.split('\t')[5]
    price=s.split('\t')[8]
    xiaoqu=s.split('\t')[9]
    area=s.split('\t')[11]
    zhuangxiu=s.split('\t')[13]
    shi=s.split('\t')[15]
    ting=s.split('\t')[16]
    wei=s.split('\t')[17]
    peizhi=s.split('\t')[18]
    #价格分析
    if prices<=500:
        prices['500'] = prices['500'] + 1
    elif prices<=1000:
        prices['1000'] = prices['1000'] + 1
    elif prices<=2000:
        prices['2000'] = prices['2000'] + 1
    elif prices<=3000:
        prices['3000'] = prices['3000'] + 1
    elif prices<=4000:
        prices['4000'] = prices['4000'] + 1
    elif prices<=5000:
        prices['5000'] = prices['5000'] + 1
    elif prices<=8000:
        prices['8000'] = prices['8000'] + 1
    elif prices>8000:
        prices['8000+'] = prices['8000+'] + 1

    '''if price in prices:
        prices[price] = prices[price] + 1
    else:
        prices[price] = 1'''
    #室型分析
    if shi in shiXing:
        shiXing[shi] = shiXing[shi] + 1
    else:
        shiXing[shi] = 1
    #区域
    if district in districts:
        districts[district] = districts[district] + 1
    else:
        districts[district] = 1
    #街道
    if street in streets:
        streets[street] = streets[street] + 1
    else:
        streets[street] = 1
    #图片数
    if images in pics:
        pics[images] = pics[images] + 1
    else:
        pics[images] = 1