from __future__ import annotations

import os
import copy

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit, QFrame, QLabel, \
    QGroupBox, QColorDialog, QPushButton
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING
from Widgets.FormWidgets import ColorPicker, FontPicker, LabeledSpinBox

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
        self.color_group = _AppearanceSettings(self.main, parent=self)
        self.app_settings = _AppSettings(self.main, parent=self)
        self.timing_settings = _TimingSettings(self.main, parent=self)
        self.footer_settings = _FooterSettings(self.main, parent=self)

        # add all the groups into the scroll
        self.scroll_widget_layout.addWidget(self.color_group)
        self.scroll_widget_layout.addWidget(self.app_settings)
        self.scroll_widget_layout.addWidget(self.timing_settings)
        self.scroll_widget_layout.addWidget(self.footer_settings)

        # add a stretch for funsies
        self.scroll_widget_layout.addStretch()

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.layout.addWidget(self.scroll_area)

        # link it all up so that this displays
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

    def apply(self):
        self.color_group.apply()


class _AppearanceSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Appearance', parent)

        self.layout = QVBoxLayout(self)
        self.main = main

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

        self.titleFontPicker = FontPicker('Title Font: ', var_map['title-font'], 12)

        self.layout.addWidget(self.backgroundColorPicker)
        self.layout.addWidget(self.splitBackgroundColorPicker)
        self.layout.addWidget(self.currentSplitBackgroundColorPicker)
        self.layout.addWidget(self.bestTimeAheadPicker)
        self.layout.addWidget(self.bestTimeBehindPicker)
        self.layout.addWidget(self.savedTimeAheadPicker)
        self.layout.addWidget(self.savedTimeBehindPicker)
        self.layout.addWidget(self.lostTimeAheadPicker)
        self.layout.addWidget(self.lostTimeBehindPicker)
        self.layout.addWidget(self.titleFontPicker)

    def apply(self):
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

        # apply the fonts
        var_map['title-font'] = self.titleFontPicker.get_font_family()
        var_map['title-size'] = f'{self.titleFontPicker.get_size()}px'

        self.main.configurator.style.update_style(var_map=var_map)


class _AppSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('App Settings')

        self.layout = QVBoxLayout(self)

    def apply(self):
        pass


class _TimingSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Timing Settings')

        self.layout = QVBoxLayout(self)

    def apply(self):
        pass


class _FooterSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Timing Settings')

        # TODO : Make the footer so I can configure it

        self.layout = QVBoxLayout(self)

    def apply(self):
        pass
