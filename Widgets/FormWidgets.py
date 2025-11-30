from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSizePolicy, QTimeEdit, QColorDialog, \
    QFontComboBox, QPushButton, QFileDialog, QStyle
from PySide6.QtCore import Qt, Signal, QTime

from helpers.ColorHelpers import *


class LabeledTextEntry(QFrame):
    def __init__(self, label: str, original_value: str, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.label.setMinimumWidth(125)
        self.label.setFixedHeight(25)
        self.label.setObjectName('SettingsLabel')

        self.input = QLineEdit()
        self.input.setMinimumWidth(225)
        self.input.setFixedHeight(25)
        self.input.setText(original_value)
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.input, stretch=1)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')


class LabeledSpinBox(QFrame):
    def __init__(self, label: str, original_value: int, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.label.setMinimumWidth(125)
        self.label.setFixedHeight(25)
        self.label.setObjectName('SettingsLabel')

        self.input = NoScrollQSpinBox()
        self.input.setMinimumWidth(225)
        self.input.setFixedHeight(25)
        self.input.setValue(original_value)
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.input, stretch=1)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')


class NoScrollQSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()  # prevent scroll changes


class NoScrollQTimeEdit(QTimeEdit):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()  # prevent scroll changes


class NoScrollQFontComboBox(QFontComboBox):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()


class LabeledNoScrollQTimeEdit(QFrame):
    def __init__(self, label: str, time: QTime, parent, timerFormat: str = 'hh:mm:ss.zzz'):
        super().__init__(parent=parent)

        self.timer_start_delay_input = QHBoxLayout()

        self.timer_start_delay_label = QLabel(label)
        self.timer_start_delay_label.setMinimumWidth(125)
        self.timer_start_delay_label.setFixedHeight(25)
        self.timer_start_delay_label.setObjectName('SettingsLabel')

        self.timer_start_delay = NoScrollQTimeEdit()
        self.timer_start_delay.setDisplayFormat(timerFormat)
        self.timer_start_delay.setTime(time)
        self.timer_start_delay.setBaseSize(100, 25)
        self.timer_start_delay.setMinimumSize(100, 25)

        self.timer_start_delay_input.addWidget(self.timer_start_delay_label)
        self.timer_start_delay_input.addWidget(self.timer_start_delay)

        self.setLayout(self.timer_start_delay_input)
        self.setObjectName('SettingLine')


class ClickableFrame(QFrame):
    clicked = Signal()

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ColorPicker(QFrame):
    def __init__(self, label: str, color: QColor, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setSpacing(5)

        self.label = QLabel(label)

        self.color = color
        self.color_name = color.name(QColor.HexArgb)

        self.hex_entry = QLineEdit()
        self.hex_entry.setFixedHeight(25)
        self.hex_entry.setMaximumWidth(150)
        self.hex_entry.setText(self.color_name)
        self.hex_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.hex_entry.textChanged.connect(self.set_color)

        self.color_preview = ClickableFrame()
        self.color_preview.setFixedSize(25, 25)
        self.color_preview.clicked.connect(self.pick_color)
        self.color_preview.setStyleSheet(f"background-color: {self.color_name}; border-radius: 2; border: 1px solid #616769;")

        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.layout.addWidget(self.hex_entry)
        self.layout.addWidget(self.color_preview)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

    def pick_color(self):
        color = QColorDialog.getColor(self.color, self, "Pick A Color")

        if color.isValid():
            self.color = color
            self.color_name = color.name(QColor.HexArgb)

            self.hex_entry.setText(to_full_rgba(self.color_name, argb=True))

            self.color_preview.setStyleSheet(f"background-color: {self.color_name}")

    def set_color(self, hex_code: str):
        if hex_code is not None and hex_code != '' and hex_code != '#':  # if there is something to select
            hex_code = hex_code.strip('#')
            argb_hex_code = to_full_argb(hex_code, rgba=True)

            color = QColor.fromRgba(int(argb_hex_code, 16))

            if color.isValid():
                self.color = color
                self.color_name = color.name(QColor.HexArgb)

                self.color_preview.setStyleSheet(f"background-color: {self.color_name}")

    def get_color(self):
        if isinstance(self.color, QColor):
            return self.color

        else:
            return QColor(self.color_name)


class FontPicker(QFrame):
    def __init__(self, label: str, font_family: str, size: int):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        if isinstance(size, str):
            size = int(size.strip('px'))

        self.size_spinner = NoScrollQSpinBox()
        self.size_spinner.setRange(6, 72)
        self.size_spinner.setValue(size)
        self.size_spinner.setFixedHeight(25)
        self.size_spinner.setFixedWidth(50)
        self.layout.addWidget(self.size_spinner)

        self.font_combobox = NoScrollQFontComboBox()
        self.font_combobox.setFixedHeight(25)
        self.font_combobox.setFixedWidth(125)
        if font_family != '':
            self.font_combobox.setCurrentText(font_family)
        else:
            self.font_combobox.setCurrentText(self.font().family())
        self.layout.addWidget(self.font_combobox)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

    def get_font(self):
        return self.font_combobox.currentFont()

    def get_font_family(self):
        return self.get_font().family()

    def get_size(self):
        return self.size_spinner.value()


class FileDialogOpener(QFrame):
    def __init__(self, label: str, file_path: str = ''):
        super().__init__()

        self.file_path = file_path

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.file_path_label = QLineEdit(file_path if len(file_path) != 0 else '...')
        self.file_path_label.setReadOnly(True)
        self.file_path_label.setFixedSize(250, 25)
        self.layout.addWidget(self.file_path_label)

        self.open_dialog_button = QPushButton('Choose')
        self.open_dialog_button.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.open_dialog_button.clicked.connect(self.on_click)
        self.open_dialog_button.setFixedSize(80, 25)
        self.layout.addWidget(self.open_dialog_button)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

    def on_click(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            self.file_path = file_path
            self.file_path_label.setText(file_path)
