#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  quickinstall.py
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

import shutil

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QuickInstall(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("Pug/ui/docks/quickinstall/quickinstall.ui", self)

        # Setup the radio buttons
        self.radio_python_2.version = 2
        self.radio_python_3.version = 3

        self.version_button_group = QButtonGroup()
        self.version_button_group.addButton(self.radio_python_2)
        self.version_button_group.addButton(self.radio_python_3)

        self.bind_signals()

    def bind_signals(self):
        self.install_button.clicked.connect(self.install_package)

    @pyqtSlot()
    def install_package(self):
        """ Installs the selected package """
        package_name = self.package_name_entry.text()

        try:
            python_version = self.version_button_group.checkedButton().version
        except:
            pass

        if package_name != "":
            package = package_name
            self.pip_process = QProcess()

            if python_version == 3:
                # Try the python3 command, otherwise fallback to the python command
                if shutil.which("python3"):
                    self.pip_process.setProgram("python3")
                else:
                    self.pip_process.setProgram("python")
            else:
                self.pip_process.setProgram("python")

            if self.pip_process.program():
                if self.user_dir_check.isChecked():
                    self.pip_process.setArguments(['-m', 'pip', 'install', '--user', package])
                else:
                    self.pip_process.setArguments(['-m', 'pip', 'install', package])

            if self.pip_process:
                self.pip_process.readyReadStandardOutput.connect(self.update_installation_process)
                self.pip_process.finished.connect(self.on_pip_process_finished)
                self.pip_process.start()

    def update_installation_process(self):
        str_data = str(self.pip_process.readAll(), 'utf-8').strip()
        try:
            self.parent.console.add_text(str_data)
        except:
            print(str_data)

    def on_pip_process_finished(self):
        try:
            self.parent.console.add_text("Finished")
        except:
            print("Finished")
