from Widgets.ColorPickerWidget import ColorPickerWidget
from helpers.TimerFormat import format_wall_clock_from_ms
from Main import Main
from pathlib import Path
from PySide6.QtGui import QFontDatabase, QColor
from PySide6.QtWidgets import QApplication, QMessageBox
import sys
import unittest
from unittest.mock import patch


class TestColorPickerWidget(unittest.TestCase):
    def setUp(self):
        self._app = QApplication.instance()
        if self._app is None:
            self._app = QApplication(sys.argv)

    def test_color_picker_widget_defaults(self):
        widget = ColorPickerWidget()
        self.assertEqual(widget.color, QColor("#ffff0000"))
