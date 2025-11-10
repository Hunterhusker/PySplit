from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QSizePolicy, QTimeEdit, QColorDialog
from PySide6.QtCore import Qt, Signal


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
    def wheelEvent(self, event):
        event.ignore()  # prevent scroll changes


class NoScrollQTimeEdit(QTimeEdit):
    def wheelEvent(self, event):
        event.ignore()  # prevent scroll changes


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

        self.label = QLabel(label)

        self.color = color
        self.color_name = color.name()

        self.hex_entry = QLineEdit()
        self.hex_entry.setFixedHeight(25)
        self.hex_entry.setText(self.color_name)
        self.hex_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.color_preview = ClickableFrame()
        self.color_preview.setFixedSize(20, 20)
        self.color_preview.clicked.connect(self.pick_color)
        self.color_preview.setStyleSheet(f"background-color: {self.color_name};")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.hex_entry)
        self.layout.addWidget(self.color_preview)

        self.setStyleSheet("background-color: #ffffff")

        self.setLayout(self.layout)

    def pick_color(self):
        color = QColorDialog.getColor(self.color, self, "Pick A Color")

        if color.isValid():
            self.color = color
            self.color_name = color.name()

            self.color_preview.setStyleSheet(f"background-color: {self.color_name}")
