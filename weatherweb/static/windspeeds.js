Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_tnr_chart(div_id, data_url) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false,
            marginLeft: 120,
            marginRight: 120
        },
        title: {text: "Wind Speeds"},
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
    chart.addAxis({title: {text: "Wind Speed - m/s"}, id: "windspeed_axis"});

    $.getJSON(data_url, function(jdata) {
        for(var index in jdata) {
            if (!jdata.hasOwnProperty(index))
                continue;

            var aux = jdata[index]["aux"];
            var data = jdata[index]["data"];

            chart.addSeries({
                name: aux.sensor_name + " - " + aux.unit,
                yAxis: "windspeed_axis",
                data: data
            });
        }
        chart.hideLoading();
    });

    return chart;
}
