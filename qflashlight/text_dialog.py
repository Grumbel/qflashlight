# qflashlight - Simple Qt-based fullscreen flashlight
# Copyright (C) 2022 Ingo Ruhnke <grumbel@gmail.com>
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


from typing import Callable

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QDialog, QPlainTextEdit,
                             QDialogButtonBox, QHBoxLayout, QVBoxLayout)


class TextDialog(QDialog):

    sig_text_edited = pyqtSignal(str)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.resize(600, 200)
        self.setWindowTitle("Change Text")
        self.setWindowModality(Qt.WindowModal)

        self._original_text: str = ""

        # widgets
        self._text_edit = QPlainTextEdit(self)
        self._button_box = QDialogButtonBox(self)
        self._btn_ok = self._button_box.addButton(QDialogButtonBox.Ok)
        self._btn_cancel = self._button_box.addButton(QDialogButtonBox.Cancel)

        # layout
        self._vbox = QVBoxLayout()
        self._vbox.addWidget(self._text_edit)
        self._vbox.addWidget(self._button_box)

        hbox = QHBoxLayout()
        hbox.addLayout(self._vbox)

        self.setLayout(hbox)

        # signals and defaults
        self._btn_ok.setDefault(True)
        self._btn_ok.clicked.connect(self._on_ok_clicked)
        self._btn_cancel.clicked.connect(self._on_cancel_clicked)

        self._text_edit.textChanged.connect(self._on_text_changed)

    def set_text(self, text: str) -> None:
        self._original_text = text
        self._text_edit.setPlainText(text)

    def _on_text_changed(self) -> None:
        self.sig_text_edited.emit(self._text_edit.toPlainText())

    def _on_ok_clicked(self) -> None:
        self.accept()

    def _on_cancel_clicked(self) -> None:
        self.sig_text_edited.emit(self._original_text)
        self.reject()


def show_text_dialog(parent: QWidget,
                     text: str,
                     text_callback: Callable[[str], None]) -> None:
    dialog = TextDialog(parent)
    dialog.set_text(text)
    dialog.sig_text_edited.connect(text_callback)
    dialog.show()


# EOF #
