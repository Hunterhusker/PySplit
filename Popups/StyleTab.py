from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QFrame, QWidget, QLineEdit
from PySide6.QtCore import Slot, Signal, Qt
import copy

from Listeners.ABCListener import ABCListener
from Listeners.KeyboardListener import key_to_str

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main


class StyleTab(QWidget):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)

        self.var_map = mainWindow.configurator.style.variable_map

        self.layout = QVBoxLayout()

        self.inputs = []

        for k, v in self.var_map.items():
            tmp = StyleSettingLine(k, v)

            self.inputs.append(tmp)
            self.layout.addWidget(tmp)

        self.layout.addStretch()

        self.setLayout(self.layout)


class StyleSettingLine(QFrame):
    def __init__(self, label: str, value: str):
        super().__init__()

        self.layout = QHBoxLayout()  # like the key lines we want a label and then a value

        self.label = QLabel(label, self)
        self.label.setObjectName('KeyAssignmentLabel')

        self.textInput = QLineEdit()
        self.textInput.setText(value)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textInput)

        self.setLayout(self.layout)
        self.setObjectName('KeyReassignmentLine')

        # hook up the signals to our input
        self.textInput.editingFinished.connect(self.textChanged)

    @Slot()
    def textChanged(self):
        print(f'lineEditText: {self.textInput.text()}')

