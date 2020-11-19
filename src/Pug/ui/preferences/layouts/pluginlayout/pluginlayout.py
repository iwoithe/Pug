#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pluginlayout.py
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


class PluginLayout(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/preferences/layouts/pluginlayout/pluginlayout.ui', self)

        self.load_plugin_paths()

        self.bind_signals()

    def load_plugin_paths(self):
        # Index 0: Plugin Path
        # Index 1: Is the plugin installed
        for plugin_path in self.parent.parent.settings["Plugin Paths"]:
            if plugin_path[0] is not "":
                dir = QListWidgetItem(plugin_path[0], self.plugin_paths_view)

    def bind_signals(self):
        self.button_add_plugin_paths.clicked.connect(self.add_plugin_paths)
        self.button_remove_plugin_paths.clicked.connect(self.remove_plugin_paths)

    @pyqtSlot()
    def add_plugin_paths(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self.parent,
                                                  "Open Folder",
                                                  self.parent.parent.settings["Current Directory"],
                                                  options=options)

        if folder:
            self.parent.parent.settings["Current Directory"] = folder

            dir = QListWidgetItem(folder, self.plugin_paths_view)

    @pyqtSlot()
    def remove_plugin_paths(self):
        selected_items = self.plugin_paths_view.selectedItems()

        for item in selected_items:
            self.plugin_paths_view.takeItem(self.plugin_paths_view.row(item))
