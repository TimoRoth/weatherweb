Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_chart(div_id, title) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false,
            marginLeft: 0,
            marginRight: 0
        },
        title: {text: title},
        xAxis: {
            type: 'datetime',
            gridLineWidth: 1
        },
        plotOptions: {
            pointInterval: 10,
            line: {marker: {enabled: false}},
            area: {marker: {enabled: false}}
        },
        tooltip: {
            shared: true,
            crosshairs: [true],
            valueDecimals: 1
        }
    });
    chart.showLoading("Loading Data...");
    chart.yAxis[0].remove();
    chart.addAxis({title: {text: title}, id: "main_axis"});
    return chart;
}

function add_sensor(chart, url) {
    $.getJSON(url, function(jdata) {
        chart.addSeries({
            name: jdata.aux.sensor_name + " - " + jdata.aux.unit,
            yAxis: "main_axis",
            data: jdata.data
        });
        chart.hideLoading();
    });
}
