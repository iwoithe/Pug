#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  packagelists.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Pug.core.piputils import *


class PackageListsToolbar(QToolBar):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setup_actions()
        self.add_actions()
        self.bind_signals()

        self.setWindowTitle("Package Lists Toolbar")
        icon_size = self.parent.settings["Icon Size"]
        self.setIconSize(QSize(*icon_size))

    def setup_actions(self):
        # Download PyPI Package List action
        self.download_pypi_package_list_action = QAction(QIcon("data/assets/download_pypi_package_list.svg"), "Download PyPI Package List", self)

    def add_actions(self):
        self.addAction(self.download_pypi_package_list_action)

    def bind_signals(self):
        # Download PyPI Package List action
        self.download_pypi_package_list_action.triggered.connect(self.download_pypi_package_list)

    def download_pypi_package_list(self):
        try:
            save_pypi_package_list(self.parent.console)
        except:
            save_pypi_package_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    package_lists_toolbar = PackageListsToolbar(QToolBar)
    package_lists_toolbar.show()
    sys.exit(app.exec())
