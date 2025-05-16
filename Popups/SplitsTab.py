from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea, QTimeEdit, QPushButton
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
        self.main = mainWindow

        self.splits = mainWindow.splits

        self.splitWidgets = []
        self.splitWidgets.append(SplitLine("test split", 0, 0, self))
        self.splitWidgets.append(SplitLine("test split", 0, 0, self))

        for sp in self.splitWidgets:
            self.layout.addWidget(sp)

        self.addButton = QPushButton("+")
        self.addButton.setFixedSize(25, 25)
        self.layout.addWidget(self.addButton, alignment=Qt.AlignHCenter)

        self.layout.addStretch()  # add in a stretch for good measure
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

        # make our connections now that everything is displayed
        self.addButton.clicked.connect(self.addEmptySplit)

    def importSplits(self, json):
        """
        Generates a set of splits from the information in the main window

        Args:
            json: (str) the JSON string that represents the splits for this game

        Returns:
            (list[SplitLine]): the list of the splits to put on the screen
        """
        pass

    def exportSplits(self):
        """
        Using the data on the screen, create the standard split format for passing to anything that cares

        Returns:
            (str) the JSON string for these splits
        """
        pass

    def addEmptySplit(self):
        """
        Adds a blank split for the user to fill out
        """
        newSplit = SplitLine("", 0, 0, self)

        count = len(self.splitWidgets)  # since this widget contains only split lines and then an add button count is the next index to insert at

        self.splitWidgets.append(newSplit)
        self.layout.insertWidget(count, newSplit)  # insert the new split before the add button

    def apply(self):
        """
        Creates the splits as they need to be sent out, and then applies it on the main window

        Returns:
            TODO: figure out how the update are applied
        """
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
