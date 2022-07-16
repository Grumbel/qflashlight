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


import subprocess

from typing import Optional, TYPE_CHECKING

from PyQt5.QtCore import Qt, QPoint, QRectF, QTimerEvent
from PyQt5.QtGui import (QColor, QPalette, QIcon, QContextMenuEvent,
                         QPainter, QFont, QFontMetrics, QMouseEvent,
                         QPaintEvent, QKeyEvent)
from PyQt5.QtWidgets import QWidget, QMenu

if TYPE_CHECKING:
    from qflashlight.application import Application


class FlashlightWidget(QWidget):

    def __init__(self, app: 'Application', parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._app = app

        self._bg_color: QColor = QColor(Qt.black)
        self._fg_color: QColor = QColor(Qt.white)
        self._font: QFont = QFont()

        self._text: Optional[str] = None
        self._command: Optional[str] = None
        self._refresh_interval: Optional[float] = None

        self._mpos = QPoint()

        self._cursor_visible = True
        self._borderless = False
        self._fullscreen = False

        self.setWindowTitle("QFlashlight")
        self.setAutoFillBackground(True)

        self.setWindowIcon(QIcon.fromTheme("qflashlight"))

    def mouseDoubleClickEvent(self, ev: QMouseEvent) -> None:
        self.set_fullscreen(not self._fullscreen)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self._mpos = ev.pos()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if ev.buttons() & Qt.LeftButton:
            diff = ev.pos() - self._mpos
            newpos = self.pos() + diff
            self.move(newpos)

    def contextMenuEvent(self, ev: QContextMenuEvent) -> None:
        menu = QMenu()

        if self._fullscreen:
            menu.addAction("Exit full screen", lambda: self.set_fullscreen(False))
        else:
            menu.addAction("Enter full screen", lambda: self.set_fullscreen(True))

        if self._cursor_visible:
            menu.addAction("Hide mouse cursor", lambda: self.hide_cursor())
        else:
            menu.addAction("Show mouse cursor", lambda: self.show_cursor())

        if self._borderless:
            menu.addAction("Show window border", lambda: self.set_borderless(False))
        else:
            menu.addAction("Hide window border", lambda: self.set_borderless(True))

        menu.addAction("Change Color...", lambda: self._app.show_color_dialog())
        menu.addAction("Change Text Color...", lambda: self._app.show_text_color_dialog())

        menu.addSeparator()

        def on_exit() -> None:
            self.close()
        menu.addAction("Exit", on_exit)

        menu.exec(ev.globalPos())

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        if ev.key() == Qt.Key_Escape:
            self.close()
        elif ev.key() == Qt.Key_Q:
            self.close()
        elif ev.key() == Qt.Key_F:
            self.set_fullscreen(not self._fullscreen)
        elif ev.key() == Qt.Key_M:
            if self._cursor_visible:
                self.hide_cursor()
            else:
                self.show_cursor()
        elif ev.key() == Qt.Key_C:
            self._app.show_color_dialog()
        elif ev.key() == Qt.Key_T:
            self._app.show_text_color_dialog()
        elif ev.key() == Qt.Key_B:
            self.set_borderless(not self._borderless)

    def set_background_color(self, bg_color: QColor) -> None:
        self._bg_color = bg_color

        pal = self.palette()
        pal.setColor(QPalette.Background, self._bg_color)
        self.setPalette(pal)

    def background_color(self) -> QColor:
        return self._bg_color

    def set_foreground_color(self, fg_color: QColor) -> None:
        self._fg_color = fg_color

        pal = self.palette()
        pal.setColor(QPalette.Foreground, self._fg_color)
        self.setPalette(pal)

    def foreground_color(self) -> QColor:
        return self._fg_color

    def set_font(self, font: QFont) -> None:
        self._font = font

    def set_text(self, text: str) -> None:
        self._text = text

    def set_command(self, command: str) -> None:
        self._command = command
        self._update_text_from_command()

    def set_refresh_interval(self, interval: Optional[float]) -> None:
        self._refresh_interval = interval

        if self._refresh_interval is not None:
            self.startTimer(int(self._refresh_interval * 1000))

    def timerEvent(self, ev: QTimerEvent) -> None:
        self._update_text_from_command()

    def _update_text_from_command(self) -> None:
        if self._command is None:
            return

        self._text = subprocess.getoutput(self._command)
        self.update()

    def set_fullscreen(self, fullscreen: bool) -> None:
        self._fullscreen = fullscreen

        if self._fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

    def set_borderless(self, borderless: bool) -> None:
        self._borderless = borderless

        if self._borderless:
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()

    def hide_cursor(self) -> None:
        self.setCursor(Qt.BlankCursor)
        self._cursor_visible = False

    def show_cursor(self) -> None:
        self.unsetCursor()
        self._cursor_visible = True

    def paintEvent(self, ev: QPaintEvent) -> None:
        if self._text is not None:
            text = self._text
            painter = QPainter(self)
            painter.setFont(self._font)
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
