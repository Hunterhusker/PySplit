from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab

if TYPE_CHECKING:
    from Main import Main


class StyleTab(ABCSettingTab):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)

        self.var_map = mainWindow.configurator.style.variable_map

        self.layout = QVBoxLayout()

        self.scrollWidget = QWidget()
        self.scrollWidgetLayout = QVBoxLayout()
        self.scrollWidgetLayout.setSpacing(3)
        self.scrollWidgetLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setFrameStyle(QFrame.NoFrame)
        self.scrollArea.setViewportMargins(0, 0, 5, 0)

        self.inputs = []

        for k, v in self.var_map.items():
            tmp = StyleSettingLine(k, v)

            self.inputs.append(tmp)
            self.scrollWidgetLayout.addWidget(tmp)

        self.scrollWidgetLayout.addStretch()

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

    def apply(self):
        pass


class StyleSettingLine(QFrame):
    def __init__(self, label: str, value: str):
        super().__init__()

        self.layout = QHBoxLayout()  # like the key lines we want a label and then a value

        self.label = QLabel(label, self)
        self.label.setObjectName('KeyAssignmentLabel')
        self.setFixedHeight(35)

        self.textInput = QLineEdit()
        self.textInput.setText(value)
        self.textInput.setFixedSize(125, 25)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textInput)

        self.layout.setAlignment(self.textInput, Qt.AlignRight | Qt.AlignVCenter)
        self.layout.setAlignment(self.label, Qt.AlignLeft | Qt.AlignVCenter)

        self.setLayout(self.layout)
        self.setObjectName('KeyReassignmentLine')

        # hook up the signals to our input
        self.textInput.editingFinished.connect(self.textChanged)

    @Slot()
    def textChanged(self):
        print(f'lineEditText: {self.textInput.text()}')

