import json
from pathlib import Path

from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import CardWidget, TransparentPushButton, FluentIcon

from app.custom_view.custom_dialog import TraceDialog
from app.custom_view.group_widget import ButtonGroup


class PageWithConsole(QWebEnginePage):
    def javaScriptConsoleMessage(
            self,
            level: QWebEnginePage.JavaScriptConsoleMessageLevel,
            message: str,
            lineNumber: int,
            sourceID: str,
    ):
        print("console 输出:", message)
        return super(PageWithConsole, self).javaScriptConsoleMessage(
            level, message, lineNumber, sourceID
        )


class Communicate(QObject):
    click_signal = pyqtSignal(dict)
    hover_signal = pyqtSignal(dict)
    legend_signal = pyqtSignal(dict)
    selected_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(Communicate, self).__init__(parent)

    @pyqtSlot(str, result=str)
    def connect_result(self, me):
        print("已连接", me)
        return "已连接上pyqt5"

    @pyqtSlot(str, result=str)  # 更改类型为str
    def hover_info(self, json_str):  # 更改参数名为points_str
        info = json.loads(json_str)
        self.hover_signal.emit(info)
        return ""

    @pyqtSlot(str, result=str)  # 更改类型为str
    def legend_info(self, json_str):  # 更改参数名为points_str
        info = json.loads(json_str)
        self.legend_signal.emit(info)
        return ""

    @pyqtSlot(str, result=str)  # 更改类型为str
    def click_info(self, json_str):  # 更改参数名为points_str
        info = json.loads(json_str)
        self.click_signal.emit(info)
        return ""

    @pyqtSlot(str, result=str)  # 更改类型为str
    def selected_info(self, json_str):
        info = json.loads(json_str)
        self.selected_signal.emit(info)
        return ""


class WebInterface(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("WebInterface")
        self.web_view = QWebEngineView(self)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.control_widget = QWidget(self)
        self.control_lay = QHBoxLayout(self.control_widget)
        self.control_lay.setContentsMargins(0, 0, 0, 0)

        self.connect_btn = TransparentPushButton(self)
        self.connect_btn.setText("连接")

        self.control_lay.addWidget(self.connect_btn)
        self.lay.addWidget(self.control_widget, 1)
        self.lay.addWidget(self.web_view, 25)
        self.channel = QWebChannel()
        self.communicate = Communicate()

        self.channel.registerObject("communicate", self.communicate)

        self.action_buttons = ButtonGroup(self)
        self.control_lay.addWidget(self.action_buttons)
        self.action_buttons.add_button("自定义", FluentIcon.SETTING, "开启后，可通过点击折线来修改折线属性")

    def show_trace_dialog(self, info: dict):
        w = TraceDialog(self, info=info)
        result = w.exec_()
        if result:
            return w.param
        return None

    def run_js_code(self, js_code: str):
        self.web_view.page().runJavaScript(js_code)