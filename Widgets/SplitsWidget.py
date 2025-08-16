"""

"""
from Models.Game import Game, Split
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

    # TODO : Add better support for the strategy adoption
    def __init__(self, game: Game):
        super().__init__()

        self.visible_splits = 3

        # some basic layout setup to keep stuff off the top and bottom but not the sides
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # create the widget we would like to be able to scroll on
        self.scroll_widget = QWidget()
        self.scroll_widget_layout = QVBoxLayout()
        self.scroll_widget_layout.setSpacing(2)
        self.scroll_widget_layout.setContentsMargins(0, 2, 0, 2)

        # create the internal scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)

        # we'll want to keep track of these
        self.splits = []
        self.index = 0  # a way to keep place in our list
        self.curr_time = 0.0

        # add in some bools to track state of the splits
        self.started = False
        self.done = False

        # save the game so we can apply updates to it later
        self.game = game
        self.load_splits(game)

        self.scroll_widget.setLayout(self.scroll_widget_layout)

        self.scroll_area.setWidget(self.scroll_widget)
        self.setFixedHeight((self.splits[0].height() + 2) * self.visible_splits + 2)
        self.scroll_area.verticalScrollBar().setSingleStep(self.splits[0].height())

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def get_current_split(self):
        return self.splits[self.index]

    @Slot(int)
    def increment_split(self, inc: int):
        """
        Go to the next (or more) split(s) and return it

        Args:
            inc: (int) the number of splits to increment by

        Returns:
            (SingleSplitWidget): The split that is currently active
        """
        curr_time = self.splits[self.index].current_time_ms

        self.index += inc

        self.splits[self.index].current_start_time = curr_time

        if self.index >= self.visible_splits:
            sb = self.scroll_area.verticalScrollBar()  # doing this will allow us to scroll to the next widget
            sb.setValue((self.splits[self.index].height() + 2) * self.index + 2)

        if self.index >= len(self.splits):  # don't let it leave the array
            self.index = len(self.splits) - 1

        return self.splits[self.index]

    @Slot(int)
    def decrement_split(self, inc: int):
        """
        Go back a (or more) split(s) and return it

        Args:
            inc: (int) the number of splits to decrement, if it goes negative, hard stop at 0

        Returns:
            (SingleSplitWidget): The split that is currently active
        """
        self.index -= inc
        sb = self.scroll_area.verticalScrollBar()  # doing this will allow us to scroll to the next widget
        sb.setValue((self.splits[self.index].height() + 2) * self.index + 2)

        if self.index < 0:  # don't let it leave the array
            self.index = 0

        return self.splits[self.index]

    @Slot(int)
    def update_split(self, curr_time: int):
        """
        Update the current split with the current time

        Args:
            curr_time: (int) the current time of the timer in milliseconds
        """
        self.curr_time = curr_time

        if self.started:
            self.splits[self.index].update_split(curr_time)

    @Slot(str)
    def handle_control(self, event: str):
        """
        An event handler to send all the needed data to the splits themselves

        Args:
            event: (str) the event to handle from the user
        """
        current_split = self.get_current_split()

        # pass the control on to the split itself
        current_split.handle_control(str)

        if event == 'STARTSPLIT':  # if we are splitting, then we ought to move on to the next one
            self.splits[self.index].handle_control(event)

            if not self.started:
                self.index = 0
                sb = self.scroll_area.verticalScrollBar()
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
                    did_pb = self.splits[-1].split.pb_time_ms < self.splits[-1].current_time_ms

                    for sp in self.splits:
                        if did_pb:
                            sp.split.pb_time_ms = sp.current_time_ms
                            sp.split.pb_segment_ms = sp.current_segment_ms

                        if sp.current_segment_ms < sp.split.gold_segment_ms:
                            sp.split.gold_segment_ms = sp.current_segment_ms

                        sp.current_time_ms = 0
                        sp.current_segment_ms = 0

                    # maintain state
                    self.started = False
                    self.done = True

                    self.SplitFinish.emit()

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

            sb = self.scroll_area.verticalScrollBar()
            sb.setValue(0)

            for sp in self.splits:
                sp.reset_split()

        elif event == 'STOP':
            self.index = 0
            self.started = False
            self.done = False

            for sp in self.splits:
                # sp.finalize_split()
                if sp.current_segment_ms != 0 and sp.current_segment_ms < sp.split.gold_segment_ms:
                    sp.split.gold_segment_ms = sp.current_segment_ms

                sp.current_segment_ms = 0
                sp.gold_segment_ms = 0

    def export_splits(self, indent: str = '    ', depth: int = 0) -> str:
        """
        Exports the split data as a JSON string representing the current splits

        Args:
            indent: (str, optional) the indentation to increment for each level of nesting
            depth: (str, optional) the number of indents to apply to the string

        Returns:
            (str) the string representing the splits and their configuration
        """
        tmp = f'{{\n{indent * (depth + 1)}"splits": [\n'

        for i in range(len(self.splits)):
            tmp += self.splits[i].export_data(indent=indent, depth=depth + 2)

            if i != len(self.splits) - 1:  # if not the last split, add a comma
                tmp += ',\n'

        return tmp + f'\n{indent * (depth + 1)}]\n}}'

    def load_splits(self, game: Game):
        """
        Load the splits into the GUI from JSONish data

        Args:
            game: (Models.Game) the game object that we are building the GUI from
        """
        self.load_splits_from_list(game.splits)

    def load_splits_from_list(self, splits: list[Split]):
        """
        Loads in splits form a list of Models.Game.Split
        Args:
            splits: (list[Models.Game.Split]) the list of splits to load into our split widget
        """
        pb_segment_total = 0
        gold_segment_total = 0

        # clear out the splits from the layout
        for split in self.splits:
            self.scroll_widget_layout.removeWidget(split)

        self.splits = []  # and empty our internal list

        # create the new splits, and add them to the screen
        for i in range(len(splits)):
            split = splits[i]

            pb_segment_total += split.pb_segment_ms
            gold_segment_total += split.gold_segment_ms

            tmp = SingleSplitWidget(split, split_pb_strategy)
            tmp.pb_segment_total = pb_segment_total
            tmp.gold_segment_total = gold_segment_total

            self.splits.append(tmp)
            self.scroll_widget_layout.addWidget(tmp)

    def load_splits_from_json(self, json: dict[str]):
        """

        Args:
            json:

        Returns:

        """
        pb_segment_total = 0
        gold_segment_total = 0

        # clear out the splits from the widget
        for split in self.splits:
            self.scroll_widget_layout.removeWidget(split)
            self.splits.remove(split)

        # create the new splits, and add them to the screen
        for split in json:
            pb_segment_total += split.pb_segment_ms
            gold_segment_total += split.gold_segment_ms

            tmp = SingleSplitWidget(split, split_pb_strategy)
            tmp.pb_segment_total = pb_segment_total
            tmp.gold_segment_total = gold_segment_total

            self.splits.append(tmp)
            self.scroll_widget_layout.addWidget(tmp)

    def reset_splits(self):
        """
        Resets the splits back to an unstarted state
        """
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


# different split display time strategies
def split_pb_strategy(split: Split):
    return split.pb_time_ms


def split_pb_segment_strategy(split: Split):
    return split.pb_segment_total_ms


def split_gold_segement_strategy(split: Split):
    return split.gold_segment_total_ms
