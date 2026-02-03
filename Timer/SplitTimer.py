from copy import deepcopy
from PySide6.QtCore import Slot, Signal, QObject
from Styling.Settings import Settings

from helpers.TimerFormat import format_wall_clock_from_ms


class SplitTimer(QObject):
    SplitFinish = Signal()
    SplitReset = Signal()
    SplitUpdate = Signal()

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

        self.splits = None # settings.game.splits
        self.index = None  # 0  # start at the first split
        self.started = None

        self.start_times = []
        self.segment_times = []
        self.end_times = []
        self.current_time_ms = 0

        self.reset()  # call the setup method on the settings to put this into a blank state

    def reset(self):
        self.splits = deepcopy(self.settings.game.splits)  # save a copy of the splits that we can safely mutate
        self.index = 0
        self.started = False

        count = len(self.splits)
        self.segment_times = [-1] * count
        self.start_times = [0] * count
        self.end_times = [-1] * count
        self.current_time_ms = self.settings.game.start_offset

    def update_game(self):
        last_split = self.splits[-1]
        final_time = self.end_times[-1]

        is_pb = False
        if final_time < last_split.pb_time_ms:
            is_pb = True

        for i in range(len(self.splits)):
            split = self.splits[i]

            if is_pb:
                split.pb_time_ms = self.end_times[i]
                split.pb_segment_ms = self.segment_times[i]

            if self.segment_times[i] < split.gold_segment_ms:
                split.gold_segment_ms = self.segment_times[i]

        #self.settings.game.splits = deepcopy(self.splits)  # turned off for now

    @Slot(int)
    def on_tick(self, curr_time_ms):
        if curr_time_ms < 0:
            segment_time = 0
        else:
            segment_time = curr_time_ms - self.start_times[self.index]

        self.segment_times[self.index] = segment_time

        self.current_time_ms = curr_time_ms

    @Slot(str)
    def handle_control(self, event: str):
        match event:
            case 'STARTSPLIT':
                if not self.started:  # if not started, then start the splits
                    self.started = True

                if self.current_time_ms < 0:  # ignore everything before we reach 0
                    return

                # always set the end time no matter if we're at the end or not
                self.end_times[self.index] = self.current_time_ms

                print(self.index, format_wall_clock_from_ms(self.end_times[self.index]), format_wall_clock_from_ms(self.segment_times[self.index]))

                if self.index == len(self.splits) - 1:  # if we are incrementing past the last split actually finish
                    self.started = False  # finish the splits
                    self.SplitFinish.emit()  # notify subscribers we finished
                    return

                self.index += 1  # if we get here we can increment
                self.start_times[self.index] = self.current_time_ms  # and we should save the start of this split here
                return

            case 'UNSPLIT':
                if self.index != 0 and self.started:
                    self.start_times[self.index] = -1
                    self.end_times[self.index - 1] = -1
                    self.index -= 1

            case 'RESET':
                self.reset()
                self.SplitReset.emit()

            case 'STOP':
                self.reset()

            case 'SKIP':
                self.end_times[self.index] = -1
                self.segment_times[self.index] = -1
                self.index += 1
