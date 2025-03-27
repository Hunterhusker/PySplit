from PySide6.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot, Signal

from helpers.TimerFormat import format_wall_clock_from_ms


class SingleSplitWidget(QFrame):
    def __init__(self, split_name: str, gold_time_ms: int, pb_time_ms: int, gold_segment_ms: int, pb_segment_ms: int, displayPb: bool):
        """
        An individual split that can display the times from the PB and the comparison  time

        Args:
            split_name: (str) the name of the split
            gold_time_ms: (int) the number of milliseconds from the start that was achieved on the PB for this segment only
            pb_time_ms: (int) the number of milliseconds from the start that was achieved on the overall PB for this game
        """
        super().__init__()

        # save the variables we will need
        self.split_name = split_name

        # track the saved times
        self.gold_time_ms = gold_time_ms
        self.pb_time_ms = pb_time_ms

        # track our best saved segments
        self.gold_segment_ms = gold_segment_ms
        self.pb_segment_ms = pb_segment_ms

        # setup values for the current state of the split
        self.current_time_ms = 0
        self.current_segment_ms = 0
        self.current_start_time = 0

        # whether to display the PB or not
        self.displayPb = displayPb

        if displayPb:
            self.display_time_ms = self.pb_time_ms
        else:
            self.display_time_ms = self.gold_time_ms

        self.layout = QHBoxLayout()

        # create the labels we need
        self.split_name_label = QLabel(split_name, self)
        self.time_label = QLabel(format_wall_clock_from_ms(self.display_time_ms), self)
        self.delta_label = QLabel('', self)

        # add them to the layout
        self.layout.addWidget(self.split_name_label)
        self.layout.addWidget(self.delta_label)
        self.layout.addWidget(self.time_label)

        # align the items in the layout
        self.layout.setAlignment(self.split_name_label, Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.setAlignment(self.delta_label, Qt.AlignRight)
        self.layout.setAlignment(self.time_label, Qt.AlignRight | Qt.AlignVCenter)

        # set this as a little lighter grey so they look nice
        self.setStyleSheet("""
            background-color: #323232;
            color: #bbbbbb;
        """)

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

        time_delta = self.current_time_ms - self.display_time_ms

        if time_delta >= -1000.0 and False:
            time_delta_str = format_wall_clock_from_ms(time_delta)

            if time_delta >= 0:
                time_delta_str = "+" + time_delta_str

            self.delta_label.setText(time_delta_str)

            if time_delta <= 0:
                self.delta_label.setStyleSheet('color: green;')
            else:
                self.delta_label.setStyleSheet('color: red;')

        elif True:
            self.delta_label.setText(format_wall_clock_from_ms(self.current_segment_ms))

        else:
            self.delta_label.setText('')

    def reset_split(self):
        """
        Resets the split data to how it would have been when first loaded
        """
        self.delta_label.setText('')  # clear the time delta
        self.time_label.setText(format_wall_clock_from_ms(self.display_time_ms))
        self.time_label.setStyleSheet('color: #bbbbbb')

        self.current_time_ms = 0
        self.current_segment_ms = 0

    def finalize_split(self):
        """
        Saves any golds and starts the split over
        """
        if self.current_segment_ms < self.gold_segment_ms and self.current_time_ms != 0:
            self.gold_time_ms = self.current_time_ms
            self.gold_segment_ms = self.current_segment_ms
            self.time_label.setText(format_wall_clock_from_ms(self.current_time_ms))

            # reset the current state to 0 since this split is done
            self.current_time_ms = 0
            self.current_segment_ms = 0

    @Slot()
    def export_data(self):
        """
        A method to turn the data for this single split into JSON and output it as a dictionary

        Returns:
            (dict[str, any]): A dictionary of this split's data as valid JSON that we can store in a splits file
        """
        return f"""{{
            "split_name": "{self.split_name}",
            "pb_time_ms": {self.pb_time_ms},
            "gold_time_ms": {self.gold_time_ms},
            "pb_segment_ms": {self.pb_segment_ms},
            "gold_segment_ms": {self.gold_segment_ms}
        }}"""

    @Slot(str)
    def handle_control(self, event: str):
        if event == 'STARTSPLIT' and self.current_time_ms != 0:
            time_delta = self.current_time_ms - self.gold_time_ms
            time_delta_str = format_wall_clock_from_ms(time_delta)

            if time_delta >= 0:
                time_delta_str = "+" + time_delta_str

            if self.current_time_ms < self.gold_time_ms:
                self.time_label.setText(format_wall_clock_from_ms(self.current_time_ms))
                self.time_label.setStyleSheet('color: gold;')

            elif self.current_time_ms >= self.gold_time_ms:
                self.time_label.setStyleSheet('color: red;')

            else:
                self.time_label.setStyleSheet('color: green;')

            # as a test put the current time as the saved time of the split
            self.delta_label.setText(time_delta_str)

            if time_delta <= 0:
                self.delta_label.setStyleSheet('color: gold;')
            else:
                self.delta_label.setStyleSheet('color: red;')

        elif event == 'RESET':
            self.reset_split()

        elif event == 'STOP':
            self.finalize_split()
