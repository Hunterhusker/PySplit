from __future__ import annotations

import os

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

        self.testGroup = QGroupBox('Test Box')
        self.testGroupLayout = QVBoxLayout(self.testGroup)

        # create objects here
        self.label = QLabel('TEST')
        self.label2 = QLabel('TEST2')

        self.colorPicker = ColorPicker('Pick A Color', QColor("#ff0000"), parent=self)

        self.colorPicker2 = ColorPicker('Pick A Color', QColor("#00ff00"), parent=self)
        self.colorPicker2.setFixedSize(300, 60)

        # add them to scroll widget layout here, and it will show up
        self.testGroupLayout.addWidget(self.label)
        self.testGroupLayout.addWidget(self.label2)
        self.testGroupLayout.addWidget(self.colorPicker)
        self.testGroupLayout.addWidget(self.colorPicker2)

        # create a group for selecting colors
        self.colorGroup = QGroupBox('Colors')
        self.colorGroupLayout = QVBoxLayout(self.colorGroup)

        self.backgroundColorPicker = ColorPicker('Background: ', QColor("#2b2b2b"), parent=self)

        self.splitBackgroundColorPicker = ColorPicker('Split Background: ', QColor("#323232"), parent=self)
        self.currentSplitBackgroundColorPicker = ColorPicker('Current Split: ', QColor("#4c5052"), parent=self)

        self.bestTimeAheadPicker = ColorPicker('Best Time: ', QColor('#ffffff'), parent=self)
        self.bestTimeBehindPicker = ColorPicker('Best Time (Behind): ', QColor('#ffffff'), parent=self)

        self.savedTimeAheadPicker = ColorPicker('Saved Time: ', QColor('#ffffff'), parent=self)
        self.savedTimeBehindPicker = ColorPicker('Saved Time (Behind): ', QColor('#ffffff'), parent=self)

        self.lostTimeAheadPicker = ColorPicker('Lost Time: ', QColor('#ffffff'), parent=self)
        self.lostTimeBehindPicker = ColorPicker('Lost Time (Behind): ', QColor('#ffffff'), parent=self)

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
        self.scroll_widget_layout.addWidget(self.testGroup)
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
        raise NotImplementedError()
