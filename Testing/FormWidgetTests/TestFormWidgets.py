import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtTest import QSignalSpy
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
