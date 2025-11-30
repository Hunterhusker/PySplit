from __future__ import annotations

import copy

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit, QFrame, QLabel, \
    QGroupBox, QColorDialog, QPushButton, QCheckBox
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

from Models.Game import Game
from Widgets.FormWidgets import ColorPicker, FontPicker, FileDialogOpener

from Popups.ABCSettingTab import ABCSettingTab


# checkout QGroupBox for title and then box of settings items
class BasicSettingsTab(ABCSettingTab):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        self.layout = QVBoxLayout()
        self.main = mainWindow

        self.scroll_widget = QWidget()
        self.scroll_widget_layout = QVBoxLayout()
        self.scroll_widget_layout.setSpacing(20)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)

        # create a group for selecting colors
        self.app_settings = _AppSettings(self.main, parent=self)
        self.text_group = _TextSettings(self.main, parent=self)
        self.color_group = _ColorSettings(self.main, parent=self)
        self.timing_settings = _TimingSettings(self.main, parent=self)
        self.footer_settings = _FooterSettings(self.main, parent=self)

        # add all the groups into the scroll
        self.scroll_widget_layout.addWidget(self.app_settings)
        self.scroll_widget_layout.addWidget(self.text_group)
        self.scroll_widget_layout.addWidget(self.color_group)
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
        for i in range(self.scroll_widget_layout.count() - 1):  # -1 so we don't apply on the stretch
            self.scroll_widget_layout.itemAt(i).widget().apply()  # for each thing added to the layout, run the apply method on them


class _ColorSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Color Settings', parent)

        self.layout = QVBoxLayout(self)
        self.main = main

        var_map = self.main.configurator.style.variable_map

        self.backgroundColorPicker = ColorPicker('Background: ', QColor(var_map['primary-background']), parent=self)
        self.layout.addWidget(self.backgroundColorPicker)

        curr = var_map.get('background-image', 'none')
        if curr != 'none' and '"' in curr:
            start = curr.index('"') + 1
            end = curr.rindex('"')

            bg_img_path = curr[start:end]
        else:
            bg_img_path = curr

        self.backgroundImagePicker = FileDialogOpener('Background Image: ', file_path=bg_img_path, file_filter="Images (*.png *.jpg *.jpeg *.bmp *.svg)")
        self.layout.addWidget(self.backgroundImagePicker)

        self.separatorColorPicker = ColorPicker('Separator: ', QColor(var_map['border-color']), parent=self)
        self.layout.addWidget(self.separatorColorPicker)

        self.splitBackgroundColorPicker = ColorPicker('Split Background: ', QColor(var_map['split-background']), parent=self)
        self.layout.addWidget(self.splitBackgroundColorPicker)

        self.currentSplitBackgroundColorPicker = ColorPicker('Current Split: ', QColor(var_map['current-split-background']), parent=self)
        self.layout.addWidget(self.currentSplitBackgroundColorPicker)

        self.bestTimeAheadPicker = ColorPicker('Best Time: ', QColor(var_map['best-time-color-ahead']), parent=self)
        self.layout.addWidget(self.bestTimeAheadPicker)

        self.bestTimeBehindPicker = ColorPicker('Best Time (Behind): ', QColor(var_map['best-time-color-behind']), parent=self)
        self.layout.addWidget(self.bestTimeBehindPicker)

        self.savedTimeAheadPicker = ColorPicker('Saved Time: ', QColor(var_map['saved-time-color-ahead']), parent=self)
        self.layout.addWidget(self.savedTimeAheadPicker)

        self.savedTimeBehindPicker = ColorPicker('Saved Time (Behind): ', QColor(var_map['saved-time-color-behind']), parent=self)
        self.layout.addWidget(self.savedTimeBehindPicker)

        self.lostTimeAheadPicker = ColorPicker('Lost Time: ', QColor(var_map['lost-time-color-ahead']), parent=self)
        self.layout.addWidget(self.lostTimeAheadPicker)

        self.lostTimeBehindPicker = ColorPicker('Lost Time (Behind): ', QColor(var_map['lost-time-color-behind']), parent=self)
        self.layout.addWidget(self.lostTimeBehindPicker)

    def apply(self):
        var_map = copy.deepcopy(self.main.configurator.style.variable_map)

        var_map['primary-background'] = self.backgroundColorPicker.color_name
        var_map['border-color'] = self.separatorColorPicker.color_name
        var_map['split-background'] = self.splitBackgroundColorPicker.color_name
        var_map['current-split-background'] = self.currentSplitBackgroundColorPicker.color_name

        # split time colors
        var_map['best-time-color-ahead'] = self.bestTimeAheadPicker.color_name
        var_map['best-time-color-behind'] = self.bestTimeBehindPicker.color_name
        var_map['saved-time-color-ahead'] = self.savedTimeAheadPicker.color_name
        var_map['saved-time-color-behind'] = self.savedTimeBehindPicker.color_name
        var_map['lost-time-color-ahead'] = self.lostTimeAheadPicker.color_name
        var_map['lost-time-color-behind'] = self.lostTimeBehindPicker.color_name

        # url("/home/hunter/Pictures/Backgrounds/dbpg16g-d0814f5c-4142-4dbb-b50d-f22e0fe1e103.jpg") 0 0 0 0 stretch stretch;
        bg_img_path = self.backgroundImagePicker.file_path

        if bg_img_path != 'none':
            bg_img_path = f'url("{bg_img_path}") 0 0 0 0 stretch stretch'

        var_map['background-image'] = bg_img_path

        self.main.configurator.style.update_style(var_map=var_map)


class _TextSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Text Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        var_map = self.main.configurator.style.variable_map

        self.titleFontPicker = FontPicker('Title Font: ', var_map['title-font'], var_map['title-size'])
        self.titleColorPicker = ColorPicker('Title Color: ', QColor(var_map['title-color']), parent=parent)

        self.subtitleFontPicker = FontPicker('Sub-Title Font: ', var_map['subtitle-font'], var_map['subtitle-size'])
        self.subtitleColorPicker = ColorPicker('Sub-Title Color: ', QColor(var_map['subtitle-color']), parent=parent)

        self.splitFontPicker = FontPicker('Split Font: ', var_map['split-font'], var_map['split-size'])
        self.splitColorPicker = ColorPicker('Split Color: ', QColor(var_map['split-color']), parent=parent)

        self.timerFontPicker = FontPicker('Timer Font: ', var_map['timer-font'], var_map['timer-size'])
        self.timerColorPicker = ColorPicker('Timer Color: ', QColor(var_map['timer-color']), parent=parent)

        self.layout.addWidget(self.titleFontPicker)
        self.layout.addWidget(self.titleColorPicker)

        self.layout.addWidget(self.subtitleFontPicker)
        self.layout.addWidget(self.subtitleColorPicker)

        self.layout.addWidget(self.splitFontPicker)
        self.layout.addWidget(self.splitColorPicker)

        self.layout.addWidget(self.timerFontPicker)
        self.layout.addWidget(self.timerColorPicker)

    def apply(self):
        var_map = copy.deepcopy(self.main.configurator.style.variable_map)

        var_map['title-font'] = self.titleFontPicker.get_font_family()
        var_map['title-size'] = f'{self.titleFontPicker.get_size()}px'
        var_map['title-color'] = self.titleColorPicker.color_name

        var_map['subtitle-font'] = self.subtitleFontPicker.get_font_family()
        var_map['subtitle-size'] = f'{self.subtitleFontPicker.get_size()}px'
        var_map['subtitle-color'] = self.subtitleColorPicker.color_name

        var_map['split-font'] = self.splitFontPicker.get_font_family()
        var_map['split-size'] = f'{self.splitFontPicker.get_size()}px'
        var_map['split-color'] = self.splitColorPicker.color_name

        var_map['timer-font'] = self.timerFontPicker.get_font_family()
        var_map['timer-size'] = f'{self.timerFontPicker.get_size()}px'
        var_map['timer-color'] = self.timerColorPicker.color_name

        self.main.configurator.style.update_style(var_map=var_map)


class _AppSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('App Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        self.checkbox = QCheckBox('Enable Advanced Styling')
        self.checkbox.setFixedHeight(40)  # just to make it look like our QFrames since we didn't need to make a custom for this one
        self.layout.addWidget(self.checkbox)

        # self.theme_file_chooser = FileDialogOpener('Theme File: ')
        # self.layout.addWidget(self.theme_file_chooser)

        self.splits_file_chooser = FileDialogOpener('Splits File: ', file_path=self.main.configurator.game_path)
        self.layout.addWidget(self.splits_file_chooser)

    def apply(self):
        # show / hide the advanced tab
        self.main.settings_window.set_tab_visibility('Advanced', self.checkbox.isChecked())

        self.main.configurator.game.update_from_file(self.splits_file_chooser.file_path)
        self.main.configurator.game.GameUpdated.emit(self.main.configurator.game)


class _TimingSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Timing Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

    def apply(self):
        pass


class _FooterSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Footer Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        self.todo = QLabel('Gotta make the footer first eh?')

        self.layout.addWidget(self.todo)

    def apply(self):
        pass
