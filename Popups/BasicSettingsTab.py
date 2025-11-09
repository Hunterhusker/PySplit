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
        self.colorPicker2.setFixedSize(300, 35)

        # add them to scroll widget layout here, and it will show up
        self.testGroupLayout.addWidget(self.label)
        self.testGroupLayout.addWidget(self.label2)
        self.testGroupLayout.addWidget(self.colorPicker)
        self.testGroupLayout.addWidget(self.colorPicker2)

        self.scroll_widget_layout.addWidget(self.testGroup)

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
