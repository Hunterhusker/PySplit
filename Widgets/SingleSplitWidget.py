from PySide6.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot, Signal

from helpers.TimerFormat import format_wall_clock_from_ms


class SingleSplitWidget(QFrame):
    def __init__(self, split_name: str, best_time_ms: int, pb_time_ms: int):
        """
        An initializer to create

        Args:
            split_name:
            best_time_ms:
            pb_time_ms:
        """
        super().__init__()

        # save the variables we will need
        self.split_name = split_name
        self.best_time_ms = best_time_ms
        self.pb_time_ms = pb_time_ms
        self.current_time_ms = 0

        self.layout = QHBoxLayout()

        # create the labels we need
        self.split_name_label = QLabel(split_name, self)
        self.split_saved_time_label = QLabel(format_wall_clock_from_ms(best_time_ms), self)
        self.over_under_time_label = QLabel('', self)

        # add them to the layout
        self.layout.addWidget(self.split_name_label)
        self.layout.addWidget(self.over_under_time_label)
        self.layout.addWidget(self.split_saved_time_label)

        # align the items in the layout
        self.layout.setAlignment(self.split_name_label, Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.setAlignment(self.over_under_time_label, Qt.AlignRight)
        self.layout.setAlignment(self.split_saved_time_label, Qt.AlignRight | Qt.AlignVCenter)

        # set this as a little lighter grey so they look nice
        self.setStyleSheet("""
            background-color: #323232;
            color: #bbbbbb;
        """)

        self.setLayout(self.layout)  # set the layout on the frame

    @Slot(int)
    def update_split(self, curr_time_ms: int):
        """
        A method to update the current split to represent the current time taken

        Args:
            curr_time_ms: (int) the current amount of time taken up to this point (from start of timer to now, not start of split)
        """
        self.current_time_ms = curr_time_ms

        time_delta = self.current_time_ms - self.best_time_ms

        if time_delta >= -1000.0:
            time_delta_str = format_wall_clock_from_ms(time_delta)

            if time_delta >= 0:
                time_delta_str = "+" + time_delta_str

            # as a test put the current time as the saved time of the split
            self.over_under_time_label.setText(time_delta_str)

        else:
            self.over_under_time_label.setText('')

    def reset_split(self):
        """
        Resets the split data to how it would have been when first loaded
        """
        self.over_under_time_label.setText('')  # clear the time delta
        self.split_saved_time_label.setText(format_wall_clock_from_ms(self.best_time_ms))

        self.current_time_ms = 0

    @Slot()
    def export_data(self):
        """
        A method to turn the data for this single split into JSON and output it as a dictionary

        Returns:
            (dict[str, any]): A dictionary of this split's data as valid JSON that we can store in a splits file
        """
        pass

    @Slot(str)
    def handle_control(self, event: str):
        """

        Args:
            event:
        """
        if event == 'STARTSPLIT':
            # update the saved time to the current time
            if self.current_time_ms > 0:
                self.split_saved_time_label.setText(format_wall_clock_from_ms(self.current_time_ms))
