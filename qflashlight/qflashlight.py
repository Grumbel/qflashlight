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
import logging
import re
import signal
import sys

from PyQt5.QtCore import Qt, QPoint, QRect, QRectF
from PyQt5.QtGui import QColor, QPalette, QIcon, QContextMenuEvent, QPainter, QFontMetrics
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog, QMenu


class FlashlightWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle("QFlashlight")
        self.setAutoFillBackground(True)

        self.text = None
        self.color = Qt.black
        self.text_color = Qt.white
        self.mpos = QPoint()

        self._cursor_visible = True
        self._borderless = False
        self._fullscreen = False

        self.setWindowIcon(QIcon.fromTheme("qflashlight"))

    def mouseDoubleClickEvent(self, ev):
        self.set_fullscreen(not self._fullscreen)

    def mousePressEvent(self, ev):
        self.mpos = ev.pos()

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton:
            diff = ev.pos() - self.mpos
            newpos = self.pos() + diff
            self.move(newpos)

    def contextMenuEvent(self, ev: QContextMenuEvent):
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

        menu.addAction("Change Color...", lambda: self.showColorDialog())

        menu.addSeparator()
        menu.addAction("Exit", lambda: self.close())
        menu.exec(ev.globalPos())

    def showColorDialog(self):
        tmpcolor = self.color

        def set_color(color):
            nonlocal tmpcolor
            self.setColor(color)
            tmpcolor = None

        def restore_color():
            if tmpcolor is not None:
                self.setColor(tmpcolor)

        color_dlg = QColorDialog(self)
        color_dlg.setWindowModality(Qt.WindowModal)
        color_dlg.setCurrentColor(self.color)

        color_dlg.currentColorChanged.connect(self.setColor)
        color_dlg.colorSelected.connect(set_color)
        color_dlg.rejected.connect(restore_color)

        color_dlg.show()

    def keyPressEvent(self, ev):
        if ev.key() == Qt.Key_Escape:
            self.close()
        elif ev.key() == Qt.Key_Q:
            self.close()
        elif ev.key() == Qt.Key_F:
            self.toggle_fullscreen()
        elif ev.key() == Qt.Key_M:
            if self._cursor_visible:
                self.hide_cursor()
            else:
                self.show_cursor()
        elif ev.key() == Qt.Key_C:
            self.showColorDialog()
        elif ev.key() == Qt.Key_B:
            self.set_borderless(not self._borderless)

    def setColor(self, color):
        self.color = color

        pal = self.palette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)

    def setTextColor(self, color):
        self.text_color = color

        pal = self.palette()
        pal.setColor(QPalette.Foreground, color)
        self.setPalette(pal)

    def setText(self, text):
        self.text = text

    def set_fullscreen(self, fullscreen: bool) -> None:
        self._fullscreen = fullscreen

        if self._fullscreen:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

    def set_borderless(self, borderless: bool):
        self._borderless = borderless

        if self._borderless:
            self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()

    def hide_cursor(self):
        self.setCursor(Qt.BlankCursor)
        self._cursor_visible = False

    def show_cursor(self):
        self.unsetCursor()
        self._cursor_visible = True

    def paintEvent(self, ev):
        if self.text is not None:
            # text = f" {self.text} "
            text = self.text
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


def fullscreen_flashlight(color, text_color, args):
    # allow Ctrl-C to close the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    w = FlashlightWidget()
    if not args.window:
        w.set_fullscreen(True)
    if args.hide_cursor:
        w.hide_cursor()
    w.setColor(color)
    w.setTextColor(text_color)
    w.setText(args.text)
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
    parser.add_argument("FILE", nargs='*')
    parser.add_argument("-c", "--color", metavar="COLOR", type=str, default=Qt.black,
                        help="Color to use for the background (#FFF, #FFFFFF or name)")
    parser.add_argument("-T", "--text-color", metavar="COLOR", type=str, default=Qt.white,
                        help="Color to use for text")
    parser.add_argument("-t", "--text", metavar="TEXT", type=str, default=None,
                        help="Display text")
    parser.add_argument("-w", "--window", action="store_true", default=False,
                        help="Start in window mode")
    parser.add_argument("-m", "--hide-cursor", action="store_true", default=False,
                        help="Hide the mouse cursor")
    parser.add_argument("-b", "--borderless", action="store_true", default=False,
                        help="Run the window without a border")
    parser.add_argument("-g", "--geometry", metavar="WxH+X+Y", type=str2qrect, default=None,
                        help="Set the size and position of the window")
    return parser.parse_args(args)


def main(argv):
    args = parse_args(argv[1:])

    color = QColor(args.color)
    if not color.isValid():
        raise Exception("invalid color name")

    text_color = QColor(args.text_color)
    if not text_color.isValid():
        raise Exception("invalid text color name")

    fullscreen_flashlight(color, text_color, args)


def main_entrypoint():
    main(sys.argv)


if __name__ == '__main__':
    main_entrypoint()


# EOF #
