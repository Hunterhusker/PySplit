from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QTimeEdit, QPushButton, QBoxLayout, QScrollArea, QWidget, QGroupBox
from PySide6.QtCore import Qt
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab
from helpers.TimerFormat import qtime_to_ms, ms_to_qtime
from Models.Game import Game, Split
from Widgets.FormWidgets import LabeledTextEntry, LabeledSpinBox, NoScrollQTimeEdit

if TYPE_CHECKING:
    from Main import Main


class GameSettingsTab(ABCSettingTab):
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

        self.scroll_widget = QWidget()
        self.scroll_widget_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)

        self.splits_group = QGroupBox('Split Data')
        self.splits_group_layout = QVBoxLayout(self.splits_group)
        self.split_area = QVBoxLayout()

        # make the basic labeled inputs
        self.title_group = QGroupBox('Game Information')
        self.title_group_layout = QVBoxLayout(self.title_group)

        self.title_input = LabeledTextEntry("Title: ", self.game.title, parent=self)
        self.title_input.setMinimumHeight(35)

        self.sub_title_input = LabeledTextEntry("Sub-Title: ", self.game.sub_title, parent=self)
        self.sub_title_input.setMinimumHeight(35)

        self.session_attempts_input = LabeledSpinBox('Session Attempts: ', self.game.session_attempts, parent=self)
        self.session_attempts_input.setMinimumHeight(35)

        self.lifetime_attempts_input = LabeledSpinBox('Lifetime Attempts: ', self.game.lifetime_attempts, parent=self)
        self.lifetime_attempts_input.setMinimumHeight(35)

        # populate the title group
        self.title_group_layout.addWidget(self.title_input)
        self.title_group_layout.addWidget(self.sub_title_input)
        self.title_group_layout.addWidget(self.session_attempts_input)
        self.title_group_layout.addWidget(self.lifetime_attempts_input)

        # add everything to the main layout
        self.scroll_widget_layout.addWidget(self.title_group)
        self.splits_group_layout.addLayout(self.split_area)
        self.splits_group_layout.addWidget(self.add_button, alignment=Qt.AlignHCenter)
        self.scroll_widget_layout.addWidget(self.splits_group)

        # import the splits to their layout
        self.import_splits(self.game, self.split_area)

        # add a stretch to keep stuff sized right
        self.scroll_widget_layout.addStretch()

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_widget.setLayout(self.scroll_widget_layout)
        self.layout.addWidget(self.scroll_area)

        # link it all up so that this displays
        self.setLayout(self.layout)
        self.setObjectName('SettingLine')  # set the object name here so it uses the right QSS

        # make our connections now that everything is displayed
        self.add_button.clicked.connect(self.addEmptySplit)

    def import_splits(self, game: Game, container: QBoxLayout):
        """
        Generates a set of splits from the information in the main window

        Args:
            game: (Game) The current game settings
            container: (QBoxLayout) Where to stick the splits once we make them

        Returns:
            (list[SplitLine]): the list of the splits to put on the screen
        """
        for split in game.splits:
            new_split = SplitLine(split, parent=self)
            container.addWidget(new_split)

    def exportSplits(self):
        """
        Using the data on the screen, create the standard split format for passing to anything that cares

        Returns:
            (list[dict]) the JSON for these splits
        """
        return [self.layout.itemAt(i).widget().export() for i in range(self.layout.count() - 2)]

    def addEmptySplit(self):
        """
        Adds a blank split for the user to fill out
        """
        empty_split = Split('', 0, 0, 0, 0, 0)
        newSplit = SplitLine(empty_split, parent=self)
        self.split_area.addWidget(newSplit)

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
        self.game.title = self.title_input.input.text()
        self.game.sub_title = self.sub_title_input.input.text()
        self.game.session_attempts = self.session_attempts_input.input.value()
        self.game.lifetime_attempts = self.lifetime_attempts_input.input.value()

        self.game.splits = []  # make this into an empty list

        # update the splits
        for i in range(self.split_area.count()):
            curr = self.split_area.itemAt(i).widget()

            curr.update_split()
            self.game.splits.append(curr.split)

        self.game.GameUpdated.emit(self.game)


class SplitLine(QFrame):
    def __init__(self, split: Split, parent: GameSettingsTab = None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.split = split

        self.pb_time_ms = split.pb_time_ms
        self.pb_segment_ms = split.pb_segment_ms
        self.gold_segment_ms = split.gold_segment_ms

        self.split_name_input = QLineEdit()
        self.split_name_input.setText(split.split_name)
        self.split_name_input.setBaseSize(125, 25)
        self.split_name_input.setMinimumSize(125, 25)

        self.best_time_input = NoScrollQTimeEdit()
        self.best_time_input.setDisplayFormat('hh:mm:ss.zzz')
        self.best_time_input.setTime(ms_to_qtime(self.pb_time_ms))
        self.best_time_input.setBaseSize(100, 25)
        self.best_time_input.setMinimumSize(100, 25)

        self.best_segment_input = NoScrollQTimeEdit()
        self.best_segment_input.setDisplayFormat('hh:mm:ss.zzz')
        self.best_segment_input.setTime(ms_to_qtime(self.pb_segment_ms))
        self.best_segment_input.setBaseSize(100, 25)
        self.best_segment_input.setMinimumSize(100, 25)

        self.gold_segment_input = NoScrollQTimeEdit()
        self.gold_segment_input.setDisplayFormat('hh:mm:ss.zzz')
        self.gold_segment_input.setTime(ms_to_qtime(self.gold_segment_ms))
        self.gold_segment_input.setBaseSize(100, 25)
        self.gold_segment_input.setMinimumSize(100, 25)

        self.remove_button = QPushButton("-")
        self.remove_button.setBaseSize(25, 25)
        self.remove_button.setMinimumSize(25, 25)

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
