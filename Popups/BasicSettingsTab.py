from __future__ import annotations

import os
import copy

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit, QFrame, QLabel, \
    QGroupBox, QColorDialog, QPushButton
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING
from Widgets.FormWidgets import ColorPicker

from Popups.ABCSettingTab import ABCSettingTab


# checkout QGroupBox for title and then box of settings items
class BasicSettingsTab(ABCSettingTab):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        self.layout = QVBoxLayout()
        self.main = mainWindow

        self.scroll_widget = QWidget()
        self.scroll_widget_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)

        # create a group for selecting colors
        self.colorGroup = QGroupBox('Colors')
        self.colorGroupLayout = QVBoxLayout(self.colorGroup)

        var_map = self.main.configurator.style.variable_map

        self.backgroundColorPicker = ColorPicker('Background: ', QColor(var_map['primary-background']), parent=self)

        self.splitBackgroundColorPicker = ColorPicker('Split Background: ', QColor(var_map['split-background']), parent=self)
        self.currentSplitBackgroundColorPicker = ColorPicker('Current Split: ', QColor(var_map['current-split-background']), parent=self)

        self.bestTimeAheadPicker = ColorPicker('Best Time: ', QColor(var_map['best-time-color-ahead']), parent=self)
        self.bestTimeBehindPicker = ColorPicker('Best Time (Behind): ', QColor(var_map['best-time-color-behind']), parent=self)

        self.savedTimeAheadPicker = ColorPicker('Saved Time: ', QColor(var_map['saved-time-color-ahead']), parent=self)
        self.savedTimeBehindPicker = ColorPicker('Saved Time (Behind): ', QColor(var_map['saved-time-color-behind']), parent=self)

        self.lostTimeAheadPicker = ColorPicker('Lost Time: ', QColor(var_map['lost-time-color-ahead']), parent=self)
        self.lostTimeBehindPicker = ColorPicker('Lost Time (Behind): ', QColor(var_map['lost-time-color-behind']), parent=self)

        self.colorGroupLayout.addWidget(self.backgroundColorPicker)
        self.colorGroupLayout.addWidget(self.splitBackgroundColorPicker)
        self.colorGroupLayout.addWidget(self.currentSplitBackgroundColorPicker)
        self.colorGroupLayout.addWidget(self.bestTimeAheadPicker)
        self.colorGroupLayout.addWidget(self.bestTimeBehindPicker)
        self.colorGroupLayout.addWidget(self.savedTimeAheadPicker)
        self.colorGroupLayout.addWidget(self.savedTimeBehindPicker)
        self.colorGroupLayout.addWidget(self.lostTimeAheadPicker)
        self.colorGroupLayout.addWidget(self.lostTimeBehindPicker)

        # add all the groups into the scroll
        self.scroll_widget_layout.addWidget(self.colorGroup)

        # add a stretch for funsies
        self.scroll_widget_layout.addStretch()

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.layout.addWidget(self.scroll_area)

        # link it all up so that this displays
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

    def pickColor(self):
        color = QColorDialog.getColor(QColor('#ffffff'), self, "Select A Color")

        if color.isValid():
            self.label.setText(color.name())

    def apply(self):
        self.apply_colors()

    def apply_colors(self):
        var_map = copy.deepcopy(self.main.configurator.style.variable_map)

        var_map['primary-background'] = self.backgroundColorPicker.color_name
        var_map['split-background'] = self.splitBackgroundColorPicker.color_name
        var_map['current-split-background'] = self.currentSplitBackgroundColorPicker.color_name

        # split time colors
        var_map['best-time-color-ahead'] = self.bestTimeAheadPicker.color_name
        var_map['best-time-color-behind'] = self.bestTimeBehindPicker.color_name
        var_map['saved-time-color-ahead'] = self.savedTimeAheadPicker.color_name
        var_map['saved-time-color-behind'] = self.savedTimeBehindPicker.color_name
        var_map['lost-time-color-ahead'] = self.lostTimeAheadPicker.color_name
        var_map['lost-time-color-behind'] = self.lostTimeBehindPicker.color_name

        self.main.configurator.style.update_style(var_map=var_map)
