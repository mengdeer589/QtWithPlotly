import logging
import threading
import time
import dash
from dash import dcc, html, Input, Output, no_update
import plotly.graph_objs as go
import queue
from werkzeug.serving import make_server
from plotly_resampler import FigureResampler

from app.dash_app.generate_fig import CustomPlot


class SimpleChartApp:
    def __init__(self, figure_queue):
        self.app = dash.Dash("local_app")
        self.setup_layout()
        self.setup_callbacks()
        self.fig: FigureResampler = FigureResampler(go.Figure(), resampled_trace_prefix_suffix=(
            '<b style="color:sandybrown">[采样]</b> ',
            "",
        ), )
        self.fig.register_update_graph_callback(app=self.app, graph_id="graph-id")
        self.server = None
        self.stop_event = threading.Event()
        self.figure_queue = figure_queue

    def setup_layout(self):
        # 定义布局
        self.app.layout = html.Div([
            dcc.Graph(id='graph-id', style={
                "height": "95vh",  # 占据 95% 的视口高度
                "width": "95vw",  # 占据 95% 的视口宽度
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center"
            }, config=CustomPlot.config),  # 图表元素
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # 每秒检查一次
                n_intervals=0
            )
        ], style={
            "height": "95vh",  # 占据 95% 的视口高度
            "width": "95vw",  # 占据 95% 的视口宽度
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center"
        })

    def setup_callbacks(self):
        @self.app.callback(
            Output('graph-id', 'figure'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_chart(n):
            try:
                # 尝试从队列中获取新的 Figure 对象
                update_method: dict = self.figure_queue.get_nowait()
                method = update_method.get("method")
                kwargs = update_method.get("kwargs", {})
                uid = update_method.get("uid", "")
                if method == "add_trace":
                    self.check_exist_trace(self.fig, uid)
                elif method == "remove_trace":
                    self.check_exist_trace(self.fig, uid)
                    return self.fig
                elif method == "plotly_restyle":
                    curveNumber = kwargs.pop("curveNumber")
                    new_style = {
                        'name': kwargs.get("trace_name"),
                        'mode': kwargs.get("trace_mode"),
                        'line.width': kwargs.get("line_width"),
                        'line.color': kwargs.get("line_color"),
                        'line.dash': kwargs.get("line_dash"),
                        'marker.size': kwargs.get("marker_size"),
                        'marker.color': kwargs.get("marker_color"),
                        'marker.symbol': kwargs.get("marker_symbol"),
                    }
                    self.fig.plotly_restyle(new_style,[curveNumber])
                    return self.fig
                getattr(self.fig, method)(*update_method.get("args", ()),
                                          **kwargs)

                return self.fig
            except queue.Empty:
                # 如果队列为空，则不更新图表
                return no_update
            except AttributeError:
                return no_update

    def run(self, host, port):
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        self.server = make_server(host, port, self.app.server, threaded=True)

        # 在单独的线程中运行服务器
        server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        server_thread.start()

        # 定期检查 stop_event 是否被设置
        while not self.stop_event.is_set():
            time.sleep(1)

        # 设置 stop_event 后关闭服务器
        self.server.shutdown()
        server_thread.join()

    def check_exist_trace(self, fig: FigureResampler, uid: str):
        current_data = fig.data
        for i, existing_trace in enumerate(fig.data):
            if existing_trace.uid == uid:
                new_data_list = [trace for j, trace in enumerate(current_data) if j != i]
                new_data_tuple = tuple(new_data_list)
                fig.data = new_data_tuple
                return True
        return False
