import queue
import sys
from pathlib import Path
from typing import List

import plotly.graph_objs as go
from datatable import Frame
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QWidget, QSizePolicy,
)
from qfluentwidgets import (
    CaptionLabel,
    ComboBox,
    Dialog,
    FluentIcon,
    FluentIconBase,
    IconWidget,
    PrimaryPushButton,
    StrongBodyLabel,
    TransparentPushButton,
    TransparentToolButton,
    isDarkTheme, qconfig
)
from qfluentwidgets.common.icon import toQIcon

from app.custom_view.custom_icon import CustomIcon
from app.data.data_manager import DataManager


class SingleTypeWidget(QFrame):
    def __init__(self, icon: FluentIconBase, name: str, size: int, parent=None):
        super().__init__(parent)
        self.setObjectName("singleTypeWidget")

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.icon = IconWidget(icon, self)
        self.icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon.setMinimumSize(2 * size, 2 * size)
        self.lay.addWidget(self.icon, 5)

        self.name = CaptionLabel(name, self)
        self.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.name.setMinimumSize(size, size)
        self.lay.addWidget(self.name, 1, Qt.AlignCenter)
        # self.setFixedSize(size*3, 3*size)
        self.setFixedSize(4 * size, 4 * size)

        qconfig.themeChanged.connect(self.theme_changed)
        self.theme_changed()

    def theme_changed(self):
        if isDarkTheme():
            color = {"border": "#333333", "border_hover": "#25d9e6", "background": "#333333",
                     "background_hover": "#282828"}
        else:
            color = {"border": "#fbfbfb", "border_hover": "#009faa", "background": "#fbfbfb",
                     "background_hover": "#f6f6f6"}
        self.setStyleSheet(f"""
                    #singleTypeWidget {{
                        border: 2px solid {color.get("border")};
                        border-radius: 8px;
                        padding: 10px;
                        background-color: {color.get("background")};  /* 选中时的背景色 */
                        margin: 5px;
                    }}
                    #singleTypeWidget:hover {{
                            border: 2px solid {color.get("border_hover")};
                            border-radius: 8px;
                            padding: 10px;
                            background-color: {color.get("background_hover")}; 
                            margin: 5px;
                        }}
                        """)

    def mousePressEvent(self, event):
        if hasattr(self, "update_theme"):
            self.update_theme(self.name.text())
        else:
            try:
                self.parent().parent().yesButton.click()
                self.parent().parent().selected_type = self.name.text()
            except AttributeError:
                pass


class TraceTypeDialog(Dialog):
    def __init__(self, title: str, parent=None):
        super().__init__(content="", title=title, parent=parent)
        self.vBoxLayout.removeItem(self.textLayout)
        for i in reversed(range(self.textLayout.count())):
            widget_item = self.textLayout.itemAt(i)
            widget = widget_item.widget()
            if widget is not None:
                widget.deleteLater()
            self.textLayout.removeItem(widget_item)
        self.textLayout.setParent(None)
        self.textLayout.deleteLater()
        self.finished.connect(self.deleteLater)
        self.type_widget = QWidget(self)
        self.type_lay = QGridLayout(self.type_widget)
        self.type_lay.setContentsMargins(5, 2, 5, 2)
        self.vBoxLayout.insertWidget(1, self.type_widget)
        self.selected_type = None

        # 2d
        self.label_2d = StrongBodyLabel("2d", self)
        self.type_lay.addWidget(self.label_2d, 0, 0, Qt.AlignLeft | Qt.AlignTop)
        trace_types = ["Scatter", "Line", "Line_Mark", "Area", "Bar", ]
        trace_types_icons = {"Scatter": CustomIcon.MARKER, "Line_Mark": CustomIcon.LINE_MARKER,
                             "Line": CustomIcon.LINE, "Area": CustomIcon.LINE_FILL, "Bar": CustomIcon.BAR, }
        for idx, trace_type in enumerate(trace_types):
            icon = SingleTypeWidget(icon=trace_types_icons.get(trace_type), name=trace_type, parent=self, size=30)
            self.type_lay.addWidget(icon, 1, idx, Qt.AlignCenter)
        # 3d
        self.label_3d = StrongBodyLabel("3d", self)
        self.type_lay.addWidget(self.label_3d, 2, 0, Qt.AlignLeft | Qt.AlignTop)
        trace_types = [
            "3DScatter",
            "3DLine",
        ]
        trace_types_icons = {"3DScatter": CustomIcon.SCATTER_3D,
                             "3DLine": CustomIcon.LINE_3D}
        for idx, trace_type in enumerate(trace_types):
            icon = SingleTypeWidget(icon=trace_types_icons.get(trace_type), name=trace_type, parent=self, size=30)
            self.type_lay.addWidget(icon, 3, idx, Qt.AlignCenter)


class DataSelectWidget(QWidget):
    def __init__(
            self,
            files: List[Path],
            total_data: List[Frame],
            update_queue: queue.Queue,
            widget_id,
            parent=None,
    ):
        super().__init__(parent)
        self.files = files
        self.total_data = total_data
        self.update_queue = update_queue
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_type_label = CaptionLabel("绘图类型", self)
        self.main_layout.addWidget(self.plot_type_label, 0, 0, Qt.AlignCenter)
        self.plot_type_btn = TransparentPushButton("绘图类型", self)
        self.main_layout.addWidget(self.plot_type_btn, 0, 1)

        self.selected_file_label = CaptionLabel("数据文件", self)
        self.main_layout.addWidget(self.selected_file_label, 1, 0, Qt.AlignCenter)
        self.selected_file_cbb = ComboBox(self)
        self.selected_file_cbb.addItems([file.stem for file in self.files])
        self.main_layout.addWidget(self.selected_file_cbb, 1, 1)

        self.selected_x_label = CaptionLabel("X", self)
        self.main_layout.addWidget(self.selected_x_label, 2, 0, Qt.AlignCenter)
        self.selected_x_cbb = ComboBox(self)
        self.main_layout.addWidget(self.selected_x_cbb, 2, 1)

        self.selected_y_label = CaptionLabel("Y", self)
        self.main_layout.addWidget(self.selected_y_label, 3, 0, Qt.AlignCenter)
        self.selected_y_cbb = ComboBox(self)
        self.main_layout.addWidget(self.selected_y_cbb, 3, 1)

        self.update_btn = PrimaryPushButton("确定", self)
        self.main_layout.addWidget(self.update_btn, 4, 1)

        self.config_event()
        self.selected_file_cbb_changed(0)
        self.type_dict = {
            "Scatter": {
                "name": "Scatter",
                "kwargs": {"mode": "markers", "uid": widget_id, "showlegend": True},
            },
            "Line": {"name": "Scatter", "kwargs": {"mode": "lines", "uid": widget_id, "showlegend": True}},
            "Line_Mark": {"name": "Scatter", "kwargs": {"mode": "lines+markers", "uid": widget_id, "showlegend": True}},
            "Bar": {"name": "Bar", "kwargs": {"uid": widget_id, "showlegend": True}},

            "Area": {
                "name": "Scatter",
                "kwargs": {"mode": "lines", "fill": "tozeroy", "uid": widget_id, "showlegend": True},
            },
            "3DScatter": {
                "name": "Scatter3d",
                "kwargs": {"mode": "markers", "uid": widget_id, "showlegend": True},
            },
            "3DLine": {
                "name": "Scatter3d",
                "kwargs": {"mode": "lines", "uid": widget_id, "showlegend": True},
            },
        }

    def config_event(self):
        self.plot_type_btn.clicked.connect(self.show_trace_type_dialog)
        self.selected_file_cbb.currentIndexChanged.connect(
            self.selected_file_cbb_changed
        )
        self.update_btn.clicked.connect(self._get_selected_trace)

    def show_trace_type_dialog(self):
        w = TraceTypeDialog(title="选择轨迹类型", parent=None)
        result = w.exec_()
        if result:
            selected_type = w.selected_type
            self.plot_type_btn.setText(selected_type)

    def selected_file_cbb_changed(self, idx: int):
        data = self.total_data[idx]
        items = data.names
        current_items = self.selected_x_cbb.items
        if len(items) == len(current_items) and all(
                [x == y for x, y in zip(items, current_items)]
        ):
            return
        self.selected_x_cbb.clear()
        self.selected_y_cbb.clear()
        self.selected_x_cbb.addItems(items)
        self.selected_y_cbb.addItems(items)

    def _get_selected_trace(self):
        trace_type_info = self.type_dict.get(self.plot_type_btn.text())
        if trace_type_info is None:
            return
        kwargs = trace_type_info.get("kwargs", {})
        data = self.total_data[self.selected_file_cbb.currentIndex()]
        name = (
                self.selected_file_cbb.currentText()
                + "_"
                + self.selected_y_cbb.currentText()
        )
        plot_data = {
            "x": data[:, self.selected_x_cbb.currentIndex()].to_numpy().T[0],
            "y": data[:, self.selected_y_cbb.currentIndex()].to_numpy().T[0],
            "name": name,
        }
        trace = getattr(go, trace_type_info["name"])(**plot_data, **kwargs)
        update_method = {
            "method": "add_trace",
            "kwargs": {"trace": trace},
            "uid": kwargs.get("uid", ""),
        }
        self.update_queue.put(update_method)

    def remove_trace(self, uid: str):
        update_method = {"method": "remove_trace", "uid": uid}
        self.update_queue.put(update_method)


class CollapsibleWidget(QWidget):
    def __init__(self, widget_id: str, queue, parent=None):
        super().__init__(parent)

        self.main_lay = QVBoxLayout(self)
        self.main_lay.setContentsMargins(0, 0, 0, 0)
        self.control_widget = QWidget(self)
        self.control_widget.setFixedHeight(40)

        self.control_widget.setObjectName("CollapsibleWidget")
        self.control_widget.mousePressEvent = self.mymousePressEvent
        self.main_lay.addWidget(self.control_widget)
        self.control_lay = QHBoxLayout(self.control_widget)
        self.control_lay.setContentsMargins(25, 0, 25, 0)
        self.status_icon = TransparentToolButton(FluentIcon.CHEVRON_RIGHT_MED, self.control_widget)
        self.status_icon.setFixedSize(12, 12)
        self.control_lay.addWidget(self.status_icon, 0, Qt.AlignLeft)
        self.control_lay.addWidget(
            StrongBodyLabel(widget_id, self.control_widget),
            1,
            Qt.AlignCenter | Qt.AlignCenter,
        )
        self.close_btn = TransparentToolButton(FluentIcon.CLOSE, self.control_widget)
        self.close_btn.setFixedSize(12, 12)
        self.control_lay.addWidget(self.close_btn, 1, Qt.AlignRight)

        self.trace_widget = DataSelectWidget(
            DataManager.files, DataManager.total_data, queue, widget_id, self
        )
        self.main_lay.addWidget(self.trace_widget)

        self.is_expand = False
        self.trace_widget.setVisible(False)
        self.close_btn.clicked.connect(lambda: self.close_trace_widget(widget_id))
        qconfig.themeChanged.connect(self.updateStyle)

    def close_trace_widget(self, widget_id: str):
        self.trace_widget.remove_trace(widget_id)
        if hasattr(self.parent(), "remove_trace"):
            self.parent().remove_trace(widget_id)

    def mymousePressEvent(self, event):
        self.is_expand = not self.is_expand
        self.trace_widget.setVisible(self.is_expand)
        icon = (
            FluentIcon.CHEVRON_DOWN_MED
            if self.is_expand
            else FluentIcon.CHEVRON_RIGHT_MED
        )
        self.status_icon.setIcon(icon)
        self.updateStyle()

    def updateStyle(self):
        if isDarkTheme():
            color = {"border_expand": "#29f1ff", "border_collapse": "#282828", "background_expand": "#333333",
                     "background_collapse": "#282828"}
        else:
            color = {"border_expand": "#00a7b3", "border_collapse": "#f6f6f6", "background_expand": "#fbfbfb",
                     "background_collapse": "#f6f6f6"}
        if self.is_expand:
            self.setStyleSheet(f"""
                        #CollapsibleWidget {{
                            border: 2px solid {color.get("border_expand")};
                            border-radius: 8px;
                            padding: 10px;
                            background-color: {color.get("background_expand")};  /* 选中时的背景色 */
                            margin: 5px;
                        }}
                    """)
        else:
            self.setStyleSheet(f"""
                        #CollapsibleWidget {{
                            border: 2px solid {color.get("border_collapse")};
                            border-radius: 8px;
                            padding: 10px;
                            background-color: {color.get("background_collapse")}; 
                            margin: 5px;
                        }}
                    """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CollapsibleWidget(parent=None)
    widget.show()
    sys.exit(app.exec_())
