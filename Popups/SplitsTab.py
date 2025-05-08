from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea, QTimeEdit
from PySide6.QtCore import Slot, Qt, QTime
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab
from helpers.TimerFormat import qtime_to_ms

if TYPE_CHECKING:
    from Main import Main


class SplitsTab(ABCSettingTab):
    """
    A tab to CRUD your splits
    """
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        self.layout = QVBoxLayout()

        self.test = SplitLine("test split", 0, 0, self)
        self.layout.addWidget(self.test)

        self.setLayout(self.layout)

    def apply(self):
        print(qtime_to_ms(self.test.bestTimeInput.time()))


class SplitLine(QFrame):
    def __init__(self, splitName, bestTimeMs, goldTimeMs, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.bestTimeMs = bestTimeMs
        self.goldTimeMs = goldTimeMs

        self.splitNameInput = QLineEdit()
        self.splitNameInput.setText(splitName)
        self.splitNameInput.setFixedSize(125, 25)

        self.goldTimeInput = QTimeEdit()
        self.goldTimeInput.setDisplayFormat('hh:mm:ss.zzz')
        self.goldTimeInput.setTime(QTime(0, 0, 0))
        self.goldTimeInput.setFixedSize(125, 25)

        self.bestTimeInput = QTimeEdit()
        self.bestTimeInput.setDisplayFormat('hh:mm:ss.zzz')
        self.bestTimeInput.setTime(QTime(0, 0, 0))
        self.bestTimeInput.setFixedSize(125, 25)

        # add them all in one block
        self.layout.addWidget(self.splitNameInput)
        self.layout.addWidget(self.goldTimeInput)
        self.layout.addWidget(self.bestTimeInput)

        self.setLayout(self.layout)
