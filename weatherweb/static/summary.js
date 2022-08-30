Highcharts.setOptions({
    global: {
        useUTC: false
    }
});

function create_summary_chart(div_id, data_url, dura_unit, wind_speed_id, wind_dir_id, temp_id, humid_id, rain_id, bila_id, bp_id, dew_id) {
    const chart = new Highcharts.Chart({
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

    const temp_color = "#d95f02";
    const temp_name = "Temperatur - °C";
    const wind_color = "#1b9e77";
    const wind_name = "Windgeschwindigkeit - m/s";
    const humi_color = "#cc2529";
    const humi_name = "Luftfeuchtigkeit - %";
    const bila_color = "#e7298a";
    const bila_name = "Strahlung - W/m²";
    const rain_color = "#0018ff";
    const rain_name = "Niederschlag - mm/" + dura_unit;
    const bp_color = "#922428";
    const bp_name = "Luftdruck - mbar"
    const dew_color = "#396ab1"
    const dew_name = "Taupunkt - °C"

    chart.showLoading("Lade Daten...");
    chart.yAxis[0].remove();
    chart.addAxis({title: {text: rain_name, style: {"color": rain_color}}, id: "rain_axis", showEmpty: false, gridLineWidth: 0, opposite: true, floor: 0, min: 0, max: 7.5}, false);
    chart.addAxis({title: {text: temp_name, style: {"color": temp_color}}, id: "temp_axis", showEmpty: false}, false);
    chart.addAxis({title: {text: wind_name, style: {"color": wind_color}}, id: "wind_speed_axis", showEmpty: false, gridLineWidth: 0, floor: 0, opposite: true}, false);
    chart.addAxis({title: {text: humi_name, style: {"color": humi_color}}, id: "humid_axis", showEmpty: false, gridLineWidth: 0, opposite: true, floor: 0, min: 0, max: 100}, false);
    chart.addAxis({title: {text: bila_name, style: {"color": bila_color}}, id: "bila_axis", showEmpty: false, gridLineWidth: 0}, false);
    chart.addAxis({title: {text:   bp_name, style: {"color":   bp_color}}, id: "bp_axis", showEmpty: false, gridLineWidth: 0}, false);
    const rain_series = chart.addSeries({name: rain_name, yAxis: "rain_axis", color: rain_color, type: "area", data: []}, false, false);
    const temp_series = chart.addSeries({name: temp_name, yAxis: "temp_axis", color: temp_color, data: []}, false, false);
    const wind_series = chart.addSeries({name: wind_name, yAxis: "wind_speed_axis", color: wind_color, visible: false, data: []}, false, false);
    const humi_series = chart.addSeries({name: humi_name, yAxis: "humid_axis", color: humi_color, visible: false, data: []}, false, false);
    const bila_series = chart.addSeries({name: bila_name, yAxis: "bila_axis", color: bila_color, visible: false, data: []}, false, false);
    const bp_series   = chart.addSeries({name:   bp_name, yAxis: "bp_axis", color: bp_color, data: []}, false, false);
    const dew_series  = chart.addSeries({name:  dew_name, yAxis: "temp_axis", color: dew_color, data: []}, false, false);

    const update_function = function() {
        $.getJSON(data_url, function(data) {
            temp_series.setData(data[temp_id].data, false);
            wind_series.setData(data[wind_speed_id].data, false);
            humi_series.setData(data[humid_id].data, false);
            bila_series.setData(data[bila_id].data, false);
            rain_series.setData(data[rain_id].data, false);
            bp_series.setData(data[bp_id].data, false);
            dew_series.setData(data[dew_id].data, false);
            chart.hideLoading();
            chart.redraw(true);
        });
    };

    update_function();
    window.setInterval(update_function, 10 * 60 * 1000);

    return chart;
}
