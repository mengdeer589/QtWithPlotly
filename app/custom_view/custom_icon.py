from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor
import app.resources.custom_icon


class CustomIcon(FluentIconBase, Enum):
    HIGH_FILTER = "HIGH_FILTER"
    ADD = "ADD"
    BAR_3D = "BAR_3D"
    LINE_3D = "LINE_3D"
    COMPUTER = "COMPUTER"
    ANALYSIS = "ANALYSIS"
    LOCATION = "LOCATION"
    NOISE_REMOVAL = "NOISE_REMOVAL"
    WORD = "WORD"
    LINE = "LINE"
    SCATTER_3D = "SCATTER_3D"
    DATA_ANALYST = "DATA_ANALYST"
    MARKER = "MARKER"
    SOCKET = "SOCKET"
    COL_APPEND = "COL_APPEND"
    SNAP_RECT = "SNAP_RECT"
    TABLE = "TABLE"
    SHOCK = "SHOCK"
    REPLACE_NULL = "REPLACE_NULL"
    BAR = "BAR"
    FUNCTION = "FUNCTION"
    LINE_FILL = "LINE_FILL"
    LOW_FILTER = "LOW_FILTER"
    DATA_MANAGE = "DATA_MANAGE"
    LOG = "LOG"
    SOCKET_1 = "SOCKET_1"
    SOCKET_FIRE = "SOCKET_FIRE"
    OVERLOAD = "OVERLOAD"
    EXIT_FULL_SCREEN = "EXIT_FULL_SCREEN"
    REPLACE = "REPLACE"
    RENAME = "RENAME"
    PEAK = "PEAK"
    HISTORY = "HISTORY"
    MARK = "MARK"
    MULTI_FILES = "MULTI_FILES"
    FULL_SCREEN = "FULL_SCREEN"
    VIBRATE = "VIBRATE"
    HELP = "HELP"
    HTML = "HTML"
    LINE_MARKER = "LINE_MARKER"
    FILTER = "FILTER"


    def path(self, theme=Theme.AUTO):
        return f":/icon/theme_icon/{self.value}_{getIconColor(theme)}.svg"
