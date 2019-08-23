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
import subprocess
import sys

from typing import Optional

from PyQt5.QtCore import Qt, QPoint, QRect, QRectF
from PyQt5.QtGui import QColor, QPalette, QIcon, QContextMenuEvent, QPainter, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog, QMenu


class FlashlightWidget(QWidget):

    def __init__(self, *args) -> None:
        super().__init__(*args)

        self._bg_color: QColor = Qt.black
        self._fg_color: QColor = Qt.white

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

    def mouseDoubleClickEvent(self, ev) -> None:
        self.set_fullscreen(not self._fullscreen)

    def mousePressEvent(self, ev) -> None:
        self._mpos = ev.pos()

    def mouseMoveEvent(self, ev) -> None:
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

        menu.addAction("Change Color...", lambda: self.show_color_dialog())
        menu.addAction("Change Text Color...", lambda: self.show_text_color_dialog())

        menu.addSeparator()
        menu.addAction("Exit", lambda: self.close())
        menu.exec(ev.globalPos())

    def show_text_color_dialog(self) -> None:
        self._show_color_dialog(lambda: self._fg_color, self.set_foreground_color)

    def show_color_dialog(self) -> None:
        self._show_color_dialog(lambda: self._bg_color, self.set_background_color)

    def _show_color_dialog(self, getter, setter) -> None:
        tmpcolor = getter()

        def set_color(color):
            nonlocal tmpcolor
            setter(color)
            tmpcolor = None

        def restore_color():
            if tmpcolor is not None:
                setter(tmpcolor)

        color_dlg = QColorDialog(self)
        color_dlg.setWindowModality(Qt.WindowModal)
        color_dlg.setCurrentColor(getter())

        color_dlg.currentColorChanged.connect(setter)
        color_dlg.colorSelected.connect(set_color)
        color_dlg.rejected.connect(restore_color)

        color_dlg.show()

    def keyPressEvent(self, ev) -> None:
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
            self.show_color_dialog()
        elif ev.key() == Qt.Key_T:
            self.show_text_color_dialog()
        elif ev.key() == Qt.Key_B:
            self.set_borderless(not self._borderless)

    def set_background_color(self, bg_color) -> None:
        self._bg_color = bg_color

        pal = self.palette()
        pal.setColor(QPalette.Background, self._bg_color)
        self.setPalette(pal)

    def set_foreground_color(self, fg_color: QColor) -> None:
        self._fg_color = fg_color

        pal = self.palette()
        pal.setColor(QPalette.Foreground, self._fg_color)
        self.setPalette(pal)

    def set_text(self, text: str) -> None:
        self._text = text

    def set_command(self, command: str) -> None:
        self._command = command
        self._update_text_from_command()

    def set_refresh_interval(self, interval: Optional[float]) -> None:
        self._refresh_interval = interval

        if self._refresh_interval is not None:
            self.startTimer(self._refresh_interval * 1000.0)

    def timerEvent(self, ev) -> None:
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

    def paintEvent(self, ev) -> None:
        if self._text is not None:
            text = self._text
            painter = QPainter(self)
            font = painter.font()
            fm = QFontMetrics(font)
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


def fullscreen_flashlight(bg_color: 'QColor', fg_color: 'QColor', args):
    # allow Ctrl-C to close the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    w = FlashlightWidget()
    if not args.window:
        w.set_fullscreen(True)
    if args.hide_cursor:
        w.hide_cursor()
    w.set_background_color(bg_color)
    w.set_foreground_color(fg_color)
    w.set_refresh_interval(args.interval)
    if args.FILE is None:
        w.set_text(args.text)
    else:
        if args.FILE[0] == "-":
            text = sys.stdin.read()
        else:
            with open(args.FILE) as fin:
                text = fin.read()
        w.set_text(text.rstrip("\n"))
    w.set_command(args.command)
    w.set_borderless(args.borderless)
    if args.geometry is not None:
        w.setGeometry(args.geometry)
    w.show()
    sys.exit(app.exec_())


def str2qrect(text: str):
    m = re.match(r'^(\d+)x(\d+)\+(\d+)\+(\d+)$', text)
    if not m:
        raise Exception("error: couldn't parse geometry (WxH+X+Y): {}".format(text))
    else:
        return QRect(int(m.group(3)),
                     int(m.group(4)),
                     int(m.group(1)),
                     int(m.group(2)))


def parse_args(args):
    parser = argparse.ArgumentParser(description="QFlashlight - Fill the screen with a solid color")
    parser.add_argument("FILE", nargs="?")

    style = parser.add_argument_group("Style")
    style.add_argument("-c", "--color", metavar="COLOR", type=QColorArgument, default=Qt.black,
                       help="Color to use for the background (#FFF, #FFFFFF or name)")
    style.add_argument("-T", "--text-color", metavar="COLOR", type=QColorArgument, default=Qt.white,
                       help="Color to use for text")

    content = parser.add_argument_group("Content")
    content.add_argument("-t", "--text", metavar="TEXT", type=str, default=None,
                         help="Display text")
    content.add_argument("-C", "--command", metavar="CMD", type=str, default=None,
                         help="Runs CMD and shows the output")
    content.add_argument("-n", "--interval", metavar="SECONDS", type=float, default=None,
                         help="Refresh the screen and rerun command every SECONDS seconds (default: None)")

    window = parser.add_argument_group("Window")
    window.add_argument("-w", "--window", action="store_true", default=False,
                        help="Start in window mode")
    window.add_argument("-m", "--hide-cursor", action="store_true", default=False,
                        help="Hide the mouse cursor")
    window.add_argument("-b", "--borderless", action="store_true", default=False,
                        help="Run the window without a border")
    window.add_argument("-g", "--geometry", metavar="WxH+X+Y", type=QRectArgument, default=None,
                        help="Set the size and position of the window")

    return parser.parse_args(args)


def main(argv):
    args = parse_args(argv[1:])

    bg_color = QColor(args.color)
    if not bg_color.isValid():
        raise Exception("invalid color name")

    fg_color = QColor(args.text_color)
    if not fg_color.isValid():
        raise Exception("invalid text color name")

    fullscreen_flashlight(bg_color, fg_color, args)


def main_entrypoint():
    main(sys.argv)


if __name__ == '__main__':
    main_entrypoint()


# EOF #
