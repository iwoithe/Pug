#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  install.py
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
import subprocess

from urllib.error import URLError
from urllib.request import urlopen

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from bs4 import BeautifulSoup

from core import piputils


class Install(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load the packages
        self.packages_model = QStringListModel(self.get_packages())

        self.proxy_packages_model = QSortFilterProxyModel()
        self.proxy_packages_model.setSourceModel(self.packages_model)

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/docks/install/install.ui', self)

        # Add the version button group
        self.radio_python_2.version = 2
        self.radio_python_3.version = 3

        self.button_group_version = QButtonGroup(self)
        self.button_group_version.addButton(self.radio_python_2)
        self.button_group_version.addButton(self.radio_python_3)

        self.bind_signals()

        self.packages_list.setModel(self.proxy_packages_model)

        self.update_package_list("")

    def bind_signals(self):
        self.entry_search.textEdited.connect(self.update_package_list)
        #self.packages_list.currentTextChanged.connect(self.update_package_info)

        self.button_install.clicked.connect(self.install_package)

    def get_packages(self) -> list:
        """ Searches PyPi for a list of available packages """
        # TODO: Switch everything over to QProcess (not subprocess.run)

        try:
            packages = piputils.load_pypi_package_list()
        except:
            packages = piputils.load_pypi_package_list()

        return packages

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
            self.parent.console.add_text("Filtering PyPi Packages Time: " + str(end_time - start_time))
        except:
            print("Filtering PyPi Packages Time: " + str(end_time - start_time))

    @pyqtSlot(str)
    def update_package_info(self, package_name):
        """ Update the preview of the package """

        pass

    @pyqtSlot()
    def install_package(self, python_version=3):
        """ Installs the selected package """
        current_item_index = self.packages_list.currentIndex()

        try:
            python_version = self.button_group_version.checkedButton().version
        except:
            pass

        if current_item_index:
            package = current_item_index.data(Qt.DisplayRole)
            self.pip_process = QProcess()

            if python_version == 3:
                # Use Pip's module to avoid warnings, on Linux
                try:
                    # Try the python3 command, otherwise fallback to the
                    # python command
                    subprocess.run(['python3'], check=True)
                    self.pip_process.setProgram("python3")
                except FileNotFoundError:
                    self.pip_process.setProgram("python")
            else:
                self.pip_process.setProgram("python")

            if self.pip_process.program():
                if self.check_user_dir.isChecked():
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    install = Install()
    install.show()
    sys.exit(app.exec())
