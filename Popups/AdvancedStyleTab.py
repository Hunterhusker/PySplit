from __future__ import annotations

import os

from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab
from Styling.Settings import Settings


class AdvancedStyleTab(ABCSettingTab):
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.settings = settings

        self.layout = QVBoxLayout()

        self.splitter = QSplitter(Qt.Horizontal)

        self.style_textarea = QPlainTextEdit()
        self.style_textarea.setPlainText(self.settings.style.raw_style_sheet)
        self.style_textarea.setObjectName("StyleTextArea")

        self.var_textarea = QPlainTextEdit()
        self.var_textarea.setPlainText(self.settings.style.raw_vars)
        self.var_textarea.setObjectName("VarTextArea")

        self.splitter.addWidget(self.style_textarea)
        self.splitter.addWidget(self.var_textarea)

        self.layout.addWidget(self.splitter)

        self.setLayout(self.layout)

    def apply(self):
        var_map = {}

        lines = [l for l in self.var_textarea.toPlainText().split(os.linesep) if l is not None and l != '']

        for line in lines:
            k, v = line.split(':')
            var_map[k] = v

        self.settings.style.update_style(var_map=var_map, style_sheet=self.style_textarea.toPlainText())

    def opened(self):
        # when opening, resync the settings so they match anything changed via the GUI
        self.style_textarea.setPlainText(self.settings.style.raw_style_sheet)
        self.var_textarea.setPlainText(self.settings.style.raw_vars)
