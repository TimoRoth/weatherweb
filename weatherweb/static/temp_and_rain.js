Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_tnr_chart(div_id) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false,
            marginLeft: 120,
            marginRight: 120
        },
        title: {text: "Temperatur und Regen"},
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
    chart.addAxis({title: {text: "Temperatur - °C"}, id: "temp_axis"});
    chart.addAxis({title: {text: "Niederschlag - mm", style: {"color": "#0018FF"}}, id: "rain_axis", gridLineWidth: 0, opposite: true, min: 0, max: 10.0});
    return chart;
}

function add_temp_sensor(chart, url) {
    $.getJSON(url, function(jdata) {
        chart.addSeries({
            name: jdata.aux.sensor_name + " - " + jdata.aux.unit,
            yAxis: "temp_axis",
            data: jdata.data
        });
        chart.hideLoading();
    });
}

function add_rain_sensor(chart, url) {
    $.getJSON(url, function(jdata) {
        chart.addSeries({
            name: jdata.aux.sensor_name + " - " + jdata.aux.unit,
            yAxis: "rain_axis",
            type: 'area',
            data: jdata.data
        });
        chart.hideLoading();
    });
}
