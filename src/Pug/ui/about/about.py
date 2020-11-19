#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import sys

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class About(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(kwargs, "parent"):
            self.parent = getattr(kwargs, "parent")

        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("ui/about/about.ui", self)
        self.bind_signals()

        about_text = self.get_file("README.md")
        self.about_text.setMarkdown(about_text)

        license_text = self.get_file("LICENSE")
        self.license_text.setPlainText(license_text)

    def bind_signals(self):
        self.button_box.accepted.connect(self.accept)

    def get_file(self, file_path) -> str:
        """ Gets the text in the README file """
        file_text: str

        with open(file_path) as f:
            file_text = f.read()

        return file_text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    about = About()
    about.show()
    sys.exit(app.exec())