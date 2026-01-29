from PySide6.QtCore import Qt
from PySide6.QtTest import QSignalSpy, QTest

from Widgets.ColorPickerWidget import ColorPickerWidget
from helpers.TimerFormat import format_wall_clock_from_ms
from Main import Main
from pathlib import Path
from PySide6.QtGui import QFontDatabase, QColor
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from random import randint
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

    def test_color_picker_widget_init(self):
        h = randint(0, 359)
        s = randint(0, 255)
        v = randint(0, 255)
        a = randint(0, 255)
        color = QColor().fromHsv(h, s, v, a)

        widget = ColorPickerWidget(color)

        # check the widget's internal color
        self.assertEqual(widget.color, color,f'The supplied color {color} did not match the one saved on the widget: {widget.color}')

        # check that the hue slider matches the randomly generated hue
        self.assertEqual(widget.hue_slider.hue, h,f'The hue slider\'s value does not match the one saved on the widget. Saw: {widget.hue_slider.hue} Expected: {h}')

        # test the image cords
        self.assertEqual(widget.sv_image._marker_pos.x(), s,f'The saturation value of the SV Image Widget did not match the randomized value. Expected: {s} but saw {widget.sv_image._marker_pos.x()}')
        self.assertEqual(widget.sv_image._marker_pos.y(), 255 - v,f'The value value of the SV Image Widget did not match the inverse of the random value. Expected {255 - v} but saw {widget.sv_image._marker_pos.y()}')
        self.assertEqual(widget.a_slider.value, color.alpha())

        # check the rgb values
        self.assertEqual(widget.r_input.value(), color.red(),f'The Red value on the widget: "{widget.r_input.value()}" does not match the supplied: "{color.red()}"')
        self.assertEqual(widget.g_input.value(), color.green(),f'The Green value on the widget: "{widget.g_input.value()}" does not match the supplied: "{color.green()}"')
        self.assertEqual(widget.b_input.value(), color.blue(),f'The Blue value on the widget: "{widget.b_input.value()}" does not match the supplied: "{color.blue()}"')
        self.assertEqual(widget.a_input.value(), color.alpha(),f'The Alpha value on the widget: "{widget.a_input.value()}" does not match the supplied: "{color.alpha()}"')

        # check the hex values
        self.assertEqual(widget.hex_input.text(), color.name(QColor.NameFormat.HexArgb),f'The Hex value on the widget: "{widget.hex_input.text()}" does not match the supplied: "{color.name(QColor.NameFormat.HexArgb)}"')

    def test_color_picker_widget_color(self):
        widget = ColorPickerWidget()
        spy = QSignalSpy(widget.Color_Changed)

        self.assertEqual(spy.count(), 0)

        for i in range(10):  # repeat the test for 10 random colors to try and really test this one
            h = randint(0, 359)
            s = randint(0, 255)
            v = randint(0, 255)
            a = randint(0, 255)
            color = QColor().fromHsv(h, s, v, a)

            widget.set_color(color)

            # check the widget's internal color
            self.assertEqual(widget.color, color, f'The supplied color {color} did not match the one saved on the widget: {widget.color}')

            # check that the hue slider matches the randomly generated hue
            self.assertEqual(widget.hue_slider.hue, h, f'The hue slider\'s value does not match the one saved on the widget. Saw: {widget.hue_slider.hue} Expected: {h}')

            # test the image cords
            self.assertEqual(widget.sv_image._marker_pos.x(), s, f'The saturation value of the SV Image Widget did not match the randomized value. Expected: {s} but saw {widget.sv_image._marker_pos.x()}')
            self.assertEqual(widget.sv_image._marker_pos.y(), 255 - v, f'The value value of the SV Image Widget did not match the inverse of the random value. Expected {255 - v} but saw {widget.sv_image._marker_pos.y()}')
            self.assertEqual(widget.a_slider.value, color.alpha())

            # check the rgb values
            self.assertEqual(widget.r_input.value(), color.red(), f'The Red value on the widget: "{widget.r_input.value()}" does not match the supplied: "{color.red()}"')
            self.assertEqual(widget.g_input.value(), color.green(), f'The Green value on the widget: "{widget.g_input.value()}" does not match the supplied: "{color.green()}"')
            self.assertEqual(widget.b_input.value(), color.blue(), f'The Blue value on the widget: "{widget.b_input.value()}" does not match the supplied: "{color.blue()}"')
            self.assertEqual(widget.a_input.value(), color.alpha(), f'The Alpha value on the widget: "{widget.a_input.value()}" does not match the supplied: "{color.alpha()}"')

            # check the hex values
            self.assertEqual(widget.hex_input.text(), color.name(QColor.NameFormat.HexArgb), f'The Hex value on the widget: "{widget.hex_input.text()}" does not match the supplied: "{color.name(QColor.NameFormat.HexArgb)}"')

            self.assertEqual(spy.count(), i + 1)  # each iteration should signal only once

    def test_color_picker_widget_hue_slider_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.hue_slider.set_hue(120)  # should make #ff00ff00

        self.assertEqual(spy.count(), 1)  # chaning the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#ff00ff00')

    def test_color_picker_widget_alpha_slider_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.a_slider.set_value(0)  # should make #00ff0000

        self.assertEqual(spy.count(), 1)  # changing the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#00ff0000')

    def test_color_picker_widget_alpha_input_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.a_input.setValue(0)  # should make #00ff0000

        self.assertEqual(spy.count(), 1)  # changing the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#00ff0000')

    def test_color_picker_widget_red_input_changes_color(self):
        widget = ColorPickerWidget(QColor('#ff00ff00'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.r_input.setValue(255)  # should make #ffffff00

        self.assertEqual(spy.count(), 1)  # changing the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#ffffff00')

    def test_color_picker_widget_green_input_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.g_input.setValue(255)  # should make #ffffff00

        self.assertEqual(spy.count(), 1)  # changing the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#ffffff00')

    def test_color_picker_widget_blue_input_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        spy = QSignalSpy(widget.Color_Changed)

        widget.b_input.setValue(255)  # should make #ffff00ff

        self.assertEqual(spy.count(), 1)  # changing the hue changes the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#ffff00ff')

    def test_color_picker_widget_hex_input_changes_color(self):
        widget = ColorPickerWidget(QColor('#ffff0000'))
        other_widget = QWidget()
        spy = QSignalSpy(widget.Color_Changed)

        widget.hex_input.setFocus()
        widget.hex_input.setText('')  # clear out the entry box
        QTest.keyClicks(widget.hex_input, '#aabbccdd')  # mock user types the new hex code
        QTest.keyClick(widget.hex_input, Qt.Key.Key_Return)  # mock user hits enter to trigger the editingFinished event

        self.assertEqual(spy.count(), 1)  # ensure we changed the color
        self.assertEqual(widget.color.name(QColor.NameFormat.HexArgb), '#aabbccdd')  # ensure it changed to the right one