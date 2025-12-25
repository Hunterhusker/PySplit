import re
from PySide6.QtGui import QColor, QIcon, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSizePolicy, QTimeEdit, QColorDialog, \
    QFontComboBox, QPushButton, QFileDialog, QStyle, QDoubleSpinBox
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

    def setText(self, text: str):
        self.input.setText(text)

    def getText(self):
        return self.input.text()


class LabeledSpinBox(QFrame):
    def __init__(self, label: str, original_value: int, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.label.setMinimumWidth(125)
        self.label.setFixedHeight(25)
        self.label.setObjectName('SettingsLabel')

        self.input = NoScrollQSpinBox()
        self.input.setFixedWidth(205)
        self.input.setFixedHeight(25)
        self.input.setValue(original_value)
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.input, stretch=1)
        self.layout.setContentsMargins(8, 0, 8, 0)

        self.setMinimumHeight(40)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')


class NoScrollQSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()  # prevent scroll changes


class LabeledDoubleSpinBox(QFrame):
    def __init__(self, label: str, original_value: int, decimals: int, step: float, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.label.setMinimumWidth(125)
        self.label.setFixedHeight(25)
        self.label.setObjectName('SettingsLabel')

        self.input = NoScrollQDoubleSpinBox()
        self.input.setMinimumWidth(225)
        self.input.setFixedHeight(25)
        self.input.setValue(original_value)
        self.input.setDecimals(decimals)
        self.input.setSingleStep(step)
        self.input.setMinimum(-9999)  # wish I did not have to set a minimum for this, try and find a way plz
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.label, stretch=1)
        self.layout.addWidget(self.input, stretch=1)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')


class NoScrollQDoubleSpinBox(QDoubleSpinBox):
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
    # TODO : This should start using our own custom color picker
    def __init__(self, label: str, color: QColor, parent):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)
        self.layout.setSpacing(5)

        self.label = QLabel(label)

        self.color = color
        self.color_name = color.name(QColor.HexArgb)

        self.hex_entry = QLineEdit()
        self.hex_entry.setFixedSize(175, 25)
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

            self.color_preview.setStyleSheet(f"background-color: {self.color_name}; border-radius: 2; border: 1px solid #616769;")

    def set_color(self, hex_code: str):
        if hex_code is not None and hex_code != '' and hex_code != '#':  # if there is something to select
            hex_code = hex_code.strip('#')

            color = QColor.fromRgba(int(hex_code, 16))

            if color.isValid():
                self.color = color
                self.color_name = color.name(QColor.HexArgb)

                self.color_preview.setStyleSheet(f"background-color: {self.color_name}; border-radius: 2; border: 1px solid #616769;")

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
        self.font_combobox.setFixedWidth(150)
        if font_family != '':
            self.font_combobox.setCurrentText(font_family)
        else:
            self.font_combobox.setCurrentText(self.font().family())
        self.layout.addWidget(self.font_combobox)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

    def get_font(self) -> QFont:
        return self.font_combobox.currentFont()

    def set_font(self, font: QFont):
        self.font_combobox.setCurrentFont(QFont)

    def get_font_family(self) -> str:
        return self.get_font().family()

    def set_font_family(self, font_family: str):
        tmp = self.get_font()
        tmp.setFamily(font_family)

        self.set_font(tmp)

    def get_size(self) -> int:
        return self.size_spinner.value()

    def set_size(self, size: int):
        self.size_spinner.setValue(size)


class FileDialogOpener(QFrame):
    def __init__(self, label: str, file_path: str = 'none', file_filter=''):
        super().__init__()

        self.file_path = file_path
        self.file_filter = file_filter

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.layout.addStretch()

        self.file_path_label = QLineEdit(file_path if len(file_path) != 0 else 'none')
        self.file_path_label.setReadOnly(True)
        self.file_path_label.setFixedSize(145, 25)
        self.layout.addWidget(self.file_path_label)

        self.open_dialog_button = QPushButton()
        self.open_dialog_button.setIcon(QIcon(':/icons/Static/file_open.svg'))
        self.open_dialog_button.clicked.connect(self.open_file_click)
        self.open_dialog_button.setFixedSize(25, 25)
        self.layout.addWidget(self.open_dialog_button)

        self.clear_button = QPushButton()
        self.clear_button.setIcon(QIcon(':/icons/Static/delete.svg'))
        self.clear_button.setFixedSize(25, 25)
        self.clear_button.clicked.connect(self.clear_file_click)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

    def open_file_click(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Open File')
        file_dialog.setNameFilter(self.file_filter)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]

            self.file_path = file_path
            self.file_path_label.setText(file_path)

    def set_file_path(self, file_path: str):
        if 'url("' in file_path:
            match = re.search(r'url\("([^"]+)"\)', file_path)

            if match:
                file_path = match.group(1)

        self.file_path_label.setText(file_path)
        self.file_path = file_path

    def clear_file_click(self):
        self.file_path = 'none'

        self.file_path_label.setText(self.file_path)
