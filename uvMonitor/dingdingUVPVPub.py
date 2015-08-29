#coding:utf-8
import html
import time
import json
import sys
import os
import config
from datetime import datetime,date
from urllib import unquote
from myMath import MyMath

params = {"UserName":config.gjname,"Domain":"@ganji.com","Password":config.gjpwd}
url = "http://sso.ganji.com/Account/LogOn"

crm = html.Html()
crm.post(url,params,"")

sourceURL = 'http://stat.corp.ganji.com/ReportBase/GetReportData?reportId=34'
citys = [{"Text":"全国","Value":"0"},{"Text":"襄阳市","Value":"412"},{"Text":"WWW","Value":"411"},{"Text":"北京市","Value":"46"},{"Text":"上海市","Value":"47"},{"Text":"天津市","Value":"48"},{"Text":"重庆市","Value":"49"},{"Text":"广州市","Value":"50"},{"Text":"深圳市","Value":"51"},{"Text":"东莞市","Value":"58"},{"Text":"珠海市","Value":"52"},{"Text":"汕头市","Value":"53"},{"Text":"佛山市","Value":"54"},{"Text":"江门市","Value":"55"},{"Text":"中山市","Value":"59"},{"Text":"惠州市","Value":"57"},{"Text":"茂名市","Value":"56"},{"Text":"韶关市","Value":"297"},{"Text":"湛江市","Value":"298"},{"Text":"肇庆市","Value":"299"},{"Text":"梅州市","Value":"300"},{"Text":"汕尾市","Value":"301"},{"Text":"河源市","Value":"302"},{"Text":"阳江市","Value":"303"},{"Text":"清远市","Value":"304"},{"Text":"潮州市","Value":"305"},{"Text":"揭阳市","Value":"306"},{"Text":"云浮市","Value":"307"},{"Text":"顺德","Value":"384"},{"Text":"台山","Value":"385"},{"Text":"阳春","Value":"386"},{"Text":"成都市","Value":"79"},{"Text":"自贡市","Value":"80"},{"Text":"泸州市","Value":"81"},{"Text":"德阳市","Value":"82"},{"Text":"绵阳市","Value":"83"},{"Text":"南充市","Value":"85"},{"Text":"凉山州","Value":"88"},{"Text":"乐山市","Value":"84"},{"Text":"达州市","Value":"87"},{"Text":"宜宾市","Value":"86"},{"Text":"攀枝花市","Value":"308"},{"Text":"广元市","Value":"309"},{"Text":"遂宁市","Value":"310"},{"Text":"内江市","Value":"311"},{"Text":"广安市","Value":"312"},{"Text":"眉山市","Value":"313"},{"Text":"雅安市","Value":"314"},{"Text":"巴中市","Value":"315"},{"Text":"资阳市","Value":"316"},{"Text":"阿坝藏族羌族自治州","Value":"317"},{"Text":"甘孜藏族自治州","Value":"318"},{"Text":"杭州市","Value":"60"},{"Text":"宁波市","Value":"61"},{"Text":"温州市","Value":"62"},{"Text":"嘉兴市","Value":"63"},{"Text":"湖州市","Value":"64"},{"Text":"绍兴市","Value":"65"},{"Text":"金华市","Value":"66"},{"Text":"衢州市","Value":"67"},{"Text":"舟山市","Value":"68"},{"Text":"台州市","Value":"69"},{"Text":"丽水市","Value":"319"},{"Text":"贵阳市","Value":"70"},{"Text":"六盘水市","Value":"71"},{"Text":"遵义市","Value":"72"},{"Text":"安顺市","Value":"73"},{"Text":"铜仁地区","Value":"74"},{"Text":"毕节地区","Value":"75"},{"Text":"黔西南州","Value":"76"},{"Text":"黔东南州","Value":"77"},{"Text":"黔南州","Value":"78"},{"Text":"沈阳市","Value":"89"},{"Text":"大连市","Value":"90"},{"Text":"鞍山市","Value":"91"},{"Text":"抚顺市","Value":"92"},{"Text":"丹东市","Value":"93"},{"Text":"锦州市","Value":"94"},{"Text":"营口市","Value":"95"},{"Text":"辽阳市","Value":"96"},{"Text":"盘锦市","Value":"97"},{"Text":"葫芦岛市","Value":"98"},{"Text":"本溪市","Value":"320"},{"Text":"阜新市","Value":"321"},{"Text":"铁岭市","Value":"322"},{"Text":"朝阳市","Value":"323"},{"Text":"瓦房店","Value":"400"},{"Text":"南京市","Value":"99"},{"Text":"苏州市","Value":"101"},{"Text":"无锡市","Value":"100"},{"Text":"徐州市","Value":"102"},{"Text":"常州市","Value":"103"},{"Text":"南通市","Value":"104"},{"Text":"连云港","Value":"105"},{"Text":"淮安市","Value":"106"},{"Text":"盐城市","Value":"107"},{"Text":"扬州市","Value":"108"},{"Text":"镇江市","Value":"324"},{"Text":"泰州市","Value":"325"},{"Text":"宿迁市","Value":"326"},{"Text":"沭阳","Value":"397"},{"Text":"大丰","Value":"398"},{"Text":"福州市","Value":"109"},{"Text":"厦门市","Value":"110"},{"Text":"莆田市","Value":"111"},{"Text":"三明市","Value":"112"},{"Text":"泉州市","Value":"113"},{"Text":"漳州市","Value":"114"},{"Text":"南平市","Value":"115"},{"Text":"龙岩市","Value":"116"},{"Text":"宁德市","Value":"117"},{"Text":"武夷山","Value":"383"},{"Text":"石家庄市","Value":"35"},{"Text":"唐山市","Value":"36"},{"Text":"邯郸市","Value":"38"},{"Text":"邢台市","Value":"39"},{"Text":"保定市","Value":"40"},{"Text":"张家口市","Value":"41"},{"Text":"承德市","Value":"42"},{"Text":"沧州市","Value":"43"},{"Text":"廊坊市","Value":"44"},{"Text":"秦皇岛市","Value":"37"},{"Text":"衡水市","Value":"45"},{"Text":"定州","Value":"388"},{"Text":"馆陶","Value":"389"},{"Text":"赵县","Value":"390"},{"Text":"正定","Value":"391"},{"Text":"张北","Value":"392"},{"Text":"郑州市","Value":"137"},{"Text":"洛阳市","Value":"138"},{"Text":"平顶山市","Value":"139"},{"Text":"焦作市","Value":"140"},{"Text":"鹤壁市","Value":"141"},{"Text":"新乡市","Value":"142"},{"Text":"安阳市","Value":"143"},{"Text":"南阳市","Value":"145"},{"Text":"漯河市","Value":"144"},{"Text":"济源市","Value":"146"},{"Text":"开封市","Value":"327"},{"Text":"濮阳市","Value":"328"},{"Text":"许昌市","Value":"329"},{"Text":"三门峡市","Value":"330"},{"Text":"商丘市","Value":"331"},{"Text":"信阳市","Value":"332"},{"Text":"周口市","Value":"333"},{"Text":"驻马店市","Value":"334"},{"Text":"明港","Value":"393"},{"Text":"长葛","Value":"394"},{"Text":"鄢陵","Value":"395"},{"Text":"禹州","Value":"396"},{"Text":"长春市","Value":"118"},{"Text":"吉林市","Value":"119"},{"Text":"四平市","Value":"120"},{"Text":"辽源市","Value":"121"},{"Text":"通化市","Value":"122"},{"Text":"白山市","Value":"123"},{"Text":"松原市","Value":"124"},{"Text":"白城市","Value":"125"},{"Text":"延边朝鲜族自治州","Value":"126"},{"Text":"哈尔滨市","Value":"127"},{"Text":"齐齐哈尔市","Value":"128"},{"Text":"鸡西市","Value":"129"},{"Text":"鹤岗市","Value":"130"},{"Text":"双鸭山市","Value":"131"},{"Text":"大庆市","Value":"132"},{"Text":"伊春市","Value":"133"},{"Text":"佳木斯市","Value":"134"},{"Text":"黑河市","Value":"135"},{"Text":"绥化市","Value":"136"},{"Text":"七台河市","Value":"335"},{"Text":"牡丹江市","Value":"336"},{"Text":"大兴安岭地区","Value":"337"},{"Text":"济南市","Value":"147"},{"Text":"青岛市","Value":"148"},{"Text":"威海市","Value":"154"},{"Text":"淄博市","Value":"149"},{"Text":"枣庄市","Value":"150"},{"Text":"东营市","Value":"151"},{"Text":"烟台市","Value":"152"},{"Text":"潍坊市","Value":"153"},{"Text":"莱芜市","Value":"155"},{"Text":"滨州市","Value":"156"},{"Text":"济宁市","Value":"338"},{"Text":"泰安市","Value":"339"},{"Text":"日照市","Value":"340"},{"Text":"临沂市","Value":"341"},{"Text":"德州市","Value":"342"},{"Text":"聊城市","Value":"343"},{"Text":"菏泽市","Value":"372"},{"Text":"垦利","Value":"402"},{"Text":"章丘","Value":"403"},{"Text":"诸城","Value":"404"},{"Text":"合肥市","Value":"157"},{"Text":"芜湖市","Value":"158"},{"Text":"蚌埠市","Value":"159"},{"Text":"马鞍山市","Value":"160"},{"Text":"安庆市","Value":"161"},{"Text":"滁州市","Value":"162"},{"Text":"阜阳市","Value":"163"},{"Text":"宿州市","Value":"164"},{"Text":"巢湖市","Value":"165"},{"Text":"六安市","Value":"166"},{"Text":"淮南市","Value":"344"},{"Text":"淮北市","Value":"345"},{"Text":"铜陵市","Value":"346"},{"Text":"黄山市","Value":"347"},{"Text":"亳州市","Value":"348"},{"Text":"池州市","Value":"349"},{"Text":"宣城市","Value":"350"},{"Text":"桐城","Value":"380"},{"Text":"和县","Value":"381"},{"Text":"霍邱","Value":"382"},{"Text":"南宁市","Value":"176"},{"Text":"桂林市","Value":"168"},{"Text":"柳州市","Value":"167"},{"Text":"梧州市","Value":"169"},{"Text":"钦州市","Value":"170"},{"Text":"贵港市","Value":"171"},{"Text":"玉林市","Value":"172"},{"Text":"百色市","Value":"173"},{"Text":"河池市","Value":"174"},{"Text":"来宾市","Value":"175"},{"Text":"北海市","Value":"351"},{"Text":"防城港市","Value":"352"},{"Text":"贺州市","Value":"353"},{"Text":"崇左市","Value":"354"},{"Text":"海口市","Value":"177"},{"Text":"三亚市","Value":"178"},{"Text":"五指山","Value":"387"},{"Text":"呼和浩特市","Value":"179"},{"Text":"包头市","Value":"180"},{"Text":"乌海市","Value":"181"},{"Text":"赤峰市","Value":"182"},{"Text":"通辽市","Value":"183"},{"Text":"鄂尔多斯市","Value":"184"},{"Text":"呼伦贝尔市","Value":"185"},{"Text":"巴彦淖尔市","Value":"186"},{"Text":"乌兰察布盟","Value":"187"},{"Text":"兴安盟","Value":"188"},{"Text":"锡林郭勒盟","Value":"355"},{"Text":"阿拉善盟","Value":"356"},{"Text":"海拉尔","Value":"401"},{"Text":"太原市","Value":"189"},{"Text":"大同市","Value":"190"},{"Text":"阳泉市","Value":"191"},{"Text":"长治市","Value":"192"},{"Text":"晋城市","Value":"193"},{"Text":"朔州市","Value":"194"},{"Text":"晋中市","Value":"195"},{"Text":"运城市","Value":"196"},{"Text":"忻州市","Value":"197"},{"Text":"临汾市","Value":"198"},{"Text":"吕梁市","Value":"357"},{"Text":"清徐","Value":"405"},{"Text":"临猗","Value":"406"},{"Text":"银川市","Value":"199"},{"Text":"石嘴山市","Value":"373"},{"Text":"吴忠市","Value":"374"},{"Text":"固原市","Value":"375"},{"Text":"中卫县","Value":"376"},{"Text":"兰州市","Value":"200"},{"Text":"金昌市","Value":"201"},{"Text":"白银市","Value":"202"},{"Text":"天水市","Value":"203"},{"Text":"武威市","Value":"204"},{"Text":"张掖市","Value":"205"},{"Text":"平凉市","Value":"206"},{"Text":"酒泉市","Value":"207"},{"Text":"庆阳市","Value":"208"},{"Text":"定西县","Value":"209"},{"Text":"嘉峪关市","Value":"377"},{"Text":"陇南地区","Value":"358"},{"Text":"临夏州","Value":"359"},{"Text":"甘南州","Value":"360"},{"Text":"西安市","Value":"210"},{"Text":"铜川市","Value":"211"},{"Text":"宝鸡市","Value":"212"},{"Text":"咸阳市","Value":"213"},{"Text":"渭南市","Value":"214"},{"Text":"延安市","Value":"215"},{"Text":"汉中市","Value":"216"},{"Text":"榆林市","Value":"217"},{"Text":"安康市","Value":"218"},{"Text":"商洛市","Value":"219"},{"Text":"西宁市","Value":"220"},{"Text":"海东地区","Value":"221"},{"Text":"海北州","Value":"222"},{"Text":"黄南州","Value":"223"},{"Text":"海南州","Value":"224"},{"Text":"果洛州","Value":"225"},{"Text":"玉树州","Value":"226"},{"Text":"海西州","Value":"227"},{"Text":"武汉市","Value":"228"},{"Text":"黄石市","Value":"229"},{"Text":"襄樊市","Value":"230"},{"Text":"十堰市","Value":"231"},{"Text":"荆州市","Value":"232"},{"Text":"宜昌市","Value":"233"},{"Text":"荆门市","Value":"234"},{"Text":"鄂州市","Value":"235"},{"Text":"仙桃市","Value":"236"},{"Text":"潜江市","Value":"237"},{"Text":"孝感市","Value":"361"},{"Text":"黄冈市","Value":"362"},{"Text":"咸宁市","Value":"363"},{"Text":"随州市","Value":"364"},{"Text":"恩施州","Value":"365"},{"Text":"天门市","Value":"366"},{"Text":"神农架林区","Value":"367"},{"Text":"长沙市","Value":"238"},{"Text":"株洲市","Value":"239"},{"Text":"湘潭市","Value":"240"},{"Text":"衡阳市","Value":"241"},{"Text":"邵阳市","Value":"242"},{"Text":"岳阳市","Value":"243"},{"Text":"常德市","Value":"244"},{"Text":"郴州市","Value":"245"},{"Text":"永州市","Value":"246"},{"Text":"娄底市","Value":"247"},{"Text":"张家界市","Value":"368"},{"Text":"益阳市","Value":"369"},{"Text":"怀化市","Value":"370"},{"Text":"湘西州","Value":"371"},{"Text":"南昌市","Value":"248"},{"Text":"景德镇市","Value":"249"},{"Text":"萍乡市","Value":"250"},{"Text":"九江市","Value":"251"},{"Text":"新余市","Value":"252"},{"Text":"鹰潭市","Value":"253"},{"Text":"赣州市","Value":"254"},{"Text":"上饶市","Value":"258"},{"Text":"吉安市","Value":"255"},{"Text":"抚州市","Value":"257"},{"Text":"宜春市","Value":"256"},{"Text":"永新","Value":"399"},{"Text":"昆明市","Value":"259"},{"Text":"曲靖市","Value":"260"},{"Text":"玉溪市","Value":"261"},{"Text":"保山市","Value":"262"},{"Text":"昭通市","Value":"263"},{"Text":"红河县","Value":"268"},{"Text":"西双版纳傣族自治州","Value":"269"},{"Text":"楚雄市","Value":"270"},{"Text":"大理市","Value":"271"},{"Text":"德宏德宏傣族景颇族自治州","Value":"272"},{"Text":"丽江市","Value":"264"},{"Text":"普洱哈尼族彝族自治县","Value":"265"},{"Text":"临沧县","Value":"266"},{"Text":"文山县","Value":"267"},{"Text":"怒江傈傈族自治州","Value":"273"},{"Text":"迪庆迪庆藏族自治州","Value":"274"},{"Text":"乌鲁木齐市","Value":"275"},{"Text":"克拉玛依市","Value":"276"},{"Text":"吐鲁番市","Value":"277"},{"Text":"哈密市","Value":"278"},{"Text":"和田市","Value":"279"},{"Text":"阿克苏市","Value":"280"},{"Text":"喀什市","Value":"281"},{"Text":"伊犁哈萨克自治州","Value":"286"},{"Text":"石河子市","Value":"289"},{"Text":"巴音郭楞蒙古自治州","Value":"283"},{"Text":"克孜勒苏柯尔克孜自治州","Value":"282"},{"Text":"昌吉市","Value":"284"},{"Text":"博尔塔拉蒙古自治州","Value":"285"},{"Text":"塔城市","Value":"287"},{"Text":"阿勒泰市","Value":"288"},{"Text":"库尔勒","Value":"407"},{"Text":"阿拉尔","Value":"408"},{"Text":"图木舒克","Value":"409"},{"Text":"五家渠","Value":"410"},{"Text":"拉萨市","Value":"290"},{"Text":"昌都地区","Value":"291"},{"Text":"山南地区","Value":"292"},{"Text":"日喀则地区","Value":"293"},{"Text":"那曲地区","Value":"294"},{"Text":"阿里地区","Value":"295"},{"Text":"林芝地区","Value":"296"},{"Text":"香港自治区","Value":"378"},{"Text":"澳门自治区","Value":"379"}]
sources = [{"Text":"全流量","Value":"1"},{"Text":"外部访问","Value":"2"},{"Text":"内部访问","Value":"3"},{"Text":"SEO","Value":"4"},{"Text":"付费流量","Value":"5"},{"Text":"非付费流量","Value":"6"}]
categories = [{"Text":"全部","Value":"0"},{"Text":"租房","Value":"29"},{"Text":"合租房","Value":"31"},{"Text":"日租房/短租房","Value":"32"},{"Text":"求租房","Value":"33"},{"Text":"二手房求购","Value":"34"},{"Text":"商铺（租）","Value":"35"},{"Text":"商铺（售）","Value":"36"},{"Text":"写字楼（租）","Value":"37"},{"Text":"写字楼（售）","Value":"38"},{"Text":"厂房/仓库/土地","Value":"90"},{"Text":"小区","Value":"10048"},{"Text":"经纪人店铺","Value":"10049"},{"Text":"二手房出售","Value":"10901"},{"Text":"新房出售","Value":"13057"}]

cityList = ['全国','襄阳市','WWW','北京市','上海市','天津市','重庆市','广州市','深圳市','东莞市','珠海市','汕头市','佛山市','江门市','中山市','惠州市','茂名市','韶关市','湛江市','肇庆市','梅州市','汕尾市','河源市','阳江市','清远市','潮州市','揭阳市','云浮市','顺德','台山','阳春','成都市','自贡市','泸州市','德阳市','绵阳市','南充市','凉山州','乐山市','达州市','宜宾市','攀枝花市','广元市','遂宁市','内江市','广安市','眉山市','雅安市','巴中市','资阳市','阿坝藏族羌族自治州','甘孜藏族自治州','杭州市','宁波市','温州市','嘉兴市','湖州市','绍兴市','金华市','衢州市','舟山市','台州市','丽水市','贵阳市','六盘水市','遵义市','安顺市','铜仁地区','毕节地区','黔西南州','黔东南州','黔南州','沈阳市','大连市','鞍山市','抚顺市','丹东市','锦州市','营口市','辽阳市','盘锦市','葫芦岛市','本溪市','阜新市','铁岭市','朝阳市','瓦房店','南京市','苏州市','无锡市','徐州市','常州市','南通市','连云港','淮安市','盐城市','扬州市','镇江市','泰州市','宿迁市','沭阳','大丰','福州市','厦门市','莆田市','三明市','泉州市','漳州市','南平市','龙岩市','宁德市','武夷山','石家庄市','唐山市','邯郸市','邢台市','保定市','张家口市','承德市','沧州市','廊坊市','秦皇岛市','衡水市','定州','馆陶','赵县','正定','张北','郑州市','洛阳市','平顶山市','焦作市','鹤壁市','新乡市','安阳市','南阳市','漯河市','济源市','开封市','濮阳市','许昌市','三门峡市','商丘市','信阳市','周口市','驻马店市','明港','长葛','鄢陵','禹州','长春市','吉林市','四平市','辽源市','通化市','白山市','松原市','白城市','延边朝鲜族自治州','哈尔滨市','齐齐哈尔市','鸡西市','鹤岗市','双鸭山市','大庆市','伊春市','佳木斯市','黑河市','绥化市','七台河市','牡丹江市','大兴安岭地区','济南市','青岛市','威海市','淄博市','枣庄市','东营市','烟台市','潍坊市','莱芜市','滨州市','济宁市','泰安市','日照市','临沂市','德州市','聊城市','菏泽市','垦利','章丘','诸城','合肥市','芜湖市','蚌埠市','马鞍山市','安庆市','滁州市','阜阳市','宿州市','巢湖市','六安市','淮南市','淮北市','铜陵市','黄山市','亳州市','池州市','宣城市','桐城','和县','霍邱','南宁市','桂林市','柳州市','梧州市','钦州市','贵港市','玉林市','百色市','河池市','来宾市','北海市','防城港市','贺州市','崇左市','海口市','三亚市','五指山','呼和浩特市','包头市','乌海市','赤峰市','通辽市','鄂尔多斯市','呼伦贝尔市','巴彦淖尔市','乌兰察布盟','兴安盟','锡林郭勒盟','阿拉善盟','海拉尔','太原市','大同市','阳泉市','长治市','晋城市','朔州市','晋中市','运城市','忻州市','临汾市','吕梁市','清徐','临猗','银川市','石嘴山市','吴忠市','固原市','中卫县','兰州市','金昌市','白银市','天水市','武威市','张掖市','平凉市','酒泉市','庆阳市','定西县','嘉峪关市','陇南地区','临夏州','甘南州','西安市','铜川市','宝鸡市','咸阳市','渭南市','延安市','汉中市','榆林市','安康市','商洛市','西宁市','海东地区','海北州','黄南州','海南州','果洛州','玉树州','海西州','武汉市','黄石市','襄樊市','十堰市','荆州市','宜昌市','荆门市','鄂州市','仙桃市','潜江市','孝感市','黄冈市','咸宁市','随州市','恩施州','天门市','神农架林区','长沙市','株洲市','湘潭市','衡阳市','邵阳市','岳阳市','常德市','郴州市','永州市','娄底市','张家界市','益阳市','怀化市','湘西州','南昌市','景德镇市','萍乡市','九江市','新余市','鹰潭市','赣州市','上饶市','吉安市','抚州市','宜春市','永新','昆明市','曲靖市','玉溪市','保山市','昭通市','红河县','西双版纳傣族自治州','楚雄市','大理市','德宏德宏傣族景颇族自治州','丽江市','普洱哈尼族彝族自治县','临沧县','文山县','怒江傈傈族自治州','迪庆迪庆藏族自治州','乌鲁木齐市','克拉玛依市','吐鲁番市','哈密市','和田市','阿克苏市','喀什市','伊犁哈萨克自治州','石河子市','巴音郭楞蒙古自治州','克孜勒苏柯尔克孜自治州','昌吉市','博尔塔拉蒙古自治州','塔城市','阿勒泰市','库尔勒','阿拉尔','图木舒克','五家渠','拉萨市','昌都地区','山南地区','日喀则地区','那曲地区','阿里地区','林芝地区','香港自治区','澳门自治区']

def getUVPVPub(StartDate,EndDate,majorCategory='全部',city='全国',source='1',days=1):
    global crm
    global citys
    global sourceURL
    global sources
    global categories
    
    crm.headerConf({'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
    for c in citys:
        if city == c['Text']:
            city = c['Value']
    
    '''for s in sources:
        if source == s['Text']:
            source = s['Value']'''
    
    for c in categories:
        if majorCategory == c['Text']:
            majorCategory = c['Value']
    
    datas = {
             'CateKey':'7',
    'CityKey':city,
    'EndDate':EndDate,
    'ListMethod':'1',
    'MajorCateKey':majorCategory,
    'Source1':source,
    'StartDate':StartDate,
    'page':'1',
    'size':'10000'
             }
    
    dataR = crm.post(sourceURL,datas,'')
    dataR = json.loads(dataR)
    tmpDic = {}
    #print len(dataR),len(dataR['data'])
    for data in dataR['data']:
        tmpDic[data["Col1"]] = {'city':data["Col2"],'uv':data["Col4"],'pv':data["Col8"],'v':data["Col6"],'pub':data["Col11"]}
    #print json.dumps(tmpDic,indent=1)
    '''dataResult = {}
    for i in sorted(tmpDic.items(), key=lambda x:x[1]['uv'], reverse=True):
        dataResult[i[0]] = {}
        dataResult[i[0]]['uv'] = int(i[1]['uv'])/days
        dataResult[i[0]]['v'] = int(i[1]['v'])/days
        dataResult[i[0]]['pv'] = int(i[1]['pv'])/days
        dataResult[i[0]]['pub'] = int(i[1]['pub'])/days'''
    return tmpDic

if __name__ == '__main__':
    
    startDate = '2015-03-24'
    EndDate = '2015-03-26'
    
    dic = {}
    
    mainCategories = ['租房' , '合租房']
    expandCat = {'租赁':['租房', '合租房']}
    cityList = ['全国','北京市','上海市','广州市']
    
    for city in cityList:
        #print city
        dic[city] = {}
        for cat in mainCategories:
            dic[city][cat] = getUVPVPub(startDate,EndDate,cat,city,'1',3)
            #print json.dumps(dic[cat],indent=1)
    #print json.dumps(dic['北京市']['租房'],indent=1)
    
    
    dicR = {}
    for eCat in expandCat:
        dicR[eCat] = {}
        for cat in expandCat[eCat]:
            for city in dic:
                    for date in dic[city][cat]:
                        if date not in dicR[eCat]:
                            dicR[eCat][date] = {}
                            if city not in dicR[eCat][date]:
                                dicR[eCat][date][city] = {}
                                dicR[eCat][date][city]['uv'] = dic[city][cat][date]['uv']
                                dicR[eCat][date][city]['pv'] = dic[city][cat][date]['pv']
                            else:
                                dicR[eCat][date][city]['uv'] = dicR[eCat][date][city]['uv'] + dic[city][cat][date]['uv']
                                dicR[eCat][date][city]['pv'] = dicR[eCat][date][city]['pv'] + dic[city][cat][date]['pv']
                        elif city not in dicR[eCat][date]:
                            dicR[eCat][date][city] = {}
                            dicR[eCat][date][city]['uv'] = dic[city][cat][date]['uv']
                            dicR[eCat][date][city]['pv'] = dic[city][cat][date]['pv']
                        else:
                            dicR[eCat][date][city]['uv'] = dicR[eCat][date][city]['uv'] + dic[city][cat][date]['uv']
                            dicR[eCat][date][city]['pv'] = dicR[eCat][date][city]['pv'] + dic[city][cat][date]['pv']
                            
    #print json.dumps(dicR,indent=1)
    for cat in expandCat:
            wFile = open('UVPVPubDingDing/' + cat.replace('/','').decode('utf-8').encode('gbk') + '.txt','w')
            for i in sorted(dicR[cat].items(), key=lambda x:x[0], reverse=False):
                wFile.write(str(i[0]) + '\t' + str(i[1]['全国']['uv']) + '\t' + str(i[1]['北京市']['uv']) + '\t' + str(i[1]['上海市']['uv']) + '\t' + str(i[1]['广州市']['uv']) + '\n')