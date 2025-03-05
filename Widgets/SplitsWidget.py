from PySide6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Slot, Signal
from Widgets.SingleSplitWidget import SingleSplitWidget


class SplitsWidget(QWidget):
    """
    Assembler Widget that holds a list of all the splits we have in the run and listens to the controller for input
    """
    def __init__(self):
        super().__init__()

        # some basic layout setup to keep stuff off the top and bottom but not the sides
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # we'll want to keep track of these
        self.splits = []
        self.index = 0  # a way to keep place in our list

        # create the splits
        split1 = SingleSplitWidget('test split', 123, 456)
        split2 = SingleSplitWidget('test split', 123, 456)

        # add them to the list
        self.splits.append(split1)
        self.splits.append(split2)

        # add those to the layout
        for split in self.splits:
            self.layout.addWidget(split)

        self.setLayout(self.layout)

    def get_current_split(self):
        return self.splits[self.index]

    @Slot(int)
    def increment_split(self, inc: int):
        self.index += inc

        return self.splits[self.index]

    @Slot(int)
    def decrement_split(self, inc: int):
        # TODO: I think 0 out the time on the "curr" split before changing curr down one and updating there?

        self.index -= inc

        return self.splits[self.index]

    @Slot(int)
    def update_split(self, curr_time: int):
        return self.splits[self.index].update_split(curr_time)
