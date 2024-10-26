from typing import Union, Optional, Dict
from uuid import uuid4

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QStackedWidget, QHBoxLayout, QWidget, QVBoxLayout, QSpacerItem, \
    QSizePolicy, QFrame
from qfluentwidgets import ListWidget, FluentIcon, PrimaryPushButton, CardWidget, ScrollArea
from qfluentwidgets.common.icon import toQIcon
import plotly.graph_objs as go

from app.custom_view.data_select_widget import CollapsibleWidget, SingleTypeWidget
import app.resources.resources


class TraceWidget(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.add_trace_btn = PrimaryPushButton(FluentIcon.ADD, title, self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.add_trace_btn, alignment=Qt.AlignRight | Qt.AlignTop)
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.add_trace_btn.clicked.connect(self.add_trace)
        self.trace_widgets_dict: Dict[str, CollapsibleWidget] = {}

    def add_trace(self):
        widget_id = str(uuid4())
        trace_widget = CollapsibleWidget(widget_id, self.update_queue, self)
        self.trace_widgets_dict |= {widget_id: trace_widget}

        self.layout.insertWidget(self.layout.count() - 1, trace_widget, alignment=Qt.AlignTop)

    def remove_trace(self, widget_id: str):
        widget = self.trace_widgets_dict.get(widget_id)
        self.layout.removeWidget(widget)
        widget.deleteLater()


class ThemeWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_widget = CardWidget(self)
        self.scroll_lay = QVBoxLayout(self.scroll_widget)
        self.setWidget(self.scroll_widget)
        self.update_queue = None
        self.setStyleSheet("""background-color: transparent;""")
        themes = [
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
        ]
        for theme in themes:
            widget = SingleTypeWidget(icon=QIcon(f":/chart_theme/chart_theme/{theme}.svg"), name=theme, size=100,
                                      parent=self.scroll_widget)
            widget.update_theme=self.update_theme
            self.scroll_lay.addWidget(widget)

    def update_theme(self, theme: str):
        update_method = {
            "method": "update_layout",
            "kwargs": {"template": theme},
        }
        self.update_queue.put(update_method)


class SidebarNavigation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建 QListWidget 用于侧边栏
        self.list_widget = ListWidget()
        self.list_widget.setMaximumWidth(120)
        self.buttons: list[QListWidgetItem] = []

        # 创建 QStackedWidget 用于显示不同页面的内容
        self.stacked_widget = QStackedWidget()

        # 连接 QListWidget 的当前行改变信号到槽函数
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # 设置主窗口的布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.stacked_widget)

    def add_page(self, name: str, page: QWidget, icon: Union[QIcon, FluentIcon, None] = None):
        """添加一个新的页面到 QStackedWidget"""
        if icon is None:
            item = QListWidgetItem(name, self.list_widget)
        else:
            icon = toQIcon(icon)
            item = QListWidgetItem(icon, name, self.list_widget)
        self.buttons.append(item)
        self.stacked_widget.addWidget(page)


class ChartView(SidebarNavigation):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.fig: Optional[go.Figure] = None
        self.update_queue = None
        self.trace_widget = TraceWidget("添加", self)
        self.theme_widget = ThemeWidget(parent=self)
        self.add_page(name="添加轨迹", page=self.trace_widget, )
        self.add_page(name="绘图主题", page=self.theme_widget, )

    def set_queue(self, queue):
        self.trace_widget.update_queue = queue
        self.theme_widget.update_queue = queue
