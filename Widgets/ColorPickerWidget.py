from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QImage, QColor, Qt, QPixmap, QPainter, QPen
from PySide6.QtWidgets import QLabel, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QGroupBox, QLineEdit, \
    QFrame, QSizePolicy, QStackedLayout


class SVImage(QLabel):
    color_changed = Signal(QColor)

    def __init__(self, width: int, height: int, color: QColor = QColor('#ffff0000'), parent=None):
        super().__init__(parent)

        # manage the input params of the widget
        self.width = width
        self.height = height
        self.hue = max(min(color.hue(), 359), 0)
        self.color = color

        # manage the location of the point
        self._marker_pos = QPoint(color.saturation(), 255 - color.value())

        # set up the image on the widget
        self.image = None
        self.generate_sv_image(self.hue, width, height)

        # manage the color data
        self.dragging = False

        self.setFixedSize(width, height)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def set_sv(self, s, v):
        self.setMarker(s, 255 - v)

    def calculate_color(self):
        saturation = max(min(255, self._marker_pos.x()), 0)
        value = 255 - max(min(255, self._marker_pos.y()), 0)
        alpha = self.color.alpha()

        self.color = QColor().fromHsv(self.hue, saturation, value, alpha)

    def mousePressEvent(self, event, /):
        self.calculate_color()
        self.setMarker(event.position().x(), event.position().y())
        self.dragging = True

    def mouseMoveEvent(self, event, /):
        if not self.dragging:
            return

        self.calculate_color()
        self.setMarker(max(min(event.position().x(), self.width), 0), max(min(event.position().y(), self.height), 0))

    def mouseReleaseEvent(self, event, /):
        self.calculate_color()
        self.setMarker(max(min(event.position().x(), self.width), 0), max(min(event.position().y(), self.height), 0))
        self.color_changed.emit(self.color)

        self.dragging = False

    def paintEvent(self, event):
        super().paintEvent(event)

        if self._marker_pos is None:
            return

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.white, 1)
        painter.setPen(pen)
        painter.setBrush(self.color)

        r = 6
        painter.drawEllipse(self._marker_pos, r, r)
        painter.end()

    def setMarker(self, x, y):
        self._marker_pos = QPoint(x, y)
        self.update()

    def generate_sv_image(self, hue: int, w: int = None, h: int = None) -> QImage:
        if w is None:
            w = self.width

        if h is None:
            h = self.height

        self.hue = hue
        self.calculate_color()

        image = QImage(w, h, QImage.Format.Format_RGB32)

        for y in range(h):
            v = 1.0 - (y / (h - 1))
            for x in range(w):
                s = x / (w - 1)
                color = QColor.fromHsv(hue, int(s * 255), int(v * 255))
                image.setPixelColor(x, y, color)

        self.image = image
        self.setPixmap(QPixmap.fromImage(self.image))


class HueSlider(QLabel):
    hue_changed = Signal(float)

    def __init__(self, value: int, bar_width: int, bar_height: int, indicator_width: int, parent=None):
        super().__init__(parent)
        self.value = max(min(value, bar_height), 0)  # set the value to the value capped between 0 and the height
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.indicator_width = indicator_width

        self.hue = None
        self.calculate_hue()
        self.clicked = False

        image = QImage(bar_width, bar_height, QImage.Format.Format_RGB32)
        for y in range(bar_height - 1, -1, -1):
            hue = (y / bar_height) * 360
            color = QColor.fromHsv(hue, 255, 255)
            for x in range(bar_width):
                image.setPixelColor(x, y, color)

        self.image = image
        self.setPixmap(QPixmap.fromImage(self.image))

        self.setFixedSize(max(bar_width, indicator_width) + 2, bar_height + (2 * indicator_width))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def calculate_hue(self) -> float:
        self.hue = int(min(max((self.value / self.bar_height) * 360, 0), 359))
        self.hue_changed.emit(self.hue)

    def set_hue(self, hue):
        self.hue = int(hue)
        self.value = int(min(max((hue / 360) * self.bar_height, 0), 359))
        self.update()

        self.hue_changed.emit(self.hue)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.white, 1)
        painter.setPen(pen)
        painter.setBrush(QColor.fromHsv(min(max(self.hue, 0), 359), 255, 255))

        r = self.indicator_width / 2
        painter.drawEllipse(
            QPoint((max(self.bar_width, self.indicator_width) + 2) // 2, self.value + self.indicator_width), r, r)
        painter.end()

    def mousePressEvent(self, event, /):
        self.clicked = True
        self.value = max(min(event.position().y(), self.bar_height), 0)
        self.calculate_hue()
        self.update()

    def mouseMoveEvent(self, event, /):
        if not self.clicked:
            return

        self.value = max(min(event.position().y(), self.bar_height), 0)
        self.calculate_hue()
        self.update()

    def mouseReleaseEvent(self, event, /):
        self.value = max(min(event.position().y(), self.bar_height), 0)
        self.clicked = False
        self.calculate_hue()
        self.update()


class CustomSlider(QLabel):
    value_changed = Signal(int)

    def __init__(self, value: int, bar_width: int, bar_height: int, indicator_width: int, background_color: QColor,
                 highlight_color: QColor, min_value: int = 0, max_value: int = 100, parent=None):
        super().__init__(parent)

        self.bar_width = bar_width
        self.bar_height = bar_height
        self.indicator_width = indicator_width

        self.background_color = background_color
        self.highlight_color = highlight_color

        self.min_value = min_value
        self.max_value = max_value

        self.y = None
        self.value = None
        self.set_value(value)
        self.clicked = False

        self.image = None
        self.generate_slider_background()
        self.setPixmap(QPixmap.fromImage(self.image))

        self.setFixedSize(max(bar_width, indicator_width) + 2, bar_height + (2 * indicator_width))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def generate_slider_background(self):
        tmp = QImage(self.bar_width, self.bar_height, QImage.Format.Format_RGB32)
        for y in range(self.bar_height):
            for x in range(self.bar_width):
                if y > self.y:
                    tmp.setPixelColor(x, y, self.highlight_color)
                else:
                    tmp.setPixelColor(x, y, self.background_color)

        self.image = tmp
        self.setPixmap(QPixmap.fromImage(self.image))

    def calculate_value(self) -> float:
        # find the min value w/ interpolation but use the min and max just to be sure
        self.value = self.max_value - min(
            max(((self.y * (self.max_value - self.min_value)) / self.bar_height) + self.min_value, self.min_value),
            self.max_value)
        self.value_changed.emit(self.value)

    def set_value(self, value):
        self.value = min(max(value, self.min_value), self.max_value)
        self.y = ((self.max_value - self.value) * self.bar_height) / (self.max_value - self.min_value)
        self.update()

        self.value_changed.emit(self.value)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.white, 1)
        painter.setPen(pen)
        painter.setBrush(QColor(self.highlight_color))

        r = self.indicator_width / 2
        painter.drawEllipse(QPoint((max(self.bar_width, self.indicator_width) + 2) // 2, self.y + self.indicator_width), r, r)
        painter.end()

    def mousePressEvent(self, event, /):
        self.clicked = True
        self.y = max(min(event.position().y(), self.bar_height), 0)
        self.calculate_value()
        self.generate_slider_background()
        self.update()

    def mouseMoveEvent(self, event, /):
        if not self.clicked:
            return

        self.y = max(min(event.position().y(), self.bar_height), 0)
        self.calculate_value()
        self.generate_slider_background()
        self.update()

    def mouseReleaseEvent(self, event, /):
        self.y = max(min(event.position().y(), self.bar_height), 0)
        self.clicked = False
        self.calculate_value()
        self.generate_slider_background()
        self.update()

        self.value_changed.emit(self.value)


class PreviewColorWidget(QWidget):
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)
        self.color = color

        container = QFrame()

        self.layout = QStackedLayout(container)
        self.layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._checker_frame = self.CheckerFrame()
        self._color_frame = QFrame()
        self._color_frame.setAutoFillBackground(False)
        self._color_frame.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.set_color(color)

        self.layout.addWidget(self._checker_frame)
        self.layout.addWidget(self._color_frame)

        self.setLayout(self.layout)

    def set_color(self, color: QColor):
        self.color = color
        self._color_frame.setStyleSheet(f"background-color: \"{self.color.name(QColor.NameFormat.HexArgb)}\"; border: none;")  # border-radius: 2; border: 1px solid #616769;")
        self.update()

    class CheckerFrame(QFrame):
        def __init__(self, size: int = 10, parent=None):
            super().__init__(parent)
            self.size = size
            self.setStyleSheet("border: none;")

        def paintEvent(self, event):
            p = QPainter(self)
            c1 = QColor(200, 200, 200)
            c2 = QColor(240, 240, 240)

            for y in range(0, self.height(), self.size):
                for x in range(0, self.width(), self.size):
                    p.fillRect(
                        x, y, self.size, self.size,
                        c1 if ((x // self.size + y // self.size) % 2 == 0) else c2
                    )


class ColorPickerWidget(QWidget):
    Color_Changed = Signal(QColor)

    def __init__(self, color: QColor = QColor('#ffff0000')):
        super().__init__()
        self.setWindowTitle("Simple Image Viewer")
        self.setWindowFlags(Qt.Window)

        layout = QHBoxLayout()

        self.sv_image = SVImage(255, 255, color=color)
        self.sv_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sv_image.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.sv_image.color_changed.connect(self.set_color)
        self.sv_image.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.hue_slider = HueSlider(color.hue(), 5, 255, 12)
        self.hue_slider.hue_changed.connect(self.hue_changed)
        self.hue_slider.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # (self, value: int, bar_width: int, bar_height: int, indicator_width: int, background_color: QColor, highlight_color: QColor, parent=None):
        self.a_slider = CustomSlider(color.alpha(), 5, 255, 12, QColor('#4c5052'), QColor('#dddddd'), 0, 255)
        self.a_slider.value_changed.connect(self.alpha_changed)

        side_box = QVBoxLayout()

        # create the RGB boxes
        rgb_group = QGroupBox('RGB')
        rgb_box = QHBoxLayout()
        rgb_group.setLayout(rgb_box)

        self.a_input = QSpinBox()
        self.a_input.setRange(0, 255)
        self.a_input.setValue(color.alpha())
        self.a_input.valueChanged.connect(self.rgb_changed)
        self.a_input.setToolTip('Set Alpha Value')

        self.r_input = QSpinBox()
        self.r_input.setRange(0, 255)
        self.r_input.valueChanged.connect(self.rgb_changed)
        self.r_input.setToolTip('Set Red Value')

        self.g_input = QSpinBox()
        self.g_input.setRange(0, 255)
        self.g_input.valueChanged.connect(self.rgb_changed)
        self.g_input.setToolTip('Set Green Value')

        self.b_input = QSpinBox()
        self.b_input.setRange(0, 255)
        self.b_input.valueChanged.connect(self.rgb_changed)
        self.b_input.setToolTip('Set Blue Value')

        rgb_box.addWidget(self.a_input)
        rgb_box.addWidget(self.r_input)
        rgb_box.addWidget(self.g_input)
        rgb_box.addWidget(self.b_input)

        # create the hex input
        hex_group = QGroupBox('HEX')
        hex_box = QHBoxLayout()
        hex_group.setLayout(hex_box)

        self.hex_input = QLineEdit()
        self.hex_input.editingFinished.connect(self.hex_changed)
        self.hex_input.setToolTip('Set ARGB Hex Value')

        hex_box.addWidget(self.hex_input)

        # make a preview box
        self.preview = PreviewColorWidget(color)  # QFrame()
        self.preview.setFixedHeight(115)
        self.preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # build out the side box structure
        side_box.addStretch()
        side_box.addWidget(self.preview)
        side_box.addWidget(rgb_group)
        side_box.addWidget(hex_group)
        side_box.addStretch()

        layout.addWidget(self.sv_image)
        layout.addWidget(self.hue_slider)
        layout.addWidget(self.a_slider)
        layout.addLayout(side_box)

        self.setLayout(layout)
        self.setFixedSize(575, 300)

        self.color = None
        self.set_color(self.sv_image.color)

    def hue_changed(self):
        self.sv_image.generate_sv_image(self.hue_slider.hue)
        self.set_color(self.sv_image.color)

    def alpha_changed(self):
        self.a_input.setValue(self.a_slider.value)  # this triggers the rgb_changed code all on its own

    def rgb_changed(self):
        new_color = QColor(self.r_input.value(), self.g_input.value(), self.b_input.value(), self.a_input.value())
        self.set_color(new_color)

    def hex_changed(self):
        hex_value = int(self.hex_input.text().strip('#'), 16)

        new_color = QColor.fromRgba(hex_value)
        self.set_color(new_color)

    def mousePressEvent(self, event):
        w = QApplication.focusWidget()
        if w:
            w.clearFocus()
        super().mousePressEvent(event)

    def set_color(self, color: QColor):
        # turn off all the signals
        self.r_input.blockSignals(True)
        self.g_input.blockSignals(True)
        self.b_input.blockSignals(True)
        self.hex_input.blockSignals(True)
        self.hue_slider.blockSignals(True)
        self.sv_image.blockSignals(True)
        self.a_input.blockSignals(True)
        self.a_slider.blockSignals(True)

        if self.r_input.value() != color.red() and not self.r_input.hasFocus():
            self.r_input.setValue(color.red())

        if self.g_input.value() != color.green() and not self.g_input.hasFocus():
            self.g_input.setValue(color.green())

        if self.b_input.value() != color.blue() and not self.b_input.hasFocus():
            self.b_input.setValue(color.blue())

        # always update the color to have the alpha value, since the one on the SV image shouldn't have it
        if color.alpha() != self.a_input.value():
            self.a_input.setValue(color.alpha())
            self.a_slider.set_value(color.alpha())

        if self.hex_input.text() != color.name():
            self.hex_input.setText(color.name(QColor.HexArgb))

        if self.hue_slider.hue != color.hue():
            self.hue_slider.set_hue(color.hue())
            self.sv_image.generate_sv_image(min(max(self.hue_slider.hue, 0), 359))

        if self.sv_image.color != color:
            self.sv_image.set_sv(color.saturation(), color.value())

        # turn the signals back on
        self.r_input.blockSignals(False)
        self.g_input.blockSignals(False)
        self.b_input.blockSignals(False)
        self.hex_input.blockSignals(False)
        self.hue_slider.blockSignals(False)
        self.sv_image.blockSignals(False)
        self.a_input.blockSignals(False)
        self.a_slider.blockSignals(False)

        self.preview.set_color(color)
        self.color = color
        self.Color_Changed.emit(color)  # emit the color
