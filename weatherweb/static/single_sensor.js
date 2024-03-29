Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_chart(div_id, url) {
    const chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false,
            marginLeft: 120,
            marginRight: 120
        },
        title: {text: "..."},
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
    chart.addAxis({title: {text: "..."}, id: "main_axis"});
    chart.addSeries({yAxis: "main_axis", id: "main_series", name: "...", data: []});
    $.getJSON(url, function(jdata) {
        const ax = chart.get("main_axis");
        const series = chart.get("main_series");
        const title = jdata.aux.sensor_name + " - " + jdata.aux.unit;
        chart.setTitle({text: title}, {});
        ax.setTitle({text: title});
        if(jdata.aux.sensor_group == "rain") {
            ax.update({style: {"color": "#0018FF"}, min: 0, max: 10});
            series.update({color: '#0018ff', type: 'area'});
        }
        series.update({name: title});
        series.setData(jdata.data);
        chart.hideLoading();
    });
    return chart;
}
