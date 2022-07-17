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


from typing import Optional, TYPE_CHECKING

from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import (QPalette, QIcon, QContextMenuEvent, QPainter,
                         QFontMetrics, QMouseEvent, QPaintEvent,
                         QKeyEvent)
from PyQt5.QtWidgets import QWidget

if TYPE_CHECKING:
    from qflashlight.application import Application


class FlashlightWidget(QWidget):

    def __init__(self, app: 'Application', parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._app = app
        self._mpos = QPoint()

        self.setWindowTitle("QFlashlight")
        self.setAutoFillBackground(True)

        self.setWindowIcon(QIcon.fromTheme("qflashlight"))

    def mouseDoubleClickEvent(self, ev: QMouseEvent) -> None:
        self._app.toggle_fullscreen()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self._mpos = ev.pos()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if ev.buttons() & Qt.LeftButton:
            diff = ev.pos() - self._mpos
            newpos = self.pos() + diff
            self.move(newpos)

    def contextMenuEvent(self, ev: QContextMenuEvent) -> None:
        self._app.show_context_menu(ev.globalPos())

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.key() == Qt.Key_Escape:
            self._app.close()
        elif ev.key() == Qt.Key_Q:
            self._app.close()
        elif ev.key() == Qt.Key_F:
            self._app.toggle_fullscreen()
        elif ev.key() == Qt.Key_M:
            self._app.toggle_cursor_visible()
        elif ev.key() == Qt.Key_E:
            self._app.show_text_dialog()
        elif ev.key() == Qt.Key_C:
            self._app.show_color_dialog()
        elif ev.key() == Qt.Key_T:
            self._app.show_text_color_dialog()
        elif ev.key() == Qt.Key_B:
            self._app.toggle_borderless()

    def set_fullscreen(self, fullscreen: bool) -> None:
        if fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

    def set_borderless(self, borderless: bool) -> None:
        if borderless:
            # Only change setting when in window mode to avoid flickering in fullscreen
            if not (self.windowState() & Qt.WindowFullScreen):
                self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
                self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()

    def paintEvent(self, ev: QPaintEvent) -> None:
        model = self._app.flashlight_model()

        pal = self.palette()
        pal.setColor(QPalette.Background, model.background_color())
        self.setPalette(pal)

        pal = self.palette()
        pal.setColor(QPalette.Foreground, model.foreground_color())
        self.setPalette(pal)

        text = model.text()
        if text is not None:
            painter = QPainter(self)
            painter.setFont(model.font())
            fm = QFontMetrics(painter.font())
            rect = fm.size(Qt.AlignCenter, text)

            src_aspect = rect.width() / rect.height()
            dst_aspect = self.width() / self.height()

            if src_aspect > dst_aspect:
                sx = self.width() / rect.width()
                sy = sx
            else:
                sy = self.height() / rect.height()
                sx = sy

            painter.scale(sx, sy)
            painter.drawText(QRectF(0, 0, self.width() / sx, self.height() / sy),
                             Qt.AlignCenter, text)


# EOF #
