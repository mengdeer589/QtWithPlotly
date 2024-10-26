import sys
from typing import Union

from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, Qt, QEasingCurve
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtWidgets import (
    QLabel,
    QButtonGroup,
    QApplication,
    QScrollArea,
    QFrame,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)
from qfluentwidgets import (
    ExpandSettingCard,
    HeaderCardWidget,
    OptionsSettingCard,
    FluentIconBase,
    RadioButton,
    SimpleCardWidget,
    FluentStyleSheet,
    FluentIcon,
    SettingCard,
    isDarkTheme,
)
from qfluentwidgets.components.settings.expand_setting_card import (
    HeaderSettingCard,
    SpaceWidget,
    ExpandBorderWidget,
)
from qfluentwidgets.components.settings.setting_card import SettingIconWidget


class MyExpandSettingCard(QScrollArea):
    def __init__(
        self,
        icon: Union[str, QIcon, FluentIcon],
        title: str,
        content: str = None,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.isExpand = False

        self.scrollWidget = QFrame(self)
        self.view = QFrame(self.scrollWidget)
        self.card = HeaderSettingCard(icon, title, content, self)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.viewLayout = QVBoxLayout(self.view)
        self.spaceWidget = SpaceWidget(self.scrollWidget)
        self.borderWidget = ExpandBorderWidget(self)

        # expand animation
        self.expandAni = QPropertyAnimation(self.verticalScrollBar(), b"value", self)

        self.__initWidget()
        self.viewLayout.setSpacing(19)
        self.viewLayout.setContentsMargins(48, 18, 0, 18)
        self._adjustViewSize()

    def __initWidget(self):
        """initialize widgets"""
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setFixedHeight(self.card.height())
        self.setViewportMargins(0, self.card.height(), 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # initialize layout
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.addWidget(self.view)
        self.scrollLayout.addWidget(self.spaceWidget)

        # initialize expand animation
        self.expandAni.setEasingCurve(QEasingCurve.OutQuad)
        self.expandAni.setDuration(200)

        # initialize style sheet
        self.view.setObjectName("view")
        self.scrollWidget.setObjectName("scrollWidget")
        self.setProperty("isExpand", False)

        self.card.installEventFilter(self)
        self.expandAni.valueChanged.connect(self._onExpandValueChanged)
        self.card.expandButton.clicked.connect(self.toggleExpand)

    def addWidget(self, widget: QWidget):
        """add widget to tail"""
        self.card.addWidget(widget)

    def wheelEvent(self, e):
        pass

    def setExpand(self, isExpand: bool):
        """set the expand status of card"""
        if self.isExpand == isExpand:
            return

        # update style sheet
        self.isExpand = isExpand
        self.setProperty("isExpand", isExpand)
        self.setStyle(QApplication.style())

        # start expand animation
        if isExpand:
            h = self.viewLayout.sizeHint().height()
            self.verticalScrollBar().setValue(h)
            self.expandAni.setStartValue(h)
            self.expandAni.setEndValue(0)
        else:
            self.expandAni.setStartValue(0)
            self.expandAni.setEndValue(self.verticalScrollBar().maximum())

        self.expandAni.start()
        self.card.expandButton.setExpand(isExpand)

    def toggleExpand(self):
        """toggle expand status"""
        self.setExpand(not self.isExpand)

    def resizeEvent(self, e):
        self.card.resize(self.width(), self.card.height())
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())

    def _onExpandValueChanged(self):
        vh = self.viewLayout.sizeHint().height()
        h = self.viewportMargins().top()
        self.setFixedHeight(max(h + vh - self.verticalScrollBar().value(), h))

    def _adjustViewSize(self):
        """adjust view size"""
        h = self.viewLayout.sizeHint().height()
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height() + h)

    def setValue(self, value):
        """set the value of config item"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyExpandSettingCard(FluentIcon.SETTING, "测试")
    w.show()
    sys.exit(app.exec_())
