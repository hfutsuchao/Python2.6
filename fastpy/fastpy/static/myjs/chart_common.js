
function RenderLineChart(id, url) {
  $.getJSON(url, function(data) {
        $('#'+id+'').highcharts({
            chart: {
                zoomType: 'xy',
                type: 'spline'
            },
            title: {
                text: data.title
            },
            subtitle: {
                text: data.sub_title
            },
            xAxis: {
                categories: data.x
            },
            yAxis: {
                title: {
                    text: data.y_title
                }
            },
            tooltip: {
                formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+this.x +', '+ this.y;
                }
            },
            legend: {
                layout: "vertical",
                align: "right",
                verticalAlign: "middle",
                borderWidth: 0
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                }
             },
            series: data.y
        });
    });

}

