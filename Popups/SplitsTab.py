import copy
import json
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea, QTimeEdit, QPushButton
from PySide6.QtCore import Slot, Qt, QTime
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab
from helpers.TimerFormat import qtime_to_ms, ms_to_qtime

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

        # keep a copy of the game settings as our local copy that we can work with without effecting the original
        self.game_settings = copy.deepcopy(mainWindow.configurator.game_settings)
        # TODO: Should this come from the splits object to make sure we have the up to date best times??

        self.splitWidgets = []

        self.addButton = QPushButton("+")
        self.addButton.setFixedSize(25, 25)
        self.layout.addWidget(self.addButton, alignment=Qt.AlignHCenter)

        self.importSplits(self.game_settings)

        self.layout.addStretch()  # add in a stretch for good measure
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

        # make our connections now that everything is displayed
        self.addButton.clicked.connect(self.addEmptySplit)

    def importSplits(self, game_settings):
        """
        Generates a set of splits from the information in the main window

        Args:
            game_settings: (dict) The dictionary of data representing the current game's configuration

        Returns:
            (list[SplitLine]): the list of the splits to put on the screen
        """
        splitDict = game_settings['splits']

        for i in range(len(splitDict)):
            curr = splitDict[i]
            new_split = SplitLine(curr['split_name'], curr['pb_time_ms'], curr['pb_segment_ms'], curr['gold_segment_ms'])

            currCount = len(self.splitWidgets)

            # add it to the list
            self.splitWidgets.append(new_split)

            self.layout.insertWidget(currCount, self.splitWidgets[i])

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
    def __init__(self, splitName, bestTimeMs, bestTimeSegmentMs, goldTimeMs, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.bestTimeMs = bestTimeMs
        self.goldTimeMs = goldTimeMs

        self.splitNameInput = QLineEdit()
        self.splitNameInput.setText(splitName)
        self.splitNameInput.setFixedSize(125, 25)

        self.bestTimeInput = QTimeEdit()
        self.bestTimeInput.setDisplayFormat('hh:mm:ss.zzz')
        self.bestTimeInput.setTime(ms_to_qtime(bestTimeMs))
        self.bestTimeInput.setFixedSize(100, 25)

        self.bestSegmentInput = QTimeEdit()
        self.bestSegmentInput.setDisplayFormat('hh:mm:ss.zzz')
        self.bestSegmentInput.setTime(ms_to_qtime(bestTimeSegmentMs))
        self.bestSegmentInput.setFixedSize(100, 25)

        self.goldSegmentInput = QTimeEdit()
        self.goldSegmentInput.setDisplayFormat('hh:mm:ss.zzz')
        self.goldSegmentInput.setTime(ms_to_qtime(goldTimeMs))
        self.goldSegmentInput.setFixedSize(100, 25)

        # add them all in one block
        self.layout.addWidget(self.splitNameInput)
        self.layout.addWidget(self.bestTimeInput)
        self.layout.addWidget(self.bestSegmentInput)
        self.layout.addWidget(self.goldSegmentInput)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')
