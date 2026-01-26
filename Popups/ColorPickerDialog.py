from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QDialog, QDialogButtonBox, QPushButton
from Widgets.ColorPickerWidget import ColorPickerWidget


class ColorPickerDialog(QDialog):
    def __init__(self, color: QColor = QColor('#ffff0000'), parent=None):
        super().__init__(parent)
        self.dialogButtons = QDialogButtonBox()
        self.dialogButtons.addButton(QDialogButtonBox.Ok)
        self.dialogButtons.addButton(QDialogButtonBox.Cancel)

        for button in self.dialogButtons.buttons():
            button.setFixedSize(80, 25)
            button.setAutoDefault(False)
            button.setDefault(False)

        self.dialogButtons.clicked.connect(self.button_event)

        self.colorPicker = ColorPickerWidget(color=color)
        self.colorPicker.Color_Changed.connect(self.set_color)
        self.color = self.colorPicker.color

        # add stuff here
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.colorPicker)
        self.layout.addWidget(self.dialogButtons)

        self.setLayout(self.layout)
        self.setWindowTitle('Settings')

    def button_event(self, button: QPushButton):
        role = self.dialogButtons.buttonRole(button)

        if role == QDialogButtonBox.AcceptRole:
            print('Accept')
            self.accept()

        else:
            print('Reject')
            self.reject()

    def set_color(self, color: QColor):
        self.color = color
