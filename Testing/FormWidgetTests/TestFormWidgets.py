import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtGui import QWheelEvent, QFontDatabase
from PySide6.QtTest import QSignalSpy, QTest
from PySide6.QtCore import Qt, QPointF, QPoint
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

        self._main = _get_a_main()

    def tearDown(self):
        if self._main is not None:
            with patch.object(QMessageBox, "exec", return_value=QMessageBox.No):  # patch out the popup
                self._main.close()
                self._main.deleteLater()

    def send_wheel_event(self, widget, delta_y=120):
        event = QWheelEvent(
            QPointF(widget.rect().center()),  # local position
            QPointF(widget.mapToGlobal(widget.rect().center())),  # global
            QPoint(0, 0),  # pixelDelta
            QPoint(0, delta_y),  # angleDelta
            Qt.NoButton,
            Qt.NoModifier,
            Qt.ScrollBegin,
            False
        )
        self._app.sendEvent(widget, event)

    def test_send_wheel_event(self):
        widget = QSpinBox()
        self.assertEqual(widget.value(), 0, 'The SpinBox did not start at 0.')
        self.send_wheel_event(widget)  # do a mock scroll on this widget

        # ensures that the scroll event goes through
        self.assertNotEqual(widget.value(), 0, 'The SpinBox did not respond to the mocked scroll event.')

    def test_NoScrollQSpinBox(self):
        widget = NoScrollQSpinBox()
        self.assertEqual(widget.value(), 0, 'The NoScrollQSpinBox did not start at 0.')
        self.send_wheel_event(widget)  # do a mock scroll on this widget
        self.assertEqual(widget.value(), 0, 'The NoScrollQSpinBox did respond to the mock scroll event, and it should not have.')

    def test_NoScrollQDoubleSpinBox(self):
        widget = NoScrollQDoubleSpinBox()
        self.assertEqual(widget.value(), 0, 'The NoScrollQDoubleSpinBox did not start at 0.')
        self.send_wheel_event(widget)  # do a mock scroll on this widget
        self.assertEqual(widget.value(), 0, 'The NoScrollQDoubleSpinBox did respond to the mock scroll event, and it should not have.')

    def test_NoScrollQTimeEdit(self):
        widget = NoScrollQTimeEdit()
        curr_time = widget.time()
        self.send_wheel_event(widget)
        self.assertEqual(widget.time(), curr_time, 'The NoScrollQTimeEdit did respond to the mock scroll event, and it should not have.')

    def test_NoScrollQFontComboBox(self):
        widget = NoScrollQFontComboBox()
        curr_font = widget.font()
        self.send_wheel_event(widget)
        self.assertEqual(widget.font(), curr_font, 'The NoScrollQFontComboBox did respond to the mock scroll event, and it should not have.')

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

    def test_LabeledSpinBox_ignore_scroll(self):
        widget = LabeledSpinBox('label', 5)

        self.assertEqual(widget.value(), 5)
        self.assertEqual(widget.input.value(), 5)

        self.send_wheel_event(widget.input)

        self.assertEqual(widget.value(), 5)
        self.assertEqual(widget.input.value(), 5)

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

    def test_FontPicker(self):
        main_font = self._main.font()
        widget = FontPicker('label', main_font.family(), 10)

        self.assertEqual(widget.get_font().family(), main_font.family())
        self.assertEqual(widget.font_combobox.currentFont(), main_font)

        self.assertEqual(widget.get_size(), 10)
        self.assertEqual(widget.size_spinner.value(), 10)

    def test_FontPicker_set_size(self):
        main_font = self._main.font()
        widget = FontPicker('label', main_font.family(), 10)

        widget.set_size(15)

        self.assertEqual(widget.get_size(), 15)
        self.assertEqual(widget.size_spinner.value(), 15)

    def test_FontPicker_set_font(self):
        font_families = QFontDatabase.families()
        main_font = self._main.font()
        main_font_idx = font_families.index(main_font.family())

        widget = FontPicker('label', main_font.family(), 10)

        new_font = QFont(font_families[min(main_font_idx + 5, len(font_families) - 1)], 10)
        widget.set_font(new_font)

        self.assertNotEqual(main_font, new_font, 'Bad test, the new font was the old font!')

        self.assertEqual(widget.get_font(), new_font, 'The new font was not the font returned by the FontPicker.')
        self.assertEqual(widget.font_combobox.currentFont(), new_font, 'The new font was not the current font for the NoScrollQFontCombobox.')

    def test_FontPicker_set_font_family(self):
        font_families = QFontDatabase.families()
        main_font = self._main.font()
        main_font_idx = font_families.index(main_font.family())

        widget = FontPicker('label', main_font.family(), 10)

        new_family = QFont(font_families[min(main_font_idx + 5, len(font_families) - 1)], 10).family()
        widget.set_font_family(new_family)

        self.assertNotEqual(main_font, new_family, 'Bad test, the new font family was the old font!')

        self.assertEqual(widget.get_font().family(), new_family, 'The new font family was not the font returned by the FontPicker.')
        self.assertEqual(widget.font_combobox.currentFont().family(), new_family,'The new font family was not the current font for the NoScrollQFontCombobox.')

    def test_FileDialogOpener(self):
        widgetSansPath = FileDialogOpener('label')
        widgetWithPath = FileDialogOpener('label2', '/test/path/file.txt')

        self.assertEqual(widgetSansPath.label.text(), 'label')
        self.assertEqual(widgetWithPath.label.text(), 'label2')

        self.assertEqual(widgetSansPath.get_file_path(), 'none')
        self.assertEqual(widgetSansPath.file_path_label.text(), 'none')

        self.assertEqual(widgetWithPath.get_file_path(), '/test/path/file.txt')
        self.assertEqual(widgetWithPath.file_path_label.text(), '/test/path/file.txt')

    def test_FileDialogOpener_open_file_click(self):
        widget = FileDialogOpener('label')
        spy = QSignalSpy(widget.open_dialog_button.clicked)

        test_path = "test/path/file.txt"

        self.assertEqual(spy.count(), 0)

        with patch.object(QFileDialog, "exec", return_value=True), patch.object(QFileDialog, "selectedFiles", return_value=[test_path]):
            QTest.mouseClick(widget.open_dialog_button, Qt.LeftButton)

        self.assertEqual(spy.count(), 1)
        self.assertEqual(widget.file_path_label.text(), test_path)
        self.assertEqual(widget.file_path, test_path)

    def test_FileDialogOpener_set_file_path(self):
        widget = FileDialogOpener('label')

        new_path = "test/path/file.txt"
        self.assertNotEqual(widget.file_path, new_path)

        widget.set_file_path(new_path)
        self.assertEqual(widget.file_path, new_path)

    def test_FileDialogOpener_set_file_path_url(self):
        widget = FileDialogOpener('label')

        new_path = "test/path/file.txt"
        new_url = f"url({new_path}) asdf asdf asdf"
        self.assertNotEqual(widget.file_path, new_path)
        self.assertNotEqual(widget.file_path, new_url)

        widget.set_file_path(new_path)
        self.assertEqual(widget.file_path, new_path)
        self.assertNotEqual(widget.file_path, new_url)  # still don't want all the URL bits in there
