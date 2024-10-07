import plotly.graph_objects as go

# 生成数据
x = list(range(20))  # X轴从0到19的整数列表
y1 = [i * 0.5 + (i % 3) for i in x]  # 第一条曲线的数据
y2 = [(i * 0.4 - (i % 2)) for i in x]  # 第二条曲线的数据
y3 = [(i * 0.6 + (i % 5)) for i in x]  # 第三条曲线的数据

# 创建图形对象
fig = go.Figure()

# 添加第一条曲线
fig.add_trace(go.Scatter(showlegend=True,
                         x=x, y=y1,
                         mode='lines+markers',  # 同时显示线条和标记
                         name='曲线1',
                         marker=dict(
                             size=10,  # 标记大小
                             symbol='circle',  # 标记形状
                             color='blue'  # 标记颜色
                         ),
                         line=dict(
                             width=2,  # 线条宽度
                             color='blue',  # 线条颜色
                             dash='solid'  # 线条类型：实线
                         )
                         ))

# 添加第二条曲线
fig.add_trace(go.Scatter(showlegend=True,
                         x=x, y=y2,
                         mode='lines+markers',
                         name='曲线2',
                         marker=dict(
                             size=12,
                             symbol='square',
                             color='red'
                         ),
                         line=dict(
                             width=3,
                             color='red',
                             dash='dash'  # 线条类型：虚线
                         )
                         ))

# 添加第三条曲线
fig.add_trace(go.Scatter(showlegend=True,
                         x=x, y=y3,
                         mode='lines+markers',
                         name='曲线3',
                         marker=dict(
                             size=8,
                             symbol='diamond',
                             color='green'
                         ),
                         line=dict(
                             width=4,
                             color='green',
                             dash='dot'  # 线条类型：点划线
                         )
                         ))

# 更新布局
fig.update_layout(title='自定义样式后的三条曲线折线图',
                  xaxis_title='X轴',
                  yaxis_title='Y轴')

# 将图表写入HTML文件
fig.write_html("测试2d_line.html", div_id="chart")
