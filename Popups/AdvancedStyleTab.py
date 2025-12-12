from __future__ import annotations

import os

from PySide6.QtWidgets import QSplitter, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QPlainTextEdit
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab


class AdvancedStyleTab(ABCSettingTab):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        self.main = mainWindow  # keep a link to the parent for later

        self.layout = QVBoxLayout()

        self.splitter = QSplitter(Qt.Horizontal)

        self.style_textarea = QPlainTextEdit()
        self.style_textarea.setPlainText(self.main.settings.style.raw_style_sheet)
        self.style_textarea.setObjectName("StyleTextArea")

        self.var_textarea = QPlainTextEdit()
        self.var_textarea.setPlainText(self.main.settings.style.raw_vars)
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

        self.main.configurator.style.update_style(var_map=var_map, style_sheet=self.style_textarea.toPlainText())
