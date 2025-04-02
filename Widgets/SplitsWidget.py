from PySide6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtCore import Slot, Signal, Qt
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

        self.visible_splits = 3

        # some basic layout setup to keep stuff off the top and bottom but not the sides
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # create the widget we would like to be able to scroll on
        self.scrollWidget = QWidget()
        self.scrollWidgetLayout = QVBoxLayout()
        self.scrollWidgetLayout.setSpacing(2)
        self.scrollWidgetLayout.setContentsMargins(0, 2, 0, 2)

        # create the internal scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setFrameStyle(QFrame.NoFrame)

        # we'll want to keep track of these
        self.splits = []
        self.index = 0  # a way to keep place in our list
        self.curr_time = 0.0

        # add in some bools to track state of the splits
        self.started = False
        self.done = False

        self.load_splits(json)

        # add the splits to the
        for split in self.splits:
            self.scrollWidgetLayout.addWidget(split)

        self.scrollWidget.setLayout(self.scrollWidgetLayout)

        self.scrollArea.setWidget(self.scrollWidget)
        self.setFixedHeight((self.splits[0].height() + 2) * self.visible_splits + 2)

        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)

    def get_current_split(self):
        return self.splits[self.index]

    @Slot(int)
    def increment_split(self, inc: int):
        curr_time = self.splits[self.index].current_time_ms

        self.index += inc

        self.splits[self.index].current_start_time = curr_time

        if self.index >= self.visible_splits:
            sb = self.scrollArea.verticalScrollBar()  # doing this will allow us to scroll to the next widget
            sb.setValue((self.splits[self.index].height() + 2) * self.index + 2)

        if self.index >= len(self.splits):  # don't let it leave the array
            self.index = len(self.splits) - 1

        return self.splits[self.index]

    @Slot(int)
    def decrement_split(self, inc: int):
        self.index -= inc
        sb = self.scrollArea.verticalScrollBar()  # doing this will allow us to scroll to the next widget
        sb.setValue((self.splits[self.index].height() + 2) * self.index + 2)

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

            if not self.started:
                self.index = 0
                sb = self.scrollArea.verticalScrollBar()
                sb.setValue(0)

                if self.done:
                    for sp in self.splits:
                        sp.delta_label.setText('')
                        sp.delta_label.setStyleSheet('color: #bbbbbb;')
                        sp.time_label.setStyleSheet('color: #bbbbbb;')

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

        elif event == 'UNSPLIT' and self.started and not self.done:
            if self.index != 0:
                self.decrement_split(1)
                sp = self.splits[self.index + 1]

                sp.current_time_ms = 0

                sp.delta_label.setText('')
                sp.delta_label.setStyleSheet('color: #bbbbbb;')
                sp.time_label.setStyleSheet('color: #bbbbbb;')

                self.splits[self.index].time_label.setStyleSheet('color: #bbbbbb;')

        elif event == 'RESET':
            self.index = 0
            self.started = False
            self.done = False

            sb = self.scrollArea.verticalScrollBar()
            sb.setValue(0)

            for sp in self.splits:
                sp.reset_split()

        elif event == 'STOP':
            self.index = 0
            self.started = False
            self.done = False

            for sp in self.splits:
                sp.finalize_split()

    def export_splits(self, indent: str = '    ', depth: int = 0):
        tmp = f'{indent * depth}"splits": [\n'

        for i in range(len(self.splits)):
            tmp += self.splits[i].export_data(indent=indent, depth=depth + 1)

            if i != len(self.splits) - 1:  # if not the last split, add a comma
                tmp += ',\n'

        return tmp + f'\n{indent * depth}],\n'

    def load_splits(self, json: str):
        # create the splits
        split1 = SingleSplitWidget('test1', 1230, 2230, 1230, 2230, True)
        split2 = SingleSplitWidget('test2', 3330, 3630, 3330 - 2230, 3630 - 2230, True)
        split3 = SingleSplitWidget('test3', 5550, 6650, 5550 - 3330, 6650 - 3630, True)
        split4 = SingleSplitWidget('test4', 8880, 8880, 8880 - 5550, 8880 - 6650, True)

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
            if sp.current_time_ms < sp.gold_time_ms:
                sp.gold_time_ms = sp.current_time_ms

            if sp.current_time_ms < sp.pb_time_ms:
                sp.pb_time_ms = sp.current_time_ms

            sp.reset_split()
