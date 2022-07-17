#!/usr/bin/env python3

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


import argparse
import re
import signal
import sys

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication

from qflashlight.application import Application


def parse_args(args: list[str]) -> argparse.Namespace:
    def QRect_from_string(text: str) -> QRect:
        m = re.match(r'^(\d+)x(\d+)\+(\d+)\+(\d+)$', text)
        if not m:
            raise ValueError(f"couldn't parse geometry (WxH+X+Y): {text}")

        return QRect(int(m.group(3)),
                     int(m.group(4)),
                     int(m.group(1)),
                     int(m.group(2)))

    QRect_from_string.__name__ = "QRect"

    def QColor_from_string(text: str) -> QColor:
        color = QColor(text)
        if not color.isValid():
            raise ValueError("invalid color name: ")

        return color

    QColor_from_string.__name__ = "QColor"

    def QFont_from_string(text: str) -> QFont:
        return QFont(text)

    QFont_from_string.__name__ = "QFont"

    parser = argparse.ArgumentParser(description="QFlashlight - Fill the screen with a solid color")
    parser.add_argument("FILE", nargs="?")

    style = parser.add_argument_group("Style")
    style.add_argument("-c", "--color", metavar="COLOR", type=QColor_from_string, default=Qt.black,
                       help="Color to use for the background (#FFF, #FFFFFF or name)")
    style.add_argument("-T", "--text-color", metavar="COLOR", type=QColor_from_string, default=Qt.white,
                       help="Color to use for text")
    style.add_argument("-F", "--font", metavar="FONT", type=QFont_from_string, default=QFont(),
                       help="Use FONT to display text")

    content = parser.add_argument_group("Content")
    content.add_argument("-t", "--text", metavar="TEXT", type=str, default=None,
                         help="Display text")
    content.add_argument("-C", "--command", metavar="CMD", type=str, default=None,
                         help="Runs CMD and shows the output")
    content.add_argument("-n", "--interval", metavar="SECONDS", type=float, default=None,
                         help="Refresh the screen and rerun command every SECONDS seconds (default: None)")

    window = parser.add_argument_group("Window")
    window.add_argument("-f", "--fullscreen", action="store_true", default=False,
                        help="Start in fullscreen mode")
    window.add_argument("-w", "--window", action="store_false", dest="fullscreen", default=False,
                        help="Start in window mode")
    window.add_argument("-m", "--hide-cursor", action="store_true", default=False,
                        help="Hide the mouse cursor")
    window.add_argument("-b", "--borderless", action="store_true", default=False,
                        help="Run the window without a border")
    window.add_argument("-g", "--geometry", metavar="WxH+X+Y", type=QRect_from_string, default=None,
                        help="Set the size and position of the window")

    return parser.parse_args(args)


def main(argv: list[str]) -> None:
    args = parse_args(argv[1:])

    # allow Ctrl-C to close the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    qapp = QApplication(sys.argv)
    app = Application()

    # Style
    app.set_foreground_color(args.text_color)
    app.set_background_color(args.color)
    app.set_font(args.font)

    # Content
    if args.FILE is None:
        app.set_text(args.text)
    else:
        if args.FILE[0] == "-":
            text = sys.stdin.read()
        else:
            with open(args.FILE) as fin:
                text = fin.read()
        app.set_text(text.rstrip("\n"))

    if args.command is not None:
        app.set_command(args.command, args.interval)

    if args.fullscreen:
        app.set_fullscreen(True)

    if args.borderless:
        app.set_borderless(True)

    if args.hide_cursor:
        app.set_show_cursor(False)

    if args.geometry is not None:
        app.set_window_geometry(args.geometry)

    # Run App
    app.show()
    sys.exit(qapp.exec_())


def main_entrypoint() -> None:
    main(sys.argv)


if __name__ == '__main__':
    main_entrypoint()


# EOF #
