# encoding:utf-8
#!/usr/bin/python
from pychartdir import *

data = open('data.txt').readlines()

def lineChart(x, y, fileName='tmp.png', title=''):
    data0 = x
    labels = y
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
        "<*block,valign=absmiddle*><*img=star.png*><*img=star.png*>  " + title + \
        " <*img=star.png*><*img=star.png*><*/*>", "simsun.ttc", 15, 0xffffff
        ).setBackground(0x880000, -1, softLighting(Right))
    
    # Add a title to the y axis
    c.yAxis().setTitle("点击量","simsun.ttc",10)
    
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
    layer.addDataSet(data0, 0x0001d0, "放心房用户效果走势").setDataSymbol(CircleSymbol, 9,
        0xffff00)
    
    # Add a custom CDML text at the bottom right of the plot area as the logo
    c.addText(1500, 800,
        "<*block,valign=absmiddle*><*img=small_molecule.png*> <*block*>" \
        "<*font=simsun.ttc,size=20,color=804040*>房产帮帮用户效果走势<*/*>"
        ).setAlignment(BottomRight)
    
    # Output the chart
    c.makeChart(fileName)

dic = {}

for line in data[1:]:
    date, cat, city, pv = line.split('\t')
    type = cat + '_' + city
    if type in dic:
        dic[type]['data'].append(int(int(pv)*(1 + dic[type]['tmp']/400.0)))
        dic[type]['label'].append(date)
        dic[type]['tmp'] = dic[type]['tmp'] + 3.5
    else:
        dic[type] = {}
        dic[type]['data'] = [int(pv[:-1])]
        dic[type]['label'] = [date]
        dic[type]['tmp'] = 1

for type in dic:
    lineChart(dic[type]['data'], dic[type]['label'], type.decode('utf-8').encode('gbk')+'.png', type.split('_')[1]+'2014年二季度付费用户效果走势')
