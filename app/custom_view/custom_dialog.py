import sys

from PyQt5.QtCore import QLocale, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QInputMethodEvent
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (QAction, QApplication, QGridLayout, QHBoxLayout,
                             QLineEdit, QListWidgetItem, QVBoxLayout, QWidget)
from qfluentwidgets import (Action, CaptionLabel, CardWidget, CheckBox,
                            ColorDialog, ComboBox, DropDownPushButton,
                            DropDownToolButton, FluentIcon, FluentWindow,
                            Flyout, FlyoutViewBase, HorizontalSeparator,
                            HyperlinkButton, LineEdit, MenuAnimationType,
                            MessageBoxBase, MSFluentWindow, RoundMenu,
                            SearchLineEdit, SubtitleLabel,
                            TransparentPushButton, TransparentToolButton,
                            isDarkTheme, qconfig)
from qfluentwidgets.components.widgets.button import (DropDownButtonBase,
                                                      ToolButton)
from qfluentwidgets.components.widgets.combo_box import ComboItem
from qfluentwidgets.components.widgets.menu import (MenuActionListWidget,
                                                    MenuAnimationManager)


class TraceDialog(MessageBoxBase):
    def __init__(self, parent, info: dict):
        super().__init__(parent=parent)
        self.title_label = SubtitleLabel("Trace 自定义", self)
        self.viewLayout.addWidget(self.title_label)
        self.param_lay = QGridLayout(self)
        self.viewLayout.addLayout(self.param_lay)

        self.name_label = CaptionLabel("数据轨迹名称", self)
        self.param_lay.addWidget(self.name_label, 0, 0, )
        self.name_input = LineEdit(self)
        self.param_lay.addWidget(self.name_input, 0, 1, )
        self.trace_mode_label = CaptionLabel("模式", self)
        self.param_lay.addWidget(self.trace_mode_label, 0, 2, )
        self.trace_mode_cbb = ComboBox(self)
        self.param_lay.addWidget(self.trace_mode_cbb, 0, 3, )
        self.line_width_label = CaptionLabel("线宽", self)
        self.param_lay.addWidget(self.line_width_label, 1, 0, )
        self.line_width_input = LineEdit(self)
        self.param_lay.addWidget(self.line_width_input, 1, 1, )
        self.line_color_label = CaptionLabel("线条颜色", self)
        self.param_lay.addWidget(self.line_color_label, 1, 2, )
        self.line_color_btn = TransparentPushButton(self)
        self.param_lay.addWidget(self.line_color_btn, 1, 3, )
        self.line_dash_label = CaptionLabel("线型", self)
        self.param_lay.addWidget(self.line_dash_label, 2, 0, )
        self.line_dash_cbb = ComboBox(self)
        self.param_lay.addWidget(self.line_dash_cbb, 2, 1, )
        self.marker_size_label = CaptionLabel("标记大小", self)
        self.param_lay.addWidget(self.marker_size_label, 2, 2, )
        self.marker_size_input = LineEdit(self)
        self.param_lay.addWidget(self.marker_size_input, 2, 3, )
        self.marker_color_label = CaptionLabel("标记颜色", self)
        self.param_lay.addWidget(self.marker_color_label, 3, 0, )
        self.marker_color_btn = TransparentPushButton(self)
        self.param_lay.addWidget(self.marker_color_btn, 3, 1, )
        self.marker_symbol_label = CaptionLabel("标记符号", self)
        self.param_lay.addWidget(self.marker_symbol_label, 3, 2, )
        self.marker_symbol_cbb = ComboBox(self)
        self.param_lay.addWidget(self.marker_symbol_cbb, 3, 3, )

        self._config_ui(info)
        self._config_event(info)
        self.accepted.connect(self.get_param)
        self.param: dict = {"curveNumber": info.get("curveNumber", 0), }

    def _config_ui(self, info: dict):
        self.name_input.setText(info.get("trace_name", ""))
        modes=["lines","markers","lines+markers"]
        self.trace_mode_cbb.addItems(modes)
        self.trace_mode_cbb.setCurrentText(info.get("trace_mode", "lines+markers"))
        self.line_width_input.setText(str(info.get("line_width", 5)))
        color = info.get("line_color", "red")
        self.line_color_btn.setText(color)
        new_stylesheet = self.line_color_btn.styleSheet() + f"TransparentPushButton{{background-color:{color};}}"
        self.line_color_btn.setStyleSheet(new_stylesheet)
        self.marker_size_input.setText(str(info.get("marker_size", 5)))

        color = info.get("marker_color", "red")
        self.marker_color_btn.setText(color)
        new_stylesheet = self.marker_color_btn.styleSheet() + f"TransparentPushButton{{background-color:{color};}}"
        self.marker_color_btn.setStyleSheet(new_stylesheet)


        items = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        self.line_dash_cbb.addItems(items)
        self.line_dash_cbb.setCurrentText(info.get("line_dash", "solid"))
        symbol_items = [
            "arrow-bar-down",
            "arrow-bar-left",
            "arrow-bar-right",
            "arrow-bar-up",
            "arrow-down",
            "arrow-left",
            "arrow-right",
            "arrow-up",
            "arrow-wide",
            "arrow",
            "asterisk",
            "bowtie",
            "circle-cross",
            "circle-x",
            "circle",
            "cross-thin",
            "cross",
            "diamond-cross",
            "diamond-tall",
            "diamond-wide",
            "diamond-x",
            "diamond",
            "hash",
            "hexagon",
            "hexagon2",
            "hexagram",
            "hourglass",
            "line-ew",
            "line-ne",
            "line-ns",
            "line-nw",
            "octagon",
            "pentagon",
            "square-cross",
            "square-x",
            "square",
            "star-diamond",
            "star-square",
            "star-triangle-down",
            "star-triangle-up",
            "star",
            "triangle-down",
            "triangle-left",
            "triangle-ne",
            "triangle-nw",
            "triangle-right",
            "triangle-se",
            "triangle-sw",
            "triangle-up",
            "x-thin",
            "x",
            "y-down",
            "y-left",
            "y-right",
            "y-up",
        ]
        self.marker_symbol_cbb.addItems(symbol_items)
        for item in self.marker_symbol_cbb.items:
            item.icon = QIcon(f":/symbol_icon/symbol_icon/{item.text}.svg")
        self.marker_symbol_cbb.setCurrentText(info.get("marker_symbol", "circle"))

    def _config_event(self, info: dict):
        self.line_color_btn.clicked.connect(
            lambda: self.show_color_dialog(self.line_color_btn, info.get("line_color", "red")))
        self.marker_color_btn.clicked.connect(
            lambda: self.show_color_dialog(self.marker_color_btn, info.get("marker_color", "red")))

    def show_color_dialog(self, obj: TransparentPushButton, default_color: str):
        w = TraceColorDialog(default_color=default_color, parent=self)
        result = w.exec_()
        if result:
            color = w.selected_color
            new_stylesheet = obj.styleSheet() + f"TransparentPushButton{{background-color:{color};}}"
            obj.setStyleSheet(new_stylesheet)
            obj.setText(color)

    def get_param(self):
        self.param |= {"trace_name": self.name_input.text(),
                       "trace_mode":self.trace_mode_cbb.currentText(),
                       "line_width": int(self.line_width_input.text()),
                       "line_color": self.line_color_btn.text(),
                       "line_dash": self.line_dash_cbb.currentText(),
                       "marker_size": int(self.marker_size_input.text()),
                       "marker_color": self.marker_color_btn.text(),
                       "marker_symbol": self.marker_symbol_cbb.currentText(),
                       }


class TraceColorDialog(MessageBoxBase):
    closed = pyqtSignal()

    def __init__(self, default_color: str, parent=None, ):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('色彩对话框', self)
        self.viewLayout.addWidget(self.titleLabel)
        self.widget = QWidget(self)
        self.viewLayout.addWidget(self.widget)
        self.widget1 = QWidget(self)
        self.widget_lay = QVBoxLayout(self.widget)
        self.widget_lay.addWidget(self.widget1)

        self.default_color_btn = ToolButton(self.widget1)
        self.default_color_label = SubtitleLabel("默认", self.widget1)
        self.widget1_lay = QHBoxLayout(self.widget1)
        self.widget1_lay.addWidget(self.default_color_btn)
        self.widget1_lay.addWidget(self.default_color_label)
        self.separator1 = HorizontalSeparator(self.widget)
        self.widget_lay.addWidget(self.separator1)
        self.widget2 = QWidget(self)
        self.widget_lay.addWidget(self.widget2)
        self.widget2_lay = QGridLayout(self.widget2)
        colors = [
            # 红色系
            "red",
            "crimson",
            "firebrick",
            "indianred",
            "orangered",
            "tomato",
            "darkred",
            # 橙色系
            "orange",
            "darkorange",
            "coral",
            "lightsalmon",
            "salmon",
            "darksalmon",
            # 黄色系
            "yellow",
            "gold",
            "goldenrod",
            "palegoldenrod",
            "khaki",
            "lemonchiffon",
            "lightgoldenrodyellow",
            # 绿色系
            "green",
            "lime",
            "forestgreen",
            "seagreen",
            "darkgreen",
            "darkolivegreen",
            "olivedrab",
            "mediumseagreen",
            "springgreen",
            "lawngreen",
            "chartreuse",
            "lightgreen",
            "palegreen",
            "darkseagreen",
            "mediumaquamarine",
            "mediumspringgreen",
            "greenyellow",
            # 青色系
            "aqua",
            "cyan",
            "turquoise",
            "paleturquoise",
            "lightcyan",
            "darkturquoise",
            "mediumturquoise",
            # 蓝色系
            "blue",
            "navy",
            "royalblue",
            "cornflowerblue",
            "steelblue",
            "dodgerblue",
            "deepskyblue",
            "skyblue",
            "lightskyblue",
            "powderblue",
            "aliceblue",
            "cadetblue",
            "darkslateblue",
            "slateblue",
            "mediumslateblue",
            "rebeccapurple",
            "midnightblue",
            # 紫色系
            "purple",
            "violet",
            "magenta",
            "fuchsia",
            "deeppink",
            "orchid",
            "plum",
            "lavender",
            "thistle",
            "palevioletred",
            "darkorchid",
            "darkviolet",
            "mediumorchid",
            "mediumpurple",
            "blueviolet",
            "darkmagenta",
            "mediumvioletred",
            # 棕色系
            "brown",
            "saddlebrown",
            "sienna",
            "peru",
            "burlywood",
            "wheat",
            "tan",
            "rosybrown",
            "bisque",
            "blanchedalmond",
            "peachpuff",
            "navajowhite",
            "moccasin",
            "sandybrown",
            "chocolate",
            # 灰色系
            "gray",
            "grey",
            "darkgray",
            "darkgrey",
            "dimgray",
            "dimgrey",
            "silver",
            "lightgray",
            "lightgrey",
            "gainsboro",
            # 白色系
            "white",
            "whitesmoke",
            "snow",
            "ivory",
            "floralwhite",
            "ghostwhite",
            "mintcream",
            "azure",
            "oldlace",
            "honeydew",
            "linen",
            "antiquewhite",
            "beige",
            # 其他（黑色）
            "black",
        ]
        self.widget.setMinimumWidth(500)
        for idx, color in enumerate(colors):
            button = TransparentToolButton(self.widget2)
            button.setIconSize(QSize(35, 35))
            button.setIcon(QIcon(f":/color_icon/color_icon/{color}.svg"))
            row = idx // 15
            column = idx % 15
            button.setFixedSize(38, 38)
            button.setProperty("color", color)
            button.clicked.connect(self.get_color)
            self.widget2_lay.addWidget(button, row, column)
        self.separator2 = HorizontalSeparator(self.widget)
        self.widget_lay.addWidget(self.separator2)
        self.custom_color = TransparentPushButton(self)
        self.widget_lay.addWidget(self.custom_color)
        self.custom_color.setText("自定义颜色")
        self.custom_color.clicked.connect(lambda: self._show_color_dialog(default_color))
        self.widget_lay.addWidget(HorizontalSeparator(self.widget))
        self.widget3 = QWidget(self.widget)
        self.widget_lay.addWidget(self.widget3)
        self.widget3_lay = QHBoxLayout(self.widget3)
        self.selected_color = default_color

    def _show_color_dialog(self, default_color: str):
        w = ColorDialog(default_color, "颜色对话框", parent=self)
        result = w.exec()
        if result:
            self.selected_color = w.color.name()
            self.yesButton.click()

    def get_color(self, _: bool):
        button = self.sender()
        self.selected_color = button.property("color")
        self.yesButton.click()
