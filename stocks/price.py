#coding:utf-8
from __future__ import with_statement
import urllib2,re,os,time,math,sys
from googleSMS import sendSMS
#初始化参数

t = 0

notice = 0
count = 0

chargeTax = 0.0008
chargeFee = 0.001
chargeChangeOwnner = 0.001
buys = {}
profitCountAll = 0

#获取最新相关信息
def getInfo():
    global buys
    
    #读取自选股配置文件
    with open("shares.conf",'r') as shares:
        for share in shares:
            try:
                shareNum,buyPrice,buyNum,isBuy = share.split("\t")
                #print share,shareNum,buyPrice,buyNum
                buys[shareNum] = {}
                buys[shareNum]['buyPrice'] = float(buyPrice)
                buys[shareNum]['buyNum'] = int(buyNum)
                buys[shareNum]['buyCount'] = int(buyNum)*float(buyPrice)
                buys[shareNum]['isBuy'] = isBuy[:-1]
            except:
                pass
    
    #拼装获取最新股票信息的URL
    myurl = 'http://hq.sinajs.cn/list='
    for key in buys:
        myurl = myurl + key + ','
    response = urllib2.urlopen(myurl[:-1])
    print myurl
    html = response.read()
    tmp = re.findall("var hq_str_(.*)=\"(.*)\";",html)
    #print tmp
    for i in tmp:
        i = list(i)
        shareNum = i[0]
        i= i[1]
        buys[shareNum]['name'] = i.split(",")[0]
        buys[shareNum]['todayStartPrice'] = float(i.split(",")[1])
        buys[shareNum]['yesterdayEndPrice'] = float(i.split(",")[2])
        buys[shareNum]['todayNowPrice'] = float(i.split(",")[3])
        buys[shareNum]['todayHighestPrice'] = float(i.split(",")[4])
        buys[shareNum]['todayLowestPrice'] = float(i.split(",")[5])
        buys[shareNum]['todayBuyOnePrice'] = float(i.split(",")[6])
        buys[shareNum]['todaySellOnePrice'] = float(i.split(",")[7])
        buys[shareNum]['date'] = i.split(",")[30]
        buys[shareNum]['time'] = i.split(",")[31]
    #return buys

##计算手续费、过户费、盈亏情况的函数
def calculate():
    global chargeTax,chargeFee,chargeChangeOwnner,profitCountAll
    profitCountAll = 0
    for shareNum in buys:
        buys[shareNum]['calculate'] = {}
        #买入股票的手续费
        buys[shareNum]['calculate']['chargeBuy'] = max(chargeTax*buys[shareNum]['buyCount'],5.0)
        #以当前价卖出的总额
        buys[shareNum]['calculate']['sellCount'] = int(buys[shareNum]['buyNum'])*float(buys[shareNum]['todayNowPrice'])
        #卖出股票的手续费和过户费等等
        if shareNum[:1] == '6':
            buys[shareNum]['calculate']['chargeSell'] = max(chargeTax*buys[shareNum]['calculate']['sellCount'],5.0) + chargeChangeOwnner*buys[shareNum]['buyNum']/1 + 1 + float(buys[shareNum]['calculate']['sellCount'])*chargeFee
        else:
            buys[shareNum]['calculate']['chargeSell'] = max(chargeTax*buys[shareNum]['calculate']['sellCount'],5.0) + float(buys[shareNum]['calculate']['sellCount'])*chargeFee
        #买卖过程中总的手续费
        buys[shareNum]['calculate']['charges'] = buys[shareNum]['calculate']['chargeBuy'] + buys[shareNum]['calculate']['chargeSell']
        
        #计算盈亏和盈亏比
        buys[shareNum]['calculate']['profitPercent'] = (int((float(buys[shareNum]['todayNowPrice'])/float(buys[shareNum]['buyPrice']) - buys[shareNum]['calculate']['charges']/buys[shareNum]['buyCount'] - 1)*10000))/100.0
        buys[shareNum]['calculate']['profitCount'] = int(buys[shareNum]['calculate']['profitPercent']*buys[shareNum]["buyCount"])/100.0
        if buys[shareNum]['isBuy'] == '1':
            profitCountAll = profitCountAll + buys[shareNum]['calculate']['profitCount']
        #print buys[shareNum]['calculate']['chargeBuy'],buys[shareNum]['calculate']['chargeSell']
#输出结果

def calcCurrentChange():
    rewrite = 0
    global buys
    try:
        #读取最高最低价格记录文件
        tmpRead = open('MaxPrice.data','r').readlines()
        for line in tmpRead:
            shareNum,maxPrice,minPrice = line.split('\t')
            buys[shareNum]['calculate']['maxPrice'] = float(maxPrice)
            buys[shareNum]['calculate']['minPrice'] = float(minPrice[:-1])
        #更新记文件并计算盈亏变化情况
        for shareNum in buys:
            buys[shareNum]['calculate']['notice'] = 0
            #看看是否有新纪录
            if buys[shareNum]['todayHighestPrice'] > buys[shareNum]['calculate']['maxPrice']:
                buys[shareNum]['calculate']['maxPrice'] = buys[shareNum]['todayHighestPrice']
                rewrite = 1
            elif buys[shareNum]['todayLowestPrice'] < buys[shareNum]['calculate']['minPrice']:
                buys[shareNum]['calculate']['minPrice'] = buys[shareNum]['todayLowestPrice']
                rewrite = 1
            
            #计算价格变化情况，负数表示亏损，正数表示盈利损失
            if buys[shareNum]['todayNowPrice'] < buys[shareNum]['buyPrice']:
                changeSmall = int((buys[shareNum]['todayNowPrice'] - buys[shareNum]['buyPrice'])/buys[shareNum]['buyPrice']*10000)/100.0
                changeTrue = int((buys[shareNum]['todayNowPrice'] - buys[shareNum]['calculate']['maxPrice'])/buys[shareNum]['calculate']['maxPrice']*10000)/100.0
                priceChange = str(changeTrue) + '||' + str(changeSmall) + '%/' + str(changeTrue) + '%'
            elif buys[shareNum]['todayNowPrice'] >= buys[shareNum]['buyPrice']:
                changeTrue = int((buys[shareNum]['calculate']['maxPrice'] - buys[shareNum]['todayNowPrice'])/buys[shareNum]['calculate']['maxPrice']*10000)/100.0
                changeSmall = int((buys[shareNum]['calculate']['maxPrice'] - buys[shareNum]['todayNowPrice'])/(buys[shareNum]['calculate']['maxPrice'] - buys[shareNum]['buyPrice'])*10000)/100.0
                tmp = max(changeTrue,changeSmall/5.0)
                priceChange = str(tmp) + '||' + str(changeTrue) + '%|' + str(changeSmall) + '%'
            buys[shareNum]['calculate']['priceChange'] = priceChange
            priceChange = float(priceChange.split('||')[0])
            if (priceChange >= 10 or priceChange<= -8) and buys[shareNum]['isBuy'] == '1':
                buys[shareNum]['calculate']['notice'] = 1
    except Exception,e:
        print e
        tmpWrite = open("maxPrice.data",'w')
        for shareNum in buys:
            buys[shareNum]['calculate']['maxPrice'] = buys[shareNum]['todayHighestPrice']
            buys[shareNum]['calculate']['minPrice'] = buys[shareNum]['todayLowestPrice']
            tmpWrite.write(shareNum + '\t' + str(buys[shareNum]['calculate']['maxPrice']) + '\t' + str(buys[shareNum]['calculate']['minPrice']) + '\n')
    if rewrite == 1:
        tmpWrite = open("maxPrice.data",'w')
        for shareNum in buys:
            tmpWrite.write(shareNum + '\t' + str(buys[shareNum]['calculate']['maxPrice']) + '\t' + str(buys[shareNum]['calculate']['minPrice']) + '\n')
        tmpWrite.close()

#输出函数
def output():
    global count
    getInfo()
    calculate()
    calcCurrentChange()
    
    if profitCountAll>0:
        os.system("color fc")
    else:
        os.system("color fa")
    
    '''for shareNum in buys:
        #上溢通知
        if float(buys[shareNum]['calculate']['profitCount']) >= 0:
            msg = buys[shareNum]['name'] + "    " + str(buys[shareNum]['calculate']['profitCount']) + "    " + str(buys[shareNum]['calculate']['profitPercent']) + "%"
            os.system("mshta vbscript:msgbox(\""+ msg +"\",64,\"profit : "+ str(int(buys[shareNum]['calculate']['profitPercent']*10000)/10000.0) +"%\")(window.close)")
        #send2self('18600219332', '814155356', msg)
    '''
    print 'Name  profitCount  profitPercent  NowPrice  MaxPrice  buyPrice  priceChange'
    for shareNum in buys:
        try:
            msg = buys[shareNum]['name'] + "    " + str(buys[shareNum]['calculate']['profitCount']) + '    ' + str(buys[shareNum]['calculate']['profitPercent']) + '%    ' + str(buys[shareNum]['todayNowPrice']) + "    " + str(buys[shareNum]['calculate']['maxPrice']) + "    " + str(buys[shareNum]['buyPrice']) + '    ' + str(buys[shareNum]['calculate']['priceChange'].split('||')[1])
            #buys[shareNum]['calculate']['label'] = Label(root,text = msg,fg = color)
            if (1 == buys[shareNum]['calculate']['notice']) and (count == 0):
                msgPop = 'Name  profitCount  profitP  NowPrice  MaxP  buyP  priceChange' + msg
                os.system("mshta vbscript:msgbox(\""+ msgPop +"\",48,\"Lose : "+ "StopLost\")(window.close)")
                count = 1800
                #发送短信
                msg = buys[shareNum]['name'] + "    " + str(buys[shareNum]['calculate']['profitCount']) + '    ' + str(buys[shareNum]['calculate']['profitPercent']) + '%    ' + str(buys[shareNum]['todayNowPrice']) + "    " + str(buys[shareNum]['calculate']['priceChange'].split('||')[1])
                msg = msg.decode('gbk').encode('utf-8').decode('utf-8')
                #sendSMS(msg)
            else:
                if count > 0:
                    count = count - 1
                print msg
        except Exception,e:
            print e
    print "\nprofitCountAll\t" + str(profitCountAll)

    time.sleep(2)
    os.system("cls")
    output()
if __name__ == "__main__":
    
    if len(sys.argv) >=2:
        if sys.argv[1] == 'add':
            shareNum = raw_input("ShareNum:")
            buyPrice = raw_input("buyPrice:")
            buyNum = raw_input("buyNum:")
            isBuy = raw_input("isBuy:")
            try:
                getInfo()
            except:
                pass
            shares = open('shares.conf','w')
            shares.write('证劵代码' + '\t' + '购买价格' + '\t' + '购买股数' + '\t' + '是否购买' + '\t' + '#表头' +'\n')
            shares.write(shareNum + '\t' + buyPrice + '\t' + buyNum + '\t' + isBuy + '\n')
            for shareNumOld in buys:
                shares.write(shareNumOld + '\t' + str(buys[shareNumOld]['buyPrice']) + '\t' + str(buys[shareNumOld]['buyNum']) + '\t' + buys[shareNumOld]['isBuy'] + '\n')
            shares.close()
            buys = {}
        elif sys.argv[1] == 'del':
            getInfo()
            shares = open('shares.conf','w')
            shareNum = raw_input("ShareNum:")
            shares.write('证劵代码' + '\t' + '购买价格' + '\t' + '购买股数' + '\t' + '是否购买' + '\t' + '#表头' +'\n')
            for shareNumOld in buys:
                if shareNum != shareNumOld:
                    shares.write(shareNumOld + '\t' + str(buys[shareNumOld]['buyPrice']) + '\t' + str(buys[shareNumOld]['buyNum']) + '\t' + buys[shareNumOld]['isBuy'] + '\n')
            shares.close()
            buys = {}
    output()
