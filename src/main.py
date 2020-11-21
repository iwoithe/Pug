#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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

import os
import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Pug.ui

from Pug.ui.about import About
from Pug.ui.docks import Install, Uninstall, Console, QuickInstall, QuickUninstall
from Pug.ui.preferences import PreferencesDialog
from Pug.ui.toolbars import PackageListsToolbar


# TODO: Use the logging library instead of print


class PugWindow(QMainWindow):

    settings_file = "data/settings.json"
    with open(settings_file) as f:
        settings = json.loads(f.read())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()

    def setup_ui(self):
        self.add_toolbars()
        self.add_docks()
        self.setup_window()

    def add_docks(self):
        # There is no central layout, use docks instead
        # Console has to be defined first to avoid errors
        self.console = Console(parent=self)

        self.install = Install(parent=self)
        self.uninstall = Uninstall(parent=self)

        self.quick_install = QuickInstall(parent=self)
        self.quick_uninstall = QuickUninstall(parent=self)

        # Add the docks to the display
        self.addDockWidget(Qt.LeftDockWidgetArea, self.install)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.uninstall)
        self.addDockWidget(Qt.RightDockWidgetArea, self.console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.quick_install)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.quick_uninstall)

        # Split/Group docks as necessary
        self.splitDockWidget(self.install, self.uninstall, Qt.Vertical)
        self.splitDockWidget(self.quick_install, self.quick_uninstall, Qt.Horizontal)

    def add_toolbars(self):
        self.package_lists = PackageListsToolbar(self)
        self.addToolBar(self.package_lists)

    def create_actions(self):
        # Quit
        self.action_quit = QAction("Quit")
        self.action_quit.setShortcuts(QKeySequence("Ctrl+Q"))
        self.action_quit.triggered.connect(self.quit)

        # Preferences
        self.action_preferences = QAction("Preferences", self)
        self.action_preferences.setStatusTip("Open the preferences")
        self.action_preferences.setShortcuts(QKeySequence("Ctrl+Shift+P"))
        self.action_preferences.triggered.connect(self.show_preferences)

        # About
        self.action_about = QAction("About", self)
        self.action_about.setStatusTip("About Pug")
        self.action_about.triggered.connect(self.show_about)

        # About Qt
        self.action_about_qt = QAction("About Qt", self)
        self.action_about_qt.setStatusTip("About Qt")
        self.action_about_qt.triggered.connect(QApplication.instance().aboutQt)

    def create_menu_bar(self):
        menu_bar = QMenuBar()

        # File
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.action_quit)

        # Edit
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.action_preferences)

        # View
        view_menu = menu_bar.addMenu("&View")

        # Toolbars
        toolbars_menu = view_menu.addMenu("Toolbars")
        toolbars_menu.addAction(self.package_lists.toggleViewAction())

        # Docks
        docks_menu = view_menu.addMenu("Docks")
        docks_menu.addAction(self.install.toggleViewAction())
        docks_menu.addAction(self.uninstall.toggleViewAction())
        docks_menu.addAction(self.quick_install.toggleViewAction())
        docks_menu.addAction(self.quick_uninstall.toggleViewAction())
        docks_menu.addAction(self.console.toggleViewAction())

        # Help
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.action_about)
        help_menu.addAction(self.action_about_qt)

        return menu_bar

    def setup_window(self):
        """ Sets up the window (e.g. title, icon, menubar etc.) """
        # Title
        self.setWindowTitle("Pug")

        # Menu Bar
        self.create_actions()
        menu_bar = self.create_menu_bar()
        self.setMenuBar(menu_bar)

        # Set the style
        style = Pug.ui.utils.load_style_from_file(os.path.join("data/styles/", self.settings["Style"].lower() + ".qss"))
        Pug.ui.utils.apply_style(style)

        # Configure dock widgets
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(self.AnimatedDocks | self.AllowNestedDocks | self.AllowTabbedDocks | self.GroupedDragging)

    def load_plugins(self):
        """ Load the plugins that Pug knows about """
        # TODO: Write the plugin system
        pass

    def show_about(self):
        about = About(self)
        about.exec()

    def show_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec()

    def quit(self):
        QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    pug = PugWindow()
    pug.show()
    sys.exit(app.exec())
