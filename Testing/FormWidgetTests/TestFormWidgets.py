import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtTest import QSignalSpy, QTest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from Main import Main
from Widgets.FormWidgets import *


def _get_a_main():
    BASE_DIR = Path(__file__).resolve().parents[1]  # Testing/
    CONFIG_PATH = BASE_DIR / "conf" / "test_settings.json"

    return Main(CONFIG_PATH)


class TestFormWidgets(unittest.TestCase):
    def setUp(self):
        self._app = QApplication.instance()
        if self._app is None:
            self._app = QApplication(sys.argv)

        self.main = _get_a_main()

    def tearDown(self):
        if self.main is not None:
            with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
                self.main.close()
                self.main.deleteLater()

    def test_LabeledTextEntry_init(self):
        widget = LabeledTextEntry('label', 'foo')

        self.assertEqual(widget.getLabel(), 'label')
        self.assertEqual(widget.text(), 'foo')

    def test_LabeledTextEntry_setText(self):
        widget = LabeledTextEntry('label', 'foo')
        spy = QSignalSpy(widget.textChanged)

        widget.setText('bar')

        self.assertEqual(widget.text(), 'bar')
        self.assertEqual(widget.input.text(), 'bar')
        self.assertEqual(spy.count(), 1)

    def test_LabeledTextEntry_changeLabel(self):
        widget = LabeledTextEntry('label', 'foo')

        widget.setLabel('NEW')

        self.assertEqual(widget.getLabel(), 'NEW')
        self.assertEqual(widget.label.text(), 'NEW')

    def test_LabeledSpinBox_init(self):
        widget = LabeledSpinBox('label', 5)

        self.assertEqual(widget.value(), 5)
        self.assertEqual(widget.input.value(), 5)
        self.assertEqual(widget.label.text(), 'label')

    def test_LabeledSpinBox_setValue(self):
        widget = LabeledSpinBox('label', 5)
        spy = QSignalSpy(widget.valueChanged)

        widget.setValue(25)

        self.assertEqual(widget.value(), 25)
        self.assertEqual(widget.input.value(), 25)
        self.assertEqual(spy.count(), 1)

    def test_LabeledSpinBox_changeLabel(self):
        widget = LabeledSpinBox('label', 5)

        widget.setLabel('NEW')

        self.assertEqual(widget.value(), 5)
        self.assertEqual(widget.label.text(), 'NEW')
        self.assertEqual(widget.getLabel(), 'NEW')

    def test_ClickableFrame(self):
        widget = ClickableFrame()
        spy = QSignalSpy(widget.clicked)

        self.assertEqual(spy.count(), 0)

        QTest.mouseClick(widget, Qt.LeftButton)

        self.assertEqual(spy.count(), 1)
        self.assertIsInstance(widget, QFrame)

    def test_ColorPicker_get_color(self):
        widget = ColorPicker('label', QColor('#ffff0000'))

        self.assertEqual(widget.label.text(), 'label')
        self.assertEqual(widget.hex_entry.text(), '#ffff0000')
        self.assertEqual(widget.get_color(), QColor('#ffff0000'))

    def test_ColorPicker_hex_entry(self):
        widget = ColorPicker('label', QColor('#ffff0000'))

        self.assertEqual(widget.hex_entry.text(), '#ffff0000')

        widget.hex_entry.setText('#ff00ff00')

        self.assertEqual(widget.get_color().name(QColor.HexArgb), '#ff00ff00')
        self.assertEqual(widget.hex_entry.text(), '#ff00ff00')

    def test_ColorPicker_set_color(self):
        widget = ColorPicker('label', QColor('#ffff0000'))

        self.assertEqual(widget.hex_entry.text(), '#ffff0000')

        widget.set_color('#ff00ff00')

        self.assertEqual(widget.get_color().name(QColor.HexArgb), '#ff00ff00')
        self.assertEqual(widget.hex_entry.text(), '#ff00ff00')

    def test_ColorPicker_pick_color(self):
        widget = ColorPicker('label', QColor('#ffff0000'))
        spy = QSignalSpy(widget.color_preview.clicked)

        self.assertEqual(spy.count(), 0)

        with patch.object(QColorDialog, "getColor", return_value=QColor('#ff0000ff')):  # patch out the popup
            QTest.mouseClick(widget.color_preview, Qt.LeftButton)

        self.assertEqual(spy.count(), 1)
        self.assertEqual(widget.hex_entry.text(), '#ff0000ff')
