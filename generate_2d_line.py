import plotly.graph_objects as go
from plotly.subplots import make_subplots
config = {
        "scrollZoom": True,
        "editable": False,
        "staticPlot": False,
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "sendDataToCloud",
            "editInChartStudio",
            "lasso2d",
            "drawrect",
            "select2d",
        ],
        "toImageButtonOptions": {
            "format": "svg",
            "filename": "custom_image",
            "scale": 1,
        },
        "showLink": False,
        "showTips": True,
        "locale": "zh",
        "doubleClick": "reset+autosize",
        "doubleClickDelay": 300,
        "sendData": False,
        "watermark": True,
        "modeBarButtonsToAdd": ["toggleHover","hoverCompareCartesian", "toggleSpikelines", "tableRotation"],
        "autosizable": True,
    }
# 创建一个3行2列的子图网格，并调整子图间的间距
fig = make_subplots(rows=3, cols=2,
                    # subplot_titles=("Scatter", "Line", "Line_Mark", "Area", "Bar"),
                    horizontal_spacing=0.05,  # 减小水平间距
                    vertical_spacing=0.05)   # 减小垂直间距

# Scatter
fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[0, 3, 6, 9]), row=1, col=1)

# Line
fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[0, 5, 2, 8], mode='lines'), row=1, col=2)

# Line_Mark
fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[5, 3, 7, 1], mode='lines+markers'), row=2, col=1)

# Area
fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=[1, 3, 5, 7], fill='tozeroy'), row=2, col=2)

# Bar
fig.add_trace(go.Bar(x=['a', 'b', 'c'], y=[2, 5, 7]), row=3, col=1)

# 更新布局
fig.update_layout(height=900, width=900, showlegend=False)

# 更新每个子图的布局
for i in range(1, 4):
    fig.update_xaxes( row=i, col=1)
    fig.update_yaxes( row=i, col=1)

for i in range(1, 3):
    fig.update_xaxes( row=1, col=i)
    fig.update_yaxes( row=1, col=i)

fig.update_xaxes( row=2, col=2)
fig.update_yaxes( row=2, col=2)

for temp in [
            "ggplot2",
            "seaborn",
            "simple_white",
            "plotly",
            "plotly_white",
            "plotly_dark",
            "presentation",
            "xgridoff",
            "ygridoff",
            "gridon",
            "none",
        ]:
    config["toImageButtonOptions"]["filename"]=temp
    fig.update_layout(template=temp)
    # fig.show(config=config)
    print(f"    <file>chart_theme/{temp}.svg</file>")