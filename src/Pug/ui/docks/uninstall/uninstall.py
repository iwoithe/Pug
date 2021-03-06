#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  uninstall.py
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
import time
import shutil

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Uninstall(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.packages_list = []
        self.get_packages()

        self.packages_model = QStringListModel()
        self.proxy_packages_model = QSortFilterProxyModel()

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

        try:
            self.parent.console.add_text("Number of Installed Packages: " + str(self.packages_model.rowCount()))
        except:
            print("Number of Installed Packages: " + self.packages_model.rowCount())

    def setup_ui(self):
        uic.loadUi('Pug/ui/docks/uninstall/uninstall.ui', self)
        self.bind_signals()

        self.packages_view.setModel(self.proxy_packages_model)

        # Update the package list on initialisation
        self.update_package_list("")

    def bind_signals(self):
        self.entry_search.textEdited.connect(self.update_package_list)

        self.button_uninstall.clicked.connect(self.uninstall_package)

    def get_packages(self, python_version=2) -> list:
        self.get_packages_process = QProcess()

        if python_version == 3:
            # Try the python3 command, otherwise fallback to the python command
            if shutil.which("python3"):
                self.get_packages_process.setProgram("python3")
            else:
                self.get_packages_process.setProgram("python")
        else:
            self.get_packages_process.setProgram("python")

        if self.get_packages_process.program():
            self.get_packages_process.setArguments(["-m", "pip", "list", "--format", "freeze"])

        self.get_packages_process.finished.connect(self.get_packages_finished)
        self.get_packages_process.start()

    def get_packages_finished(self):
        str_data = str(self.get_packages_process.readAll(), 'utf-8').strip()
        if str_data:
            installed_packages = str_data.split()
            for package in installed_packages:
                package_name, package_version = package.split("==")
                self.packages_list.append(package_name)

        self.packages_model = QStringListModel(self.packages_list)
        self.proxy_packages_model.setSourceModel(self.packages_model)

    @pyqtSlot(str)
    def update_package_list(self, text):
        """ Update (filter) the package list """
        # Using a QListView instead of QListWidget for better performance
        # TODO: Create option in GUI to slice the list of PyPi packages
        #       to get quicker load time

        start_time = time.time()

        # Filter the packages
        self.proxy_packages_model.setFilterFixedString(text)

        end_time = time.time()

        try:
            self.parent.console.add_text("Filtering Installed Packages Time: " + str(end_time - start_time))
        except:
            print("Filtering Installed Packages Time: " + str(end_time - start_time))

    @pyqtSlot()
    def uninstall_package(self, python_version=3):
        """ Uninstalls the selected package """
        current_item_index = self.packages_view.currentIndex()

        if current_item_index:
            package = current_item_index.data(Qt.DisplayRole)
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
                self.pip_process.setArguments(['-m', 'pip', 'uninstall', '--yes', package])

            if self.pip_process:
                self.pip_process.readyReadStandardOutput.connect(self.update_uninstallation_process)
                self.pip_process.finished.connect(self.get_packages_finished)
                self.pip_process.start()

    def update_uninstallation_process(self):
        str_data = str(self.pip_process.readAll(), 'utf-8').strip()
        try:
            self.parent.console.add_text(str_data)
        except:
            print(str_data)

    def on_pip_process_finished(self):
        self.packages = self.get_packages()
        self.entry_search.textChanged.emit(self.entry_search.text())

        try:
            self.parent.console.add_text("Finished")
        except:
            print("Finished")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    uninstall = Uninstall()
    uninstall.show()
    sys.exit(app.exec())
