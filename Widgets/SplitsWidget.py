from Models.Game import Game, SplitDefinition
from PySide6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QScrollArea
from PySide6.QtCore import Slot, Signal, Qt

from Styling.Settings import Settings
from Timer.SplitTimer import SplitTimer
from Widgets.SingleSplitWidget import SingleSplitWidget


class SplitsWidget(QWidget):
    """
    Assembler Widget that holds a list of all the splits we have in the run and listens to the controller for input
    """
    def __init__(self, settings: Settings, split_timer: SplitTimer, parent: 'Main'):
        super().__init__()
        self.settings = settings
        self.split_timer = split_timer
        self.split_timer.SplitsReset.connect(self.reset_splits)
        self.split_timer.SplitsFinish.connect(self.finish_splits)
        self.split_timer.SplitSkip.connect(self.skip_current_split)

        self.visible_splits = self.settings.settings['visible_splits']
        self.main = parent

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

        self.last_index = None

        # load the splits in from the settings
        self.load_splits(self.settings.game)

        self.scroll_widget.setLayout(self.scroll_widget_layout)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.verticalScrollBar().setSingleStep(self.splits[0].height())

        self.apply_settings()

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def apply_settings(self):
        """
        This method sets the size of the current window
        """
        self.visible_splits = self.settings.settings['visible_splits']
        self.setFixedHeight((self.splits[0].height() + 2) * self.visible_splits + 2)

        for split in self.splits:
            split.apply_settings()

    def get_current_split(self):
        return self.splits[self.index]

    def increment_split(self):
        timer_index = self.split_timer.index

        if timer_index >= self.visible_splits:
            sb = self.scroll_area.verticalScrollBar()  # doing this will allow us to scroll to the next widget
            sb.setValue((self.splits[timer_index].height() + 2) * timer_index + 2)

    def decrement_split(self):
        timer_index = self.split_timer.index

        sb = self.scroll_area.verticalScrollBar()  # doing this will allow us to scroll to the next widget
        sb.setValue((self.splits[timer_index].height() + 2) * timer_index + 2)

    @Slot(int)
    def update_split(self, curr_time: int):
        """
        Update the current split with the current time

        Args:
            curr_time: (int) the current time of the timer in milliseconds
        """
        timer_index = self.split_timer.index
        curr_split = self.splits[timer_index]

        if self.split_timer.started:
            if self.last_index is None:
                self.last_index = 0
                curr_split.set_selected(True)

            elif self.last_index < timer_index:
                last_split = self.splits[self.last_index]
                last_split.end()

                last_split.set_selected(False)
                curr_split.set_selected(True)

                self.increment_split()

                self.last_index = timer_index

            elif self.last_index > timer_index:
                last_split = self.splits[self.last_index]
                last_split.undo()

                last_split.set_selected(False)
                curr_split.set_selected(True)

                self.decrement_split()

                self.splits[timer_index].set_selected(True)

                self.last_index = timer_index

            curr_split.update_split(curr_time)

    @Slot()
    def reset_splits(self):
        self.splits[self.split_timer.index].set_selected(False)

        self.split_timer.index = 0
        self.split_timer.started = False
        self.last_index = None

        sb = self.scroll_area.verticalScrollBar()
        sb.setValue(0)

        for sp in self.splits:
            sp.reset()
            sp.set_selected(False)

    @Slot()
    def finish_splits(self):
        curr_split = self.splits[self.split_timer.index]
        curr_split.end()
        curr_split.set_selected(False)

    @Slot()
    def skip_current_split(self):
        curr_split = self.splits[self.last_index]
        curr_split.skip()

        timer_index = self.split_timer.index

        # make sure the correct split is highlighted
        curr_split.set_selected(False)
        self.splits[timer_index].set_selected(True)

        self.last_index = timer_index

        # manage the scroll
        if timer_index >= self.visible_splits:
            sb = self.scroll_area.verticalScrollBar()  # doing this will allow us to scroll to the next widget
            sb.setValue((self.splits[timer_index].height() + 2) * timer_index + 2)

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

    def load_splits_from_list(self, splits: list[SplitDefinition]):
        """
        Loads in splits form a list of Models.Game.Split
        Args:
            splits: (list[Models.Game.Split]) the list of splits to load into our split widget
        """
        pb_segment_total = 0
        gold_segment_total = 0

        self.remove_all_splits()

        # create the new splits, and add them to the screen
        for i in range(len(splits)):
            split = splits[i]

            pb_segment_total += split.pb_segment_ms
            gold_segment_total += split.gold_segment_ms

            tmp = SingleSplitWidget(split, split_pb_strategy, parent=self)
            tmp.pb_segment_total = pb_segment_total
            tmp.gold_segment_total = gold_segment_total

            self.splits.append(tmp)
            self.scroll_widget_layout.addWidget(tmp)

    def load_splits_from_game(self, game: Game):
        self.load_splits_from_list(game.splits)

    def load_splits_from_json(self, json: dict[str]):
        pb_segment_total = 0
        gold_segment_total = 0

        self.remove_all_splits()

        # create the new splits, and add them to the screen
        for split in json:
            pb_segment_total += split.pb_segment_ms
            gold_segment_total += split.gold_segment_ms

            tmp = SingleSplitWidget(split, split_pb_strategy, parent=self)
            tmp.pb_segment_total = pb_segment_total
            tmp.gold_segment_total = gold_segment_total

            self.splits.append(tmp)
            self.scroll_widget_layout.addWidget(tmp)

    def remove_all_splits(self):
        """
        clear out the splits from the widget
        """
        for split in self.splits:
            self.scroll_widget_layout.removeWidget(split)
            split.setParent(None)
            split.deleteLater()

        self.splits = []

    # def update_splits(self):
    #     """
    #     Update the splits to ensure they stay up to date as to the best times vs. current times
    #     """
    #     self.index = 0
    #     self.started = False
    #     self.done = False
    #
    #     # for each split, if the current time is better than the best, reset it
    #     for sp in self.splits:
    #         if sp.current_time_ms < sp.gold_time_ms:
    #             sp.gold_time_ms = sp.current_time_ms
    #
    #         if sp.current_time_ms < sp.pb_time_ms:
    #             sp.pb_time_ms = sp.current_time_ms
    #
    #         sp.reset_split()


# different split display time strategies
def split_pb_strategy(split: SplitDefinition):
    return split.pb_time_ms


def split_pb_segment_strategy(split: SplitDefinition):
    return split.pb_segment_total_ms


def split_gold_segement_strategy(split: SplitDefinition):
    return split.gold_segment_total_ms
