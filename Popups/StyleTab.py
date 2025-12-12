from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab

if TYPE_CHECKING:
    from Main import Main


class StyleTab(ABCSettingTab):
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)

        self.main = mainWindow
        self.var_map = self.main.settings.style.variable_map

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
            tmp = StyleSettingLine(k, v, self)  # pass itself in so the key line can update the parent

            self.inputs.append(tmp)
            self.scrollWidgetLayout.addWidget(tmp)
            tmp.UpdateKey.connect(self.update_key)

        self.scrollWidgetLayout.addStretch()

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollWidget.setLayout(self.scrollWidgetLayout)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

    @Slot(str, str)
    def update_key(self, key: str, value: str = ""):
        self.var_map[key] = value

    def apply(self):
        self.main.settings.style.update_style(var_map=self.var_map)


class StyleSettingLine(QFrame):
    UpdateKey = Signal(str, str)

    def __init__(self, key: str, value: str, parent: StyleTab):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()  # like the key lines we want a label and then a value
        self.parent = parent  # save the parent so we can pass var updates upstream

        self.key = key

        self.label = QLabel(key, self)
        self.label.setObjectName('SettingsLabel')
        self.setFixedHeight(35)

        self.textInput = QLineEdit()
        self.textInput.setText(value)
        self.textInput.setFixedSize(125, 25)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textInput)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.layout.setAlignment(self.textInput, Qt.AlignRight | Qt.AlignVCenter)
        self.layout.setAlignment(self.label, Qt.AlignLeft | Qt.AlignVCenter)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

        # hook up the signals to our input
        self.textInput.editingFinished.connect(self.textChanged)

    @Slot()
    def textChanged(self):
        print(f'lineEditText: {self.textInput.text()}')

        # pass the change up to the parent
        self.UpdateKey.emit(self.key, self.textInput.text())
