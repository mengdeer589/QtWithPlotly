from pathlib import Path
from queue import Queue

from PyQt5.QtCore import QObject, pyqtSignal

from app.dash_app.generate_fig import CustomPlot
from app.dash_app.plot_resample import SimpleChartApp
from app.thread.thread_fun import DashThread


class WebInterfaceModel(QObject):
    connect_to_plot_sig = pyqtSignal(tuple)
    trace_info_sig = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.files = {
            "qwebchannel": Path.cwd().joinpath(r"runtime\qwebchannel.js"),
            "chart_to_qt": Path.cwd().joinpath(r"runtime\chart_to_qt.js"),
        }
        self.figure_queue = Queue()
        self.chart_app = SimpleChartApp(self.figure_queue)

        self.dash_thread = DashThread(queue=self.figure_queue, chart_app=self.chart_app, host="localhost", port=8000)

    def get_legend_info(self, info):
        print(info)

    def connect_to_plot(self):
        """实现 PyQt5 向前端的连接，根据按钮图标提示连接状态"""
        with open(self.files.get("qwebchannel"), "r", encoding="utf-8") as f:
            channel_code = f.read()
        with open(self.files.get("chart_to_qt"), "r", encoding="utf-8") as f:
            custom_code = f.read()
        result = (channel_code, custom_code)
        self.connect_to_plot_sig.emit(result)

    def chart_click_info(self, info: dict):
        """

        :param info:
        :return:
        """
        self.trace_info_sig.emit(info)

    def run_dash(self):
        self.dash_thread.start()

    def change_fig(self):
        fig = CustomPlot.generate_figure()
        update_method = {"method": "replace", "kwargs": {"figure": fig}}
        self.figure_queue.put(update_method)
