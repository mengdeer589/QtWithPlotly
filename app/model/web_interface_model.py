from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal


class WebInterfaceModel(QObject):
    connect_to_plot_sig = pyqtSignal(tuple)
    trace_info_sig = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.files = {
            "qwebchannel": Path.cwd().joinpath(r"runtime\qwebchannel.js"),
            "chart_to_qt": Path.cwd().joinpath(r"runtime\chart_to_qt.js"),
        }

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
