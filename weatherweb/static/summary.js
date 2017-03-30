Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_summary_chart(div_id, data_url, dura_unit, wind_speed_id, wind_dir_id, temp_id, humid_id, rain_id, bila_id) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div_id,
            alignTicks: false
        },
        title: {text: "Übersicht"},
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

    var temp_color = "#d95f02";
    var temp_name = "Temperatur - °C";
    var wind_color = "#1b9e77";
    var wind_name = "Windgeschwindigkeit - m/s";
    var humi_color = "#7570b3";
    var humi_name = "Luftfeuchtigkeit - %";
    var bila_color = "#e7298a";
    var bila_name = "Strahlung - W/m²";
    var rain_color = "#0018ff";
    var rain_name = "Niederschlag - mm/" + dura_unit;

    chart.showLoading("Lade Daten...");
    chart.yAxis[0].remove();
    chart.addAxis({title: {text: rain_name, style: {"color": rain_color}}, id: "rain_axis", showEmpty: false, gridLineWidth: 0, opposite: true, floor: 0, max: 7.5}, false);
    chart.addAxis({title: {text: temp_name, style: {"color": temp_color}}, id: "temp_axis", showEmpty: false}, false);
    chart.addAxis({title: {text: wind_name, style: {"color": wind_color}}, id: "wind_speed_axis", showEmpty: false, gridLineWidth: 0, floor: 0, opposite: true}, false);
    chart.addAxis({title: {text: humi_name, style: {"color": humi_color}}, id: "humid_axis", showEmpty: false, gridLineWidth: 0, opposite: true, floor: 0, max: 100}, false);
    chart.addAxis({title: {text: bila_name, style: {"color": bila_color}}, id: "bila_axis", showEmpty: false, gridLineWidth: 0}, false);
    var rain_series = chart.addSeries({name: rain_name, yAxis: "rain_axis", color: rain_color, type: "area"}, false, false);
    var temp_series = chart.addSeries({name: temp_name, yAxis: "temp_axis", color: temp_color}, false, false);
    var wind_series = chart.addSeries({name: wind_name, yAxis: "wind_speed_axis", color: wind_color}, false, false);
    var humi_series = chart.addSeries({name: humi_name, yAxis: "humid_axis", color: humi_color}, false, false);
    var bila_series = chart.addSeries({name: bila_name, yAxis: "bila_axis", color: bila_color}, false, false);

    var update_function = function() {
        chart.redraw(true);
        $.getJSON(data_url, function(data) {
            temp_series.setData(data[temp_id].data, false);
            wind_series.setData(data[wind_speed_id].data, false);
            humi_series.setData(data[humid_id].data, false);
            bila_series.setData(data[bila_id].data, false);
            rain_series.setData(data[rain_id].data, false);
            chart.hideLoading();
            chart.redraw(true);
        });
    };

    update_function();
    window.setInterval(update_function, 10 * 60 * 1000);

    return chart;
}
