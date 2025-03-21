from PySide6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Slot, Signal
from Widgets.SingleSplitWidget import SingleSplitWidget


class SplitsWidget(QWidget):
    """
    Assembler Widget that holds a list of all the splits we have in the run and listens to the controller for input
    """
    SplitControlSignal = Signal(str)
    SplitFinish = Signal()
    SplitReset = Signal()

    def __init__(self, json: str):
        super().__init__()

        # some basic layout setup to keep stuff off the top and bottom but not the sides
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # we'll want to keep track of these
        self.splits = []
        self.index = 0  # a way to keep place in our list
        self.curr_time = 0.0

        # add in some bools to track state of the splits
        self.started = False
        self.done = False

        self.load_splits(json)

        # add those to the layout
        for split in self.splits:
            self.layout.addWidget(split)

        self.setLayout(self.layout)

    def get_current_split(self):
        return self.splits[self.index]

    @Slot(int)
    def increment_split(self, inc: int):
        self.index += inc

        if self.index >= len(self.splits):  # don't let it leave the array
            self.index = len(self.splits) - 1

        return self.splits[self.index]

    @Slot(int)
    def decrement_split(self, inc: int):
        self.index -= inc

        if self.index < 0:  # don't let it leave the array
            self.index = 0

        return self.splits[self.index]

    @Slot(int)
    def update_split(self, curr_time: int):
        self.curr_time = curr_time

        if self.started:
            self.splits[self.index].update_split(curr_time)

    @Slot(str)
    def handle_control(self, event: str):
        current_split = self.get_current_split()

        # pass the control on to the split itself
        current_split.handle_control(str)

        if event == 'STARTSPLIT':  # if we are splitting, then we ought to move on to the next one
            self.splits[self.index].handle_control(event)

            if not self.started and not self.done:
                self.index = 0

                self.started = True
                self.done = False

            elif not self.started and self.done:
                self.index = 0

                self.started = True
                self.done = False

            elif not self.done:
                if self.index == len(self.splits) - 1:
                    self.SplitFinish.emit()

                    for sp in self.splits:
                        sp.finalize_split()

                    # maintain state
                    self.started = False
                    self.done = True

                else:
                    self.increment_split(1)

        elif event == 'RESET':
            self.index = 0
            self.started = False
            self.done = False

            for sp in self.splits:
                sp.reset_split()

        elif event == 'STOP':
            self.index = 0
            self.started = False
            self.done = False

            for sp in self.splits:
                sp.finalize_split()

    def export_splits(self):
        pass

    def load_splits(self, json: str):
        # create the splits
        split1 = SingleSplitWidget('test1', 1230, 1230)
        split2 = SingleSplitWidget('test2', 3330, 3330)
        split3 = SingleSplitWidget('test3', 5550, 5550)
        split4 = SingleSplitWidget('test4', 8880, 8880)

        # add them to the list
        self.splits.append(split1)
        self.splits.append(split2)
        self.splits.append(split3)
        self.splits.append(split4)

    def reset_splits(self):
        self.index = 0
        self.started = False
        self.done = False

        for sp in self.splits:
            sp.reset_split()

    def update_splits(self):
        """
        Update the splits to ensure they stay up to date as to the best times vs. current times
        """
        self.index = 0
        self.started = False
        self.done = False

        # for each split, if the current time is better than the best, reset it
        for sp in self.splits:
            if sp.current_time_ms < sp.best_time_ms:
                sp.best_time_ms = sp.current_time_ms

            if sp.current_time_ms < sp.pb_time_ms:
                sp.pb_time_ms = sp.current_time_ms

            sp.reset_split()
