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

import subprocess

from PyQt5.QtCore import QTimer


class TextGenerator:

    def __init__(self,
                 command: str,
                 refresh_interval_sec: Optional[float],
                 text_callback: Callable[[str], None]):
        self._command = command
        self._refresh_interval_sec = refresh_interval_sec
        self._text_callback = text_callback
        self._timer = QTimer()

    def start(self) -> None:
        self._run_once()

        if self._refresh_interval_sec is not None:
            self._timer.timeout.connect(self._run_once)
            self._timer.start(int(self._refresh_interval_sec * 1000))

    def stop(self) -> None:
        self._timer.stop()

    def _run_once(self) -> None:
        text = subprocess.getoutput(self._command)
        self._text_callback(text)


# EOF #
