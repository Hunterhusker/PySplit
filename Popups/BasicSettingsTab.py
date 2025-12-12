from __future__ import annotations

import copy

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit, QFrame, QLabel, \
    QGroupBox, QColorDialog, QPushButton, QCheckBox
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

from Models.Game import Game
from Widgets.FormWidgets import ColorPicker, FontPicker, FileDialogOpener, LabeledSpinBox, LabeledDoubleSpinBox

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

        var_map = self.main.settings.style.variable_map

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
        var_map = copy.deepcopy(self.main.settings.style.variable_map)

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

        self.main.settings.style.update_style(var_map=var_map)


class _TextSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Text Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        var_map = self.main.settings.style.variable_map

        self.title_font_picker = FontPicker('Title Font: ', var_map['title-font'], var_map['title-size'])
        self.title_color_picker = ColorPicker('Title Color: ', QColor(var_map['title-color']), parent=parent)
        self.layout.addWidget(self.title_font_picker)
        self.layout.addWidget(self.title_color_picker)

        self.subtitle_font_picker = FontPicker('Sub-Title Font: ', var_map['subtitle-font'], var_map['subtitle-size'])
        self.subtitle_color_picker = ColorPicker('Sub-Title Color: ', QColor(var_map['subtitle-color']), parent=parent)
        self.layout.addWidget(self.subtitle_font_picker)
        self.layout.addWidget(self.subtitle_color_picker)

        self.attempts_font_picker = FontPicker('Attempts Font: ', var_map['attempts-font'], var_map['attempts-size'])
        self.session_attempts_color_picker = ColorPicker('Session Attempts Color: ', QColor(var_map['session-attempts-color']), parent=parent)
        self.lifetime_attempts_color_picker = ColorPicker('Lifetime Attempts Color: ', QColor(var_map['lifetime-attempts-color']), parent=parent)
        self.layout.addWidget(self.attempts_font_picker)
        self.layout.addWidget(self.session_attempts_color_picker)
        self.layout.addWidget(self.lifetime_attempts_color_picker)

        self.split_font_picker = FontPicker('Split Font: ', var_map['split-font'], var_map['split-size'])
        self.split_color_picker = ColorPicker('Split Color: ', QColor(var_map['split-color']), parent=parent)
        self.layout.addWidget(self.split_font_picker)
        self.layout.addWidget(self.split_color_picker)

        self.timer_font_picker = FontPicker('Timer Font: ', var_map['timer-font'], var_map['timer-size'])
        self.timer_color_picker = ColorPicker('Timer Color: ', QColor(var_map['timer-color']), parent=parent)
        self.layout.addWidget(self.timer_font_picker)
        self.layout.addWidget(self.timer_color_picker)

    def apply(self):
        var_map = copy.deepcopy(self.main.settings.style.variable_map)

        var_map['title-font'] = self.title_font_picker.get_font_family()
        var_map['title-size'] = f'{self.title_font_picker.get_size()}px'
        var_map['title-color'] = self.title_color_picker.color_name

        var_map['subtitle-font'] = self.subtitle_font_picker.get_font_family()
        var_map['subtitle-size'] = f'{self.subtitle_font_picker.get_size()}px'
        var_map['subtitle-color'] = self.subtitle_color_picker.color_name

        var_map['attempts-font'] = self.attempts_font_picker.get_font_family()
        var_map['attempts-size'] = f'{self.attempts_font_picker.get_size()}px'
        var_map['session-attempts-color'] = self.session_attempts_color_picker.color_name
        var_map['lifetime-attempts-color'] = self.lifetime_attempts_color_picker.color_name

        var_map['split-font'] = self.split_font_picker.get_font_family()
        var_map['split-size'] = f'{self.split_font_picker.get_size()}px'
        var_map['split-color'] = self.split_color_picker.color_name

        var_map['timer-font'] = self.timer_font_picker.get_font_family()
        var_map['timer-size'] = f'{self.timer_font_picker.get_size()}px'
        var_map['timer-color'] = self.timer_color_picker.color_name

        self.main.settings.style.update_style(var_map=var_map)


class _AppSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('App Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        self.enableAdvancedStyles = QCheckBox('Enable Advanced Styling')
        self.enableAdvancedStyles.setFixedHeight(40)  # just to make it look like our QFrames since we didn't need to make a custom for this one
        self.layout.addWidget(self.enableAdvancedStyles)

        # self.theme_file_chooser = FileDialogOpener('Theme File: ')
        # self.layout.addWidget(self.theme_file_chooser)

        self.splits_file_chooser = FileDialogOpener('Splits File: ', file_path=self.main.settings.game_path)
        self.layout.addWidget(self.splits_file_chooser)

        # TODO : main app size setting, split height setting, splits on screen setting, icons? (Prolly not here but you get it)

    def apply(self):
        # show / hide the advanced tab
        self.main.settings_window.set_tab_visibility('Advanced', self.enableAdvancedStyles.isChecked())

        self.main.settings.game.update_from_file(self.splits_file_chooser.file_path)
        self.main.settings.game.GameUpdated.emit(self.main.settings.game)


class _TimingSettings(QGroupBox):
    def __init__(self, main: 'Main', parent=None):
        super().__init__('Timing Settings')

        self.layout = QVBoxLayout(self)
        self.main = main

        self.pinLastSplit = QCheckBox('Pin Last Split? ')
        self.pinLastSplit.setFixedHeight(40)  # just to make it look like our QFrames since we didn't need to make a custom for this one
        self.layout.addWidget(self.pinLastSplit)

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
