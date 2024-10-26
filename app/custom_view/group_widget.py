import sys

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication
from qfluentwidgets import (
    CardWidget,
    ToggleButton,
    FluentIcon,
    ToolTipFilter,
    ToolTipPosition,
)


class ButtonGroup(CardWidget):
    def __init__(self, is_horizon: bool = True, parent=None):
        super().__init__(parent=parent)
        if is_horizon:
            self.lay = QHBoxLayout(self)
        else:
            self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.buttons: list[ToggleButton] = []

    def add_button(self, text: str, icon: FluentIcon = None, tooltip: str = None):
        """
        外部接口，用于添加按钮
        :param text: 按钮名称
        :param icon: 按钮图标
        :param tooltip: 按钮提示
        :return:
        """
        button = ToggleButton(text=text, icon=icon, parent=self)
        if tooltip:
            button.setToolTip(tooltip)
            button.installEventFilter(ToolTipFilter(button, 0, ToolTipPosition.TOP))
        button.clicked.connect(lambda: self._button_click_func(button))
        self.lay.addWidget(button)
        self.buttons.append(button)

    def clear_buttons(self):
        """
        外部接口，用于清空group
        :return:
        """
        for button in self.buttons:
            self.lay.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()

    def _button_click_func(self, obj: ToggleButton):
        """
        按钮点击函数，保证同时只有一个功能按钮处于点击状态
        :param obj: 触发点击事件的按钮对象
        :return:
        """
        _ = [button.setChecked(False) for button in self.buttons if obj != button]

    def current_clicked(self) -> str:
        """
        获取当前开启的功能按钮
        :return: ToggleButton对象
        """
        for button in self.buttons:
            if button.isChecked():
                return button.text()
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ButtonGroup()
    for i in range(10):
        widget.add_button(text=f"测试{i}")
    widget.show()
    sys.exit(app.exec_())
