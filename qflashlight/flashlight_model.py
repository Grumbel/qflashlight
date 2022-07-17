# qflashlight - Simple Qt-based fullscreen flashlight
# Copyright (C) 2017 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Optional

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QColor, QFont


class FlashlightModel(QObject):

    sig_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self._bg_color: QColor = QColor(Qt.black)
        self._fg_color: QColor = QColor(Qt.white)
        self._font: QFont = QFont()
        self._text: Optional[str] = None

    def foreground_color(self) -> QColor:
        return self._fg_color

    def background_color(self) -> QColor:
        return self._bg_color

    def font(self) -> QFont:
        return self._font

    def text(self) -> Optional[str]:
        return self._text

    def set_foreground_color(self, color: QColor) -> None:
        self._fg_color = color
        self.sig_changed.emit()

    def set_background_color(self, color: QColor) -> None:
        self._bg_color = color
        self.sig_changed.emit()

    def set_font(self, font: QFont) -> None:
        self._font = font
        self.sig_changed.emit()

    def set_text(self, text: str) -> None:
        self._text = text
        self.sig_changed.emit()

# EOF #
