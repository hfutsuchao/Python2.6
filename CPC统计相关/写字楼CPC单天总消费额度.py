# -*- coding: utf-8 -*-
# 统计几天内CPC总消费额度
import time, MySQLdb, os
from pychartdir import *

result = open('xzlresult.txt','w')

#频道类型
arr = [8,9]

sum = 0
timeNow = int(time.time())
dateNow = time.strftime('%Y-%m-%d',time.localtime(timeNow))
dayNow = time.strftime('%H:%M:%S',time.localtime(timeNow))
day = dateNow[8:10]
month = dateNow[5:7]
year = dateNow[0:4]
conn=MySQLdb.connect(host="192.168.116.20",user="lixueshi",passwd="i14p4Dkyd",port=3810,db="house_cpc",charset="utf8")
for houseType in arr:
    sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\') AND click_time<='+str(timeNow)+' GROUP BY 点击时间 ;'
    #连接
    cursor = conn.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        sum = sum + row[1]
result.write(dateNow+'\t'+str(sum)+'\n')
'''
#前面几天的消费总额统计
timeCheck = timeNow-99*86400+1
dateCheck = time.strftime('%Y-%m-%d',time.localtime(timeCheck))
dayCheck = time.strftime('%H:%M:%S',time.localtime(timeCheck))
day = dateCheck[8:10]
print day
month = dateCheck[5:7]
year = dateCheck[0:4]
#print day,month
'''
for i in range(0,101):
    sumOther = 0
    for houseType in arr:
        #sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*i)+' AND click_time<=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*(i-1))+' GROUP BY 点击时间 ;'
        sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*i)+' AND click_time<=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*(i-1))+' GROUP BY 点击时间 ;'
        #连接
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            sumOther = sumOther + row[1]
    '''sumOther2 = 0
    for houseType in arr:
        #sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*i)+' AND click_time<=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*(i-1))+' GROUP BY 点击时间 ;'
        sql = 'SELECT SUBSTR(FROM_UNIXTIME(click_time),1,10) 点击时间, SUM(real_price) 实际扣费 FROM house_click_record_12_'+str(houseType)+' WHERE status=1 AND click_time>=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*i)+' AND click_time<=UNIX_TIMESTAMP(\''+dateNow+'\')-'+str(86400*(i-1))+' and SUBSTR(FROM_UNIXTIME(click_time),12,8)<=\''+dayCheck+'\' GROUP BY 点击时间 ;'
        #连接
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            sumOther2 = sumOther2 + row[1]'''
    #print sumOther2,sumOther,str(sumOther2/sumOther*100)[0:5]+'%'
    if 0 != int(day)-1:
        day = str(int(day) - 1)
        if len(day) == 1:
            day = '0' + day
        #print month,day
        result.write(year+'-'+month+'-'+day+'\t'+str(sumOther)+'\n')
    else:
        tmpTime = time.mktime(time.strptime(year+month+day, '%Y%m%d')) - 1
        day = time.strftime('%d',time.localtime(tmpTime))
        month = str(int(month) - 1)
        if len(month) == 1:
            month = '0' + month
        #print month,day
        result.write(year+'-'+month+'-'+day+'\t'+str(sumOther)+'\n')
result.close()
#关闭
conn.close()


#生成走势图
# encoding:utf-8
#!/usr/bin/python

data = open('xzlresult.txt').readlines()
# The data for the chart

data0 = [i.split('\t')[1][:-1] for i in data]
data0.reverse()
# The labels for the chart
labels = [i.split('\t')[0][8:10] for i in data]
labels.reverse()
# Create a XYChart object of size 600 x 300 pixels, with a pale red (ffdddd)
# background, black border, 1 pixel 3D border effect and rounded corners.
c = XYChart(1900, 900, 0xffdddd, 0x000000, 1)
c.setRoundedFrame()

# Set the plotarea at (55, 58) and of size 520 x 195 pixels, with white (ffffff)
# background. Set horizontal and vertical grid lines to grey (cccccc).
c.setPlotArea(55, 58, 1820, 760, 0xffffff, -1, -1, 0xcccccc, 0xcccccc)

# Add a legend box at (55, 32) (top of the chart) with horizontal layout. Use 9 pts
# Arial Bold font. Set the background and border color to Transparent.
c.addLegend(55, 32, 0, "simsun.ttc", 9).setBackground(Transparent)

# Add a title box to the chart using 15 pts Times Bold Italic font. The title is in
# CDML and includes embedded images for highlight. The text is white (ffffff) on a
# dark red (880000) background, with soft lighting effect from the right side.
c.addTitle(
    "<*block,valign=absmiddle*><*img=star.png*><*img=star.png*> 一周内CPC总消费走势 " \
    " <*img=star.png*><*img=star.png*><*/*>", "simsun.ttc", 15, 0xffffff
    ).setBackground(0x880000, -1, softLighting(Right))

# Add a title to the y axis
c.yAxis().setTitle("CPC日总扣费","simsun.ttc",10)

# Set the labels on the x axis
c.xAxis().setLabels(labels)

# Add a title to the x axis using CMDL
c.xAxis().setTitle(
    "<*block,valign=absmiddle*><*img=clock.png*> 日期 <*/*>","simsun.ttc",10)

# Set the axes width to 2 pixels
c.xAxis().setWidth(2)
c.yAxis().setWidth(2)

# Add a spline layer to the chart
layer = c.addSplineLayer()

# Set the default line width to 2 pixels
layer.setLineWidth(2)

# Add a data set to the spline layer, using blue (0000c0) as the line color, with
# yellow (ffff00) circle symbols.
layer.addDataSet(data0, 0x0001d0, "每天CPC总消费").setDataSymbol(CircleSymbol, 9,
    0xffff00)

# Add a custom CDML text at the bottom right of the plot area as the logo
c.addText(1500, 800,
    "<*block,valign=absmiddle*><*img=small_molecule.png*> <*block*>" \
    "<*font=simsun.ttc,size=20,color=804040*>单天CPC消费总额走势图<*/*>"
    ).setAlignment(BottomRight)

# Output the chart
c.makeChart("xzlzs.png")
