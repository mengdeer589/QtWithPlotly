/**
 * 
myChart = document.getElementById("chart");
myChart.on('plotly_click', function(eventData) {console.log(eventData)});
 */
/**
 * 检查图表是否存在
 * @returns {boolean} 返回一个布尔值，表示图表是否存在
 */
function check_chart() { return !!myChart; }
try {
    var channel = new QWebChannel(qt.webChannelTransport, function () {
        communicate = channel.objects.communicate;

        // 连接到Python对象
        communicate.connect_result("来自前端的消息~").then(function (message) {
            console.log(message);
        });
    })
}
catch (err) { console.log("QWebChannel is not loaded"); alert("Qt与前端连接失败") }

let myChart = document.getElementsByClassName("js-plotly-plot")[0];
if (!myChart) { myChart = document.getElementById("chart") }
if (!myChart) { alert("图表对象定位失败！") } else {
    myChart.on('plotly_click', function (data) {
        const point = data?.points[0];
    
        const json_data = {
            click_x: point?.x,
            click_y: point?.y,
            curveNumber: point?.curveNumber,
            pointIndex: point?.pointIndex,
            // current_annotations_count: myChart.layout.annotations?.length || 0,
            trace_name: point?.fullData?.name || "未定义",
            trace_mode: point?.fullData?.mode || "lines+markers",
            line_width: point?.fullData?.line?.width || 5,
            line_color: point?.fullData?.line?.color || "red",
            line_dash: point?.fullData?.line?.dash || "solid",
            marker_size: point?.fullData?.marker?.size || 5,
            marker_color: point?.fullData?.marker?.color || "red",
            marker_symbol: point?.fullData?.marker?.symbol || "circle",
            plot_type: point?.fullData?.type || "scatter",        
        };
    
        const data_str = JSON.stringify(json_data);
        try {
            communicate.click_info(data_str);
        } catch (err) {
            console.log("QWebChannel is not loaded");
            alert("发送失败");
        }
    });
    myChart.on('plotly_hover', function (data) {
        const point = data.points[0];
    
        const json_data = {
            x: point.x,
            y: point.y,
            curveNumber: point.curveNumber,
            pointIndex: point.pointIndex,
            // current_annotations_count: myChart.layout.annotations.length||0,
        };
        const data_str = JSON.stringify(json_data);
        // console.log(data_str);
        try { communicate.hover_info(data_str) }
        catch (err) { console.log("发送失败", err); alert("发送失败") }
    })
}
/**
 * 修改图表样式
 *
 * @param param 图表样式参数，字符串类型，JSON格式
 * @returns 无返回值
 */
function chart_restyle(param) {
    const parameters = JSON.parse(param);
    const curveNumber = parameters.curveNumber;
    
    Plotly.restyle(myChart, {
        'name': parameters.trace_name,
        'mode': parameters.trace_mode,
        'line.width': parameters.line_width,
        'line.color': parameters.line_color,
        'line.dash': parameters.line_dash,
        'marker.size': parameters.marker_size,
        'marker.color': parameters.marker_color,
        'marker.symbol': parameters.marker_symbol
    }, [curveNumber]);
    
    console.log("修改成功");
}