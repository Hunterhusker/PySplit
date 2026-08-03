from copy import deepcopy
from PySide6.QtCore import Slot, Signal, QObject

from Settings.Session import Session


class SplitTimer(QObject):
    SplitSkip = Signal()
    SplitUnsplit = Signal()
    SplitUpdate = Signal(int)  # current milliseconds

    SplitsFinish = Signal()
    SplitsReset = Signal()
    SplitsStop = Signal()
    SplitsStart = Signal()

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

        self.splits = None
        self.index = None  # 0  # start at the first split
        self.started = None
        self.done = None

        self.start_times = []
        self.segment_times = []
        self.end_times = []
        self.current_time_ms = 0

        self.reset()  # call the setup method on the settings to put this into a blank state

    @Slot()
    def reset(self):
        self.splits = self.session.game.splits  # deepcopy(self.session.game.splits)  # save a copy of the splits that we can safely mutate
        self.index = 0
        self.started = False
        self.done = False

        count = len(self.splits)
        self.segment_times = [-1] * count
        self.start_times = [-1] * count
        self.end_times = [-1] * count
        self.current_time_ms = self.session.game.start_offset

    @Slot()
    def game_updated(self):
        self.splits = self.session.game.splits  # deepcopy(self.session.game.splits)
        self.index = 0
        self.started = False
        self.done = False

    # def update_game(self):
    #     last_split = self.splits[-1]
    #     final_time = self.end_times[-1]
    #
    #     is_pb = False
    #     if final_time < last_split.pb_time_ms:
    #         is_pb = True
    #
    #     for i in range(len(self.splits)):
    #         split = self.splits[i]
    #
    #         if is_pb:
    #             split.pb_time_ms = self.end_times[i]
    #             split.pb_segment_ms = self.segment_times[i]
    #
    #         if self.segment_times[i] < split.gold_segment_ms:
    #             split.gold_segment_ms = self.segment_times[i]
    #
    #     # TODO : When to update, probably want to spawn a dialog??
    #     #self.settings.game.splits = deepcopy(self.splits)  # turned off for now

    @Slot(int)
    def on_tick(self, curr_time_ms):
        if curr_time_ms < 0:
            segment_time = 0
        else:
            segment_time = curr_time_ms - self.start_times[self.index]

        if self.index == 0:
            segment_time += int(self.session.game.start_offset * 1000)

        if self.start_times[self.index] == -1:
            self.start_times[self.index] = curr_time_ms

        self.segment_times[self.index] = segment_time
        self.current_time_ms = curr_time_ms
        self.SplitUpdate.emit(curr_time_ms)

    @Slot(str)
    def handle_control(self, event: str):
        match event:
            case 'STARTSPLIT':
                if self.done:
                    return

                if not self.started:  # if not started, then start the splits
                    self.started = True
                    self.done = False

                    self.SplitsStart.emit()
                    return

                if self.current_time_ms <= 0:  # ignore everything before we reach 0
                    return

                # always set the end time no matter if we're at the end or not
                self.end_times[self.index] = self.current_time_ms

                # if not at the beginning, and the previous split's end time was not set, it was skipped, so we cannot know our true end time
                if self.index != 0 and self.end_times[self.index - 1] == -1:
                    self.segment_times[self.index] = -1

                if self.index == len(self.splits) - 1:  # if we are incrementing past the last split actually finish
                    self.started = False  # finish the splits
                    self.done = True
                    self.SplitsFinish.emit()  # notify subscribers we finished
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
                if self.session.settings['ask_on_reset']:
                    # open the popup and ask about saving
                    self.session.open_save_run_dialog()

                self.reset()
                self.SplitsReset.emit()

            case 'STOP':
                if self.started:
                    self.reset()
                    self.SplitsStop.emit()

            case 'SKIP':
                if self.started:
                    self.index += 1  # increment first to try and avoid updates coming in while we skip
                    self.end_times[self.index - 1] = -1
                    self.segment_times[self.index - 1] = -1

                    self.SplitSkip.emit()
