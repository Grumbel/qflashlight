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

from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QMenu

from qflashlight.color_dialog import show_color_dialog
from qflashlight.flashlight_widget import FlashlightWidget
from qflashlight.text_generator import TextGenerator


class Application:

    def __init__(self) -> None:
        self._fullscreen: bool = False
        self._borderless: bool = False
        self._cursor_visible: bool = True
        self._flashlight_widget = FlashlightWidget(self)
        self._text_generator: Optional[TextGenerator] = None

    def show(self) -> None:
        self._flashlight_widget.show()

    def close(self) -> None:
        self._flashlight_widget.close()

    def set_fullscreen(self, fullscreen: bool) -> None:
        self._fullscreen = fullscreen
        self._apply_window_mode()

    def fullscreen(self) -> bool:
        return self._fullscreen

    def toggle_fullscreen(self) -> None:
        self._fullscreen = not self._fullscreen
        self._apply_window_mode()

    def set_borderless(self, borderless: bool) -> None:
        self._borderless = borderless
        self._apply_window_mode()

    def borderless(self) -> bool:
        return self._borderless

    def toggle_borderless(self) -> None:
        self._borderless = not self._borderless
        self._apply_window_mode()

    def _apply_window_mode(self) -> None:
        self._flashlight_widget.set_fullscreen(self._fullscreen)
        self._flashlight_widget.set_borderless(self._borderless)

    def set_window_geometry(self, geometry: QRect) -> None:
        self._flashlight_widget.setGeometry(geometry)

    def set_cursor_visible(self, visible: bool) -> None:
        self._cursor_visible = visible

        if self._cursor_visible:
            self._flashlight_widget.setCursor(Qt.BlankCursor)
        else:
            self._flashlight_widget.unsetCursor()

    def cursor_visible(self) -> bool:
        return self._cursor_visible

    def toggle_cursor_visible(self) -> None:
        self.set_cursor_visible(not self._cursor_visible)

    def set_foreground_color(self, fgcolor: QColor) -> None:
        self._flashlight_widget.set_foreground_color(fgcolor)

    def set_background_color(self, bgcolor: QColor) -> None:
        self._flashlight_widget.set_background_color(bgcolor)

    def set_font(self, font: QFont) -> None:
        self._flashlight_widget.set_font(font)

    def set_text(self, text: str) -> None:
        self._text_generator = None
        self._flashlight_widget.set_text(text)

    def show_color_dialog(self) -> None:
        show_color_dialog(self._flashlight_widget,
                          self._flashlight_widget.background_color,
                          self._flashlight_widget.set_background_color)

    def show_text_color_dialog(self) -> None:
        show_color_dialog(self._flashlight_widget,
                          self._flashlight_widget.foreground_color,
                          self._flashlight_widget.set_foreground_color)

    def set_command(self, command: str, refresh_interval_sec: float) -> None:
        def update_text(text: str) -> None:
            self._flashlight_widget.set_text(text)
            self._flashlight_widget.repaint()

        self._text_generator = TextGenerator(command, refresh_interval_sec,
                                             update_text)
        self._text_generator.start()

    def show_context_menu(self, pos: QPoint) -> None:
        menu = QMenu()

        if self._fullscreen:
            menu.addAction("Exit full screen", lambda: self.set_fullscreen(False))
        else:
            menu.addAction("Enter full screen", lambda: self.set_fullscreen(True))

        if self._cursor_visible:
            menu.addAction("Hide mouse cursor", lambda: self.set_cursor_visible(False))
        else:
            menu.addAction("Show mouse cursor", lambda: self.set_cursor_visible(True))

        if self._borderless:
            menu.addAction("Show window border", lambda: self.set_borderless(False))
        else:
            menu.addAction("Hide window border", lambda: self.set_borderless(True))

        menu.addAction("Change Color...", lambda: self.show_color_dialog())
        menu.addAction("Change Text Color...", lambda: self.show_text_color_dialog())

        menu.addSeparator()

        menu.addAction("Exit", self.close)

        menu.exec(pos)


# EOF #
