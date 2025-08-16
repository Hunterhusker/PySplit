from __future__ import annotations

import copy
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QTimeEdit, QPushButton
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

import Models.Game
from Popups.ABCSettingTab import ABCSettingTab
from helpers.TimerFormat import qtime_to_ms, ms_to_qtime
from Models.Game import Game, Split

if TYPE_CHECKING:
    from Main import Main


class SplitsTab(ABCSettingTab):
    """
    A tab to CRUD your splits
    """
    def __init__(self, game: Game, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        self.layout = QVBoxLayout()
        self.main = mainWindow

        # keep a copy of the game settings as our local copy that we can work with without effecting the original
        self.game = game

        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(25, 25)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignHCenter)

        self.import_splits(self.game)  # TODO: This needs to be in a scroll container or it can just get huge

        self.layout.addStretch()  # add in a stretch for good measure
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

        # make our connections now that everything is displayed
        self.add_button.clicked.connect(self.addEmptySplit)

    def import_splits(self, game: Game):
        """
        Generates a set of splits from the information in the main window

        Args:
            game: (Game) The current game settings

        Returns:
            (list[SplitLine]): the list of the splits to put on the screen
        """
        for split in game.splits:
            new_split = SplitLine(split, parent=self)

            currCount = self.layout.count() - 1  # -1 for the add button

            self.layout.insertWidget(currCount, new_split)

    def exportSplits(self):
        """
        Using the data on the screen, create the standard split format for passing to anything that cares

        Returns:
            (list[dict]) the JSON for these splits
        """
        #return [sp.export() for sp in self.split_widgets]
        return [self.layout.itemAt(i).widget().export() for i in range(self.layout.count() - 2)]

    def addEmptySplit(self):
        """
        Adds a blank split for the user to fill out
        """
        empty_split = Split('', 0, 0, 0, 0, 0)
        newSplit = SplitLine(empty_split, parent=self)

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
        Send the updates to the game object
        """
        new_splits = []

        for i in range(self.layout.count() - 2):
            curr = self.layout.itemAt(i).widget()

            curr.update_split()
            new_splits.append(curr.split)

        self.main.splits.load_splits_from_list(new_splits)


class SplitLine(QFrame):
    def __init__(self, split: Split, parent: SplitsTab = None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.split = split

        self.pb_time_ms = split.pb_time_ms
        self.pb_segment_ms = split.pb_segment_ms
        self.gold_segment_ms = split.gold_segment_ms

        self.split_name_input = QLineEdit()
        self.split_name_input.setText(split.split_name)
        self.split_name_input.setFixedSize(125, 25)

        self.best_time_input = QTimeEdit()
        self.best_time_input.setDisplayFormat('hh:mm:ss.zzz')
        self.best_time_input.setTime(ms_to_qtime(self.pb_time_ms))
        self.best_time_input.setFixedSize(100, 25)

        self.best_segment_input = QTimeEdit()
        self.best_segment_input.setDisplayFormat('hh:mm:ss.zzz')
        self.best_segment_input.setTime(ms_to_qtime(self.pb_segment_ms))
        self.best_segment_input.setFixedSize(100, 25)

        self.gold_segment_input = QTimeEdit()
        self.gold_segment_input.setDisplayFormat('hh:mm:ss.zzz')
        self.gold_segment_input.setTime(ms_to_qtime(self.gold_segment_ms))
        self.gold_segment_input.setFixedSize(100, 25)

        self.remove_button = QPushButton("-")
        self.remove_button.setFixedSize(25, 25)

        # add them all in one block
        self.layout.addWidget(self.split_name_input)
        self.layout.addWidget(self.best_time_input)
        self.layout.addWidget(self.best_segment_input)
        self.layout.addWidget(self.gold_segment_input)
        self.layout.addWidget(self.remove_button)

        self.setLayout(self.layout)
        self.setObjectName('SettingLine')

        self.remove_button.clicked.connect(lambda: parent.remove_split(self))  # must lambda to pass parameters to the method

    def export(self):
        """
        Turn this split object into a single bit of JSON as a dictionary

        Returns:
            (dict): The split data as a dictionary
        """
        return {
            'split_name': self.split_name_input.text(),
            'pb_time_ms': qtime_to_ms(self.best_time_input.time()),
            'gold_segment_ms': qtime_to_ms(self.gold_segment_input.time()),
            'pb_segment_ms': qtime_to_ms(self.best_segment_input.time())
        }

    def update_split(self):
        self.split.split_name = self.split_name_input.text()
        self.split.pb_time_ms = qtime_to_ms(self.best_time_input.time())
        self.split.gold_segment_ms = qtime_to_ms(self.gold_segment_input.time())
        self.split.pb_segment_ms = qtime_to_ms(self.best_segment_input.time())

    def to_Split(self) -> Models.Game.Split:
        """
        Exports the current SplitLine as the corresponding Models.Game.Split that would make it

        Returns:
            (Models.Game.Split)
        """
        pass