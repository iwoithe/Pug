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
import subprocess

from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Uninstall(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.packages = self.get_packages()

        # Setup the user interface
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi('ui/docks/uninstall/uninstall.ui', self)
        self.bind_signals()

        # Update the package list on intialisation
        self.update_package_list("")

    def bind_signals(self):
        self.entry_search.textEdited.connect(self.update_package_list)

        self.button_uninstall.clicked.connect(self.uninstall_package)

    def get_packages(self, python_version=3) -> list:
        # TODO: Switch everything over to QProcess (not subprocess.run)
        if python_version == 3:
            # Use Pip's module to avoid warnings, on Linux
            try:
                pip_freeze_output = subprocess.run(['python3', '-m', 'pip', 'freeze'], capture_output=True)
            except FileNotFoundError:
                # On Windows, Python 2 is not installed
                pip_freeze_output = subprocess.run(['python', '-m', 'pip', 'freeze'], capture_output=True)
        else:
            # Use Python 2
            pip_freeze_output = subprocess.run(['python', '-m', 'pip', 'freeze'], capture_output=True)

        packages = []
        if pip_freeze_output:
            installed_packages = pip_freeze_output.stdout.decode("utf-8").split()

            for package in installed_packages:
                package_name, package_version = package.split("==")
                packages.append(package_name)

        return packages

    @pyqtSlot(str)
    def update_package_list(self, text):
        """ Update the package list """

        # Clear the packages list
        self.packages_list.clear()

        # Add the packages that match the search to the packages list
        for package in self.packages:
            if text.lower() in package.lower():
                QListWidgetItem(package, self.packages_list)

    @pyqtSlot()
    def uninstall_package(self, python_version=3):
        """ Uninstalls the selected package """
        current_item = self.packages_list.currentItem()

        if current_item:
            package = current_item.text()
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
                self.pip_process.setArguments(['-m', 'pip', 'uninstall', '--yes', package])

            if self.pip_process:
                self.pip_process.readyReadStandardOutput.connect(self.update_uninstallation_process)
                self.pip_process.finished.connect(self.on_pip_process_finished)
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
