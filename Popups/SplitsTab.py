from __future__ import annotations

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

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(25, 25)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignHCenter)

        self.import_splits(self.game_settings)  # TODO: This needs to be in a scroll container or it can just get huge

        self.layout.addStretch()  # add in a stretch for good measure
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

        # make our connections now that everything is displayed
        self.add_button.clicked.connect(self.addEmptySplit)

    def import_splits(self, game_settings):
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
            new_split = SplitLine(curr['split_name'], curr['pb_time_ms'], curr['pb_segment_ms'], curr['gold_segment_ms'], parent=self)

            currCount = self.layout.count() - 1  # -1 for the add button

            self.layout.insertWidget(currCount, new_split)

    def exportSplits(self):
        """
        Using the data on the screen, create the standard split format for passing to anything that cares

        Returns:
            (list[dict]) the JSON for these splits
        """
        return [sp.export() for sp in self.split_widgets]

    def addEmptySplit(self):
        """
        Adds a blank split for the user to fill out
        """
        newSplit = SplitLine("", 0, 0, 0, parent=self)

        count = self.layout.count() - 1  # -1 for the add button

        self.layout.insertWidget(count - 1, newSplit)  # insert the new split before the add button

    def remove_split(self, split: SplitLine):
        """
        Removes the given split from the splits

        Args:
            split: (SplitLine) The actual split that we want to remove from the list
        """
        self.layout.removeWidget(split)  # removes the widget from the layout so the layout can work around it
        split.deleteLater()  # delete later actually deletes the widget

    def apply(self):
        """
        Creates the splits as they need to be sent out, and then applies it on the main window

        Returns:
            TODO: figure out how the update are applied
        """
        data = self.exportSplits()

        self.main.splits.load_splits(data)


class SplitLine(QFrame):
    def __init__(self, splitName, bestTimeMs, bestTimeSegmentMs, goldTimeSegmentMs, parent: SplitsTab = None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.bestTimeMs = bestTimeMs
        self.goldTimeSegmentMs = goldTimeSegmentMs

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
        self.goldSegmentInput.setTime(ms_to_qtime(goldTimeSegmentMs))
        self.goldSegmentInput.setFixedSize(100, 25)

        self.removeButton = QPushButton("-")
        self.removeButton.setFixedSize(25, 25)

        # add them all in one block
        self.layout.addWidget(self.splitNameInput)
        self.layout.addWidget(self.bestTimeInput)
        self.layout.addWidget(self.bestSegmentInput)
        self.layout.addWidget(self.goldSegmentInput)
        self.layout.addWidget(self.removeButton)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

        self.removeButton.clicked.connect(lambda: parent.remove_split(self))  # must lambda to pass parameters to the method

    def export(self):
        """
        Turn this split object into a single bit of JSON as a dictionary

        Returns:
            (dict): The split data as a dictionary
        """
        return {
            'split_name': self.splitNameInput.text(),
            'pb_time_ms': qtime_to_ms(self.bestTimeInput.time()),
            'gold_segment_ms': qtime_to_ms(self.goldSegmentInput.time()),
            'pb_segment_ms': qtime_to_ms(self.bestSegmentInput.time())
        }
