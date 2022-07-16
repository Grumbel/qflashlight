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


from typing import Callable, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QColorDialog


def show_color_dialog(parent: QWidget,
                      getter: Callable[[], QColor],
                      setter: Callable[[QColor], None]) -> None:
    tmpcolor: Optional[QColor] = getter()

    def set_color(color: QColor) -> None:
        nonlocal tmpcolor
        setter(color)
        tmpcolor = None

    def restore_color() -> None:
        if tmpcolor is not None:
            setter(tmpcolor)

    color_dlg = QColorDialog(parent)
    color_dlg.setWindowModality(Qt.WindowModal)
    color_dlg.setCurrentColor(getter())

    color_dlg.currentColorChanged.connect(setter)
    color_dlg.colorSelected.connect(set_color)
    color_dlg.rejected.connect(restore_color)

    color_dlg.show()


# EOF #
