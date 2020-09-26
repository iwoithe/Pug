#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  preferences.py
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
import json

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .. import utils

from .layouts import *


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.app = QApplication.instance()

        self.parent = parent

        self.setup_ui()

        #self.setWindowTitle("Preferences")
        #self.setWindowIcon(QIcon("icon.png"))

    def setup_ui(self):
        uic.loadUi("ui/preferences/preferences.ui", self)

        # Customisation
        self.customisation_settings = CustomisationLayout()
        # Style
        self.load_available_styles()
        # Icon Size
        icon_width = self.customisation_settings.spin_icon_width.value()
        icon_height = self.customisation_settings.spin_icon_height.value()
        self.customisation_settings.spin_icon_width.setValue(icon_width)
        self.customisation_settings.spin_icon_height.setValue(icon_height)

        # Plugins
        self.plugin_settings = PluginLayout(self)

        self.add_preference_views()

        self.stacked_preferences = QStackedLayout()
        self.stacked_preferences.addWidget(self.customisation_settings)
        self.stacked_preferences.addWidget(self.plugin_settings)

        self.stacked_preferences.setCurrentIndex(0)

        self.preference_properties_widget.setLayout(self.stacked_preferences)

        self.bind_signals()

    def bind_signals(self):
        self.preferences_view.currentItemChanged.connect(self.update_stacked_preferences)

        # TODO: Set the signal of the Apply button
        self.button_box.accepted.connect(self.accept)
        self.button_box.clicked.connect(self.apply_settings)
        self.button_box.rejected.connect(self.reject)

    def add_preference_views(self):
        settings = ["customisation", "plugins"]
        for setting in settings:
            setting_item = QListWidgetItem(setting.title(), self.preferences_view)
            self.preferences_view.insertItem(settings.index(setting), setting_item)

    def load_available_styles(self):
        styles = utils.load_styles_list_from_directory()
        self.customisation_settings.combo_style.addItems(styles)
        self.customisation_settings.combo_style.setCurrentText(self.parent.settings["Style"])

    def save_settings(self):
        # Update the settings dictionary
        # Style
        current_style = self.customisation_settings.combo_style.currentText().replace(" ", "_")
        self.parent.settings["Style"] = current_style

        # Icon Size
        icon_width = self.customisation_settings.spin_icon_width.value()
        icon_height = self.customisation_settings.spin_icon_height.value()
        self.parent.settings["Icon Size"] = [icon_width, icon_height]

        # Plugins
        self.parent.settings["Plugin Paths"] = []

        for plugin_path_item_num in range(self.plugin_settings.plugin_paths_view.count()):
            plugin_path_item = self.plugin_settings.plugin_paths_view.item(plugin_path_item_num)
            plugin_path = plugin_path_item.text()
            self.parent.settings["Plugin Paths"].append(plugin_path)

        # Save the changes
        with open("data/settings.json", "w") as f:
            json.dump(self.parent.settings, f, indent=4)

        # Load the plugins
        self.parent.load_plugins()

    def apply_settings(self):
        # Apply the style
        new_style_name = self.customisation_settings.combo_style.currentText().replace(" ", "_")
        new_style = utils.load_style_from_file(os.path.join("data/styles/", new_style_name + ".qss"))
        utils.apply_style(new_style)

        # Apply the icon size
        icon_size = self.parent.settings["Icon Size"]
        self.parent.package_lists.setIconSize(QSize(*icon_size))

        self.save_settings()

    @pyqtSlot()
    def update_stacked_preferences(self):
        self.stacked_preferences.setCurrentIndex(self.preferences_view.currentRow())
