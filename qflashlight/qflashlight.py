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
import sys
import signal

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog


class FlashlightWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowTitle("QFlashlight")
        self.setAutoFillBackground(True)

        self.color = Qt.black
        self.mpos = QPoint()

        self.cursor_visible = True

    def setColor(self, color):
        self.color = color

        pal = self.palette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)

    def mouseDoubleClickEvent(self, ev):
        state = self.windowState()
        self.setWindowState(state ^ Qt.WindowFullScreen)

    def mousePressEvent(self, ev):
        self.mpos = ev.pos()

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton:
            diff = ev.pos() - self.mpos
            newpos = self.pos() + diff
            self.move(newpos)

    def showColorDialog(self):
        # leave fullscreen mode while the color selector is displayed
        # to prevent the color selector falling behind the fullscreen
        # window and the app being unclosable
        oldstate = self.windowState()
        self.setWindowState(oldstate & ~Qt.WindowFullScreen)

        tmpcolor = self.color

        def setColor(color):
            nonlocal tmpcolor
            self.setColor(color)
            tmpcolor = None

        color_dlg = QColorDialog()
        color_dlg.setCurrentColor(self.color)
        color_dlg.currentColorChanged.connect(self.setColor)
        color_dlg.colorSelected.connect(setColor)
        flags = self.windowFlags()
        color_dlg.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        color_dlg.exec_()
        if tmpcolor is not None:
            self.setColor(tmpcolor)

        self.setWindowState(oldstate)

    def keyPressEvent(self, ev):
        if ev.key() == Qt.Key_Escape:
            self.close()
        elif ev.key() == Qt.Key_Q:
            self.close()
        elif ev.key() == Qt.Key_F:
            self.setWindowState(self.windowState() ^ Qt.WindowFullScreen)
        elif ev.key() == Qt.Key_M:
            if self.cursor_visible:
                self.setCursor(Qt.BlankCursor)
                self.cursor_visible = False
            else:
                self.unsetCursor()
                self.cursor_visible = True
        elif ev.key() == Qt.Key_C:
            self.showColorDialog()


def fullscreenn_flashlight(color, window):
    # allow Ctrl-C to close the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    w = FlashlightWidget()
    if not window:
        w.showFullScreen()
    w.setColor(color)
    w.show()
    sys.exit(app.exec_())


def parse_args(args):
    parser = argparse.ArgumentParser(description="QFlashlight - Fill the screen with a solid color")
    parser.add_argument("FILE", nargs='*')
    parser.add_argument("-c", "--color", metavar="COLOR", type=str, default=Qt.black,
                        help="Color to use for the background (#FFF, #FFFFFF or name)")
    parser.add_argument("-w", "--window", action="store_true", default=False,
                        help="Start in window mode")
    return parser.parse_args(args)


def main(argv):
    args = parse_args(argv[1:])
    color = QColor(args.color)
    if not color.isValid():
        raise Exception("invalid color name")

    fullscreenn_flashlight(color, args.window)


def main_entrypoint():
    main(sys.argv)


if __name__ == '__main__':
    main_entrypoint()


# EOF #
