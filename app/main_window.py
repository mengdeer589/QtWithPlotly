import sys
from typing import Optional

from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition,isDarkTheme,setTheme,toggleTheme

from app.model.web_interface_model import WebInterfaceModel
from app.presenter.web_interface_presenter import WebInterfacePresenter
from app.view.web_interface import WebInterface
import app.resources.resources


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self._ini_window()
        self.setMicaEffectEnabled(False)
        self.web_interface = WebInterface(self)
        self.addSubInterface(self.web_interface, FluentIcon.MARKET, "图表", )

        self.web_interface_model: Optional[WebInterfaceModel] = None
        self.web_interface_pre: Optional[WebInterfacePresenter] = None
        self.web_interface_mvp()

    def _ini_window(self):
        self.setWindowTitle("QtWithPlotly Plotly图表显示与编辑")
        self.navigationInterface.addItem(
            routeKey='toggle_theme',
            icon=FluentIcon.HIGHTLIGHT,
            text="明亮",
            onClick=self.toggle_theme,
            selectable=False,
            position=NavigationItemPosition.BOTTOM
        )
    def toggle_theme(self):
        toggleTheme()

    def web_interface_mvp(self):
        self.web_interface_model = WebInterfaceModel()
        self.web_interface_pre = WebInterfacePresenter(model=self.web_interface_model, view=self.web_interface)


def start():
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec_())
