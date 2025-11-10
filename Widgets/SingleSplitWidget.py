"""
This class defines the way that a single split can be displayed on the screen
"""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Property
from PySide6.QtCore import Slot, Signal
from typing import Callable

from helpers.TimerFormat import format_wall_clock_from_ms
from Models.Game import Split


class SingleSplitWidget(QFrame):
    def isSelected(self):
        return self._selected

    def setSelected(self, state: bool):
        if self._selected != state:
            self._selected = state
            self.setProperty("selected", state)

            # Repolish self + children
            def repolish(w):
                w.style().unpolish(w)
                w.style().polish(w)
                for child in w.findChildren(QWidget):
                    child.style().unpolish(child)
                    child.style().polish(child)

            repolish(self)
            self.update()

    selected = Property(bool, isSelected, setSelected)  # hate the formatting here

    def __init__(self, split: Split, comparison_strategy: Callable[[Split], int]):
        """
        An individual split that can display the times from the PB and the comparison time
        Args:
            split: (Split) The split object that contains the information for the split itself
            comparison_strategy: (Callable[[Split], int]) a strategy function that extracts the value we display and compare against from the Split object
        """
        super().__init__()

        self._selected = False

        self.split = split
        self.comparison_strategy = comparison_strategy

        # setup values for the current state of the split
        self.current_time_ms = 0
        self.current_segment_ms = 0
        self.current_start_time = 0

        self.layout = QHBoxLayout()

        # create the labels we need
        self.split_name_label = QLabel(self.split.split_name, self)
        self.time_label = QLabel(format_wall_clock_from_ms(self.get_comparison_time()), self)
        self.delta_label = QLabel('', self)

        # add them to the layout
        self.layout.addWidget(self.split_name_label)
        self.layout.addWidget(self.delta_label)
        self.layout.addWidget(self.time_label)

        # align the items in the layout
        self.layout.setAlignment(self.split_name_label, Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.setAlignment(self.delta_label, Qt.AlignRight)
        self.layout.setAlignment(self.time_label, Qt.AlignRight | Qt.AlignVCenter)

        self.setObjectName('SingleSplit')

        self.setLayout(self.layout)  # set the layout on the frame
        self.setFixedHeight(30)

    @Slot(int)
    def update_split(self, curr_time_ms: int):
        """
        A method to update the current split to represent the current time taken

        Args:
            curr_time_ms: (int) the current amount of time taken up to this point (from start of timer to now, not start of split)
        """
        segment_time = curr_time_ms - self.current_start_time  # get the current change
        self.current_segment_ms = segment_time  # add the current change to the current segment value to get the size of the segment

        self.current_time_ms = curr_time_ms

        time_delta = self.current_time_ms - self.split.pb_time_ms

        if time_delta >= -1000.0:
            time_delta_str = format_wall_clock_from_ms(time_delta)

            if time_delta >= 0:
                time_delta_str = '+' + time_delta_str

            else:
                time_delta_str = '-' + time_delta_str

            self.delta_label.setText(time_delta_str)

            if time_delta <= 0:
                self.delta_label.setStyleSheet('color: green;')
            else:
                self.delta_label.setStyleSheet('color: red;')

        else:
            self.delta_label.setText('')

    def get_comparison_time(self):
        return self.comparison_strategy(self.split)

    def reset_split(self):
        """
        Resets the split data to how it would have been when first loaded
        """
        self.delta_label.setText('')  # clear the time delta
        self.time_label.setText(format_wall_clock_from_ms(self.get_comparison_time()))
        self.time_label.setStyleSheet('color: #bbbbbb')

        self.current_time_ms = 0
        self.current_segment_ms = 0

    def finalize_split(self):
        """
        Saves any golds and pbs and starts the split over
        """
        if self.current_segment_ms < self.split.gold_segment_ms and self.current_time_ms != 0:
            self.split.gold_segment_ms = self.current_segment_ms

        if self.current_time_ms < self.split.pb_time_ms and self.current_time_ms != 0:
            self.split.pb_time_ms = self.current_time_ms

        # make the split show what it should
        self.time_label.setText(format_wall_clock_from_ms(self.get_comparison_time()))

        # reset the current state to 0 since this split is done
        self.current_time_ms = 0
        self.current_segment_ms = 0

    @Slot()
    def export_data(self, indent: str = '    ', depth: int = 1):
        """
        A method to turn the data for this single split into JSON and output it as a dictionary

        Returns:
            (dict[str, any]): A dictionary of this split's data as valid JSON that we can store in a splits file
        """
        # indentation gets weird here due to the multiline string, but it stays a one-liner so whatever
        return f"""{indent * depth}{{
{indent * (depth + 1)}"split_name": "{self.split.split_name}",
{indent * (depth + 1)}"pb_time_ms": {self.split.pb_time_ms},
{indent * (depth + 1)}"pb_segment_ms": {self.split.pb_segment_ms},
{indent * (depth + 1)}"gold_segment_ms": {self.split.gold_segment_ms}
{indent * depth}}}"""

    @Slot(str)
    def handle_control(self, event: str):
        if event == 'STARTSPLIT' and self.current_time_ms != 0:
            time_delta = self.current_time_ms - self.get_comparison_time()
            time_delta_str = format_wall_clock_from_ms(time_delta)

            if time_delta >= 0:
                time_delta_str = '+' + time_delta_str
            else:
                time_delta_str = '-' + time_delta_str

            self.delta_label.setText(time_delta_str)  # update the +/- time delta label
            self.time_label.setText(format_wall_clock_from_ms(self.current_time_ms))  # set the text to show the time taken

            if self.current_segment_ms < self.split.gold_segment_ms:
                # if we're ahead of the saved time, then a "gold" gold
                if self.current_segment_ms < self.split.pb_segment_ms:
                    self.time_label.setStyleSheet('color: gold;')
                    self.delta_label.setStyleSheet('color: gold;')
                else:  # we're behind, but we saved time, then we ought to color it a different color to note the gold but while not ahead
                    self.time_label.setStyleSheet('color: goldenrod;')
                    self.delta_label.setStyleSheet('color: goldenrod;')

            elif self.current_segment_ms < self.split.pb_segment_ms:
                self.time_label.setStyleSheet('color: blue;')
                self.delta_label.setStyleSheet('color: blue;')

            elif self.current_time_ms >= self.split.pb_time_ms:
                self.time_label.setStyleSheet('color: red;')
                self.delta_label.setStyleSheet('color: red;')

            else:
                self.time_label.setStyleSheet('color: green;')
                self.delta_label.setStyleSheet('color: green;')

        elif event == 'RESET':
            self.reset_split()

        elif event == 'STOP':
            self.finalize_split()
