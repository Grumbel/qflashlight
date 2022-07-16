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


from enum import Enum

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QFont

from qflashlight.flashlight_widget import FlashlightWidget
from qflashlight.color_dialog import show_color_dialog


class WindowMode(Enum):

    WINDOW = 1
    BORDERLESS = 2
    FULLSCREEN = 3


class Application:

    def __init__(self) -> None:
        self._flashlight_widget = FlashlightWidget(self)
        self._window_mode = WindowMode.WINDOW

    def show(self) -> None:
        self._flashlight_widget.show()

    def set_window_mode(self, mode: WindowMode) -> None:
        if self._window_mode == mode:
            return

        self._window_mode = mode

        if mode == WindowMode.WINDOW:
            self._flashlight_widget.set_fullscreen(False)
            self._flashlight_widget.set_borderless(False)
        elif mode == WindowMode.BORDERLESS:
            self._flashlight_widget.set_fullscreen(False)
            self._flashlight_widget.set_borderless(True)
        elif mode == WindowMode.FULLSCREEN:
            self._flashlight_widget.set_fullscreen(True)

    def set_window_geometry(self, geometry: QRect) -> None:
        self._flashlight_widget.setGeometry(geometry)

    def set_hide_cursor(self, hide: bool) -> None:
        self._flashlight_widget.hide_cursor()

    def set_foreground_color(self, fgcolor: QColor) -> None:
        self._flashlight_widget.set_foreground_color(fgcolor)

    def set_background_color(self, bgcolor: QColor) -> None:
        self._flashlight_widget.set_background_color(bgcolor)

    def set_font(self, font: QFont) -> None:
        self._flashlight_widget.set_font(font)

    def set_text(self, text: str) -> None:
        self._flashlight_widget.set_text(text)

    def set_command(self, command: str, refresh_interval_sec: float) -> None:
        self._flashlight_widget.set_command(command)
        self._flashlight_widget.set_refresh_interval(refresh_interval_sec)

    def show_color_dialog(self) -> None:
        show_color_dialog(self._flashlight_widget,
                          self._flashlight_widget.background_color,
                          self._flashlight_widget.set_background_color)

    def show_text_color_dialog(self) -> None:
        show_color_dialog(self._flashlight_widget,
                          self._flashlight_widget.foreground_color,
                          self._flashlight_widget.set_foreground_color)


# EOF #
