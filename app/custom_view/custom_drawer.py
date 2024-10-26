from PyQt5.QtCore import Qt, QEvent, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import (
    CardWidget,
    SubtitleLabel,
    TransparentToolButton,
    FluentIcon,
    qconfig,
    isDarkTheme,
)


class Drawer(CardWidget):
    def __init__(
        self, parent, title: str = "抽屉", direction="left", width_ratio: float = 0.3
    ):
        super().__init__(parent)
        self.direction = direction
        self.width_ratio = width_ratio
        self.init_geometry()

        # 抽屉内容
        self.lay = QVBoxLayout(self)
        # self.lay.setContentsMargins(0, 0, 0, 0)
        self.title_lay = QHBoxLayout()
        self.title_lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addLayout(self.title_lay)
        label = SubtitleLabel(title, self)
        close_btn = TransparentToolButton(FluentIcon.CLOSE, self)
        close_btn.clicked.connect(self.toggle)
        self.title_lay.addWidget(label, 0, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.title_lay.addWidget(close_btn, 0, alignment=Qt.AlignRight | Qt.AlignTop)
        self.raise_()
        # 初始化时隐藏抽屉
        self.setVisible(False)
        self.parent().installEventFilter(self)
        qconfig.themeChanged.connect(self.theme_changed)
        self.theme_changed()

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Resize and obj is self.parent():
            self.on_resize(event)
        elif event.type() == QEvent.MouseButtonRelease:
            # 如果抽屉可见且点击不在抽屉内部
            if self.isVisible():
                # 检查点击是否在抽屉内部
                local_pos = self.mapFromGlobal(event.globalPos())
                if not self.rect().contains(local_pos):
                    self.toggle()
        return super().eventFilter(obj, event)

    def theme_changed(self):
        if isDarkTheme():
            self.setStyleSheet("""
            .Drawer{background-color:#212121;}
            """)
        else:
            self.setStyleSheet("""
                        .Drawer{background-color:#f3f3f3;}
                        """)

    def init_geometry(self):
        directions = {
            "left": (
                -int(self.parent().width() * self.width_ratio),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "right": (
                self.parent().width(),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "top": (
                0,
                -int(self.parent().height() * self.width_ratio),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
            "bottom": (
                0,
                self.parent().height(),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
        }
        self.setGeometry(*directions[self.direction])

    def update_geometry(self):
        positions = {
            "left": (
                0,
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "right": (
                self.parent().width() - int(self.parent().width() * self.width_ratio),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "top": (
                0,
                0,
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
            "bottom": (
                0,
                self.parent().height() - int(self.parent().height() * self.width_ratio),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
        }
        self.setGeometry(*positions[self.direction])

    def toggle(self):
        start_values = {
            "left": QRect(
                -int(self.parent().width() * self.width_ratio),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "right": QRect(
                self.parent().width(),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "top": QRect(
                0,
                -int(self.parent().height() * self.width_ratio),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
            "bottom": QRect(
                0,
                self.parent().height(),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
        }

        end_values = {
            "left": QRect(
                0,
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "right": QRect(
                self.parent().width() - int(self.parent().width() * self.width_ratio),
                0,
                int(self.parent().width() * self.width_ratio),
                self.parent().height(),
            ),
            "top": QRect(
                0,
                0,
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
            "bottom": QRect(
                0,
                self.parent().height() - int(self.parent().height() * self.width_ratio),
                self.parent().width(),
                int(self.parent().height() * self.width_ratio),
            ),
        }

        if self.isVisible():
            # 如果抽屉已经可见，则将其隐藏
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(300)  # 动画持续时间
            self.animation.setEasingCurve(QEasingCurve.OutQuad)  # 收回时由快变慢
            self.animation.setStartValue(end_values[self.direction])
            self.animation.setEndValue(start_values[self.direction])
            self.animation.start()
            self.animation.finished.connect(lambda: self.setVisible(False))
        else:
            # 如果抽屉不可见，则显示并启动动画
            self.setVisible(True)
            self.update_geometry()
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(300)  # 动画持续时间
            self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # 弹出时平滑加速
            self.animation.setStartValue(start_values[self.direction])
            self.animation.setEndValue(end_values[self.direction])
            self.animation.start()

    def on_resize(self, event):
        # 当窗口大小变化时，更新抽屉的几何属性
        self.update_geometry()
        event.accept()
