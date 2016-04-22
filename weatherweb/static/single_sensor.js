Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_chart(div_id, group, title, url) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false,
            marginLeft: 120,
            marginRight: 120
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
    if(group == "rain") {
        chart.addAxis({title: {text: "Niederschlag - mm/h", style: {"color": "#0018FF"}}, id: "main_axis", min: 0, max: 10});
        chart.addSeries({yAxis: "main_axis", color: '#0018ff', type: 'area', id: "main_series", name: "Niederschlag - mm/h"});
    } else {
        chart.addAxis({title: {text: title}, id: "main_axis"});
        chart.addSeries({yAxis: "main_axis", id: "main_series", name: title});
    }
    $.getJSON(url, function(jdata) {
        var series = chart.get("main_series");
        series.setData(jdata.data);
        chart.hideLoading();
    });
    return chart;
}
