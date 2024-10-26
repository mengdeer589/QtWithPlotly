from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from orjson import orjson
from qfluentwidgets import FluentIcon
from app.model.web_interface_model import WebInterfaceModel
from app.view.web_interface import WebInterface, PageWithConsole


class WebInterfacePresenter(QObject):
    def __init__(self, model: WebInterfaceModel, view: WebInterface):
        super().__init__()
        self._model = model
        self._view = view
        self.init_view()
        self.sig_config()

    def init_view(self):
        """进行 web 的一些设置"""
        self._view.web_view.setPage(PageWithConsole(self._view.web_view))
        self._view.web_view.page().setWebChannel(self._view.channel)
        self._model.run_dash()
        self._view.web_view.load(QUrl("http://localhost:8000"))

        self._view.generate_plot_btn.clicked.connect(self.generate_plot)
        self._view.communicate.legend_signal.connect(self._model.get_legend_info)
        self._view.connect_btn.clicked.connect(self._model.connect_to_plot)
        self._view.show_setting_btn.clicked.connect(self._view.plot_setting_widget.toggle)
        self._view.modify_navigations.set_queue(self._model.figure_queue)
        #绑定通信件的信号
        self._view.communicate.click_signal.connect(self._model.chart_click_info)

    def sig_config(self):
        self._model.connect_to_plot_sig.connect(self.handle_connect_to_plot)
        self._model.trace_info_sig.connect(self.update_trace_func)

    @pyqtSlot(tuple)
    def handle_connect_to_plot(self, js_code: tuple):
        for js in js_code:
            self._view.web_view.page().runJavaScript(js)
        check_js_code = """check_chart();"""
        self._view.web_view.page().runJavaScript(check_js_code, self.get_connect_result)

    @pyqtSlot(dict)
    def update_trace_func(self, info: dict):
        if self._view.action_buttons.current_clicked() == "自定义":
            user_param = self._view.show_trace_dialog(info)
            if user_param is None:
                return
            # user_param_str = orjson.dumps(user_param).decode("utf-8")
            # user_param_str = user_param_str.replace("\\", "\\\\")
            # # user_param_str=user_param_str.replace("\"", "'")
            # js_code = f"chart_restyle(`{user_param_str}`)"
            # self._view.run_js_code(js_code)
            update_method = {
                "method": "plotly_restyle",
                "kwargs": user_param,
            }
            self._model.figure_queue.put(update_method)

    def get_connect_result(self, result: bool):
        """
        是否成功连接前端后端
        :param result:
        :return:
        """
        if result:
            self._view.connect_btn.setIcon(FluentIcon.ACCEPT)
            self._view.connect_btn.setEnabled(False)
        else:
            self._view.connect_btn.setIcon(FluentIcon.CLOSE)

    def generate_plot(self):
        self._model.change_fig()
