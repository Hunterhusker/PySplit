from PySide6.QtWidgets import QWidget, QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot, Signal


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

        self.layout = QHBoxLayout()

        # create the labels we need
        self.split_name_label = QLabel(split_name, self)
        self.split_saved_time_label = QLabel(str(best_time_ms), self)
        self.over_under_time_label = QLabel('Test', self)

        # add them to the layout
        self.layout.addWidget(self.split_name_label)
        self.layout.addWidget(self.over_under_time_label)
        self.layout.addWidget(self.split_saved_time_label)

        # align the items in the layout
        self.layout.setAlignment(self.split_name_label, Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.setAlignment(self.over_under_time_label, Qt.AlignCenter)
        self.layout.setAlignment(self.split_saved_time_label, Qt.AlignRight | Qt.AlignVCenter)

        # set this as a little lighter grey so they look nice
        self.setStyleSheet("""
            background-color: #323232;
        """)

        self.setLayout(self.layout)  # set the layout on the frame

    @Slot(int)
    def update_split(self, curr_time_ms: int):
        """
        A method to update the current split to represent the current time taken

        Args:
            curr_time_ms: (int) the current amount of time taken up to this point (from start of timer to now, not start of split)
        """
        pass

    @Slot()
    def export_data(self):
        """
        A method to turn the data for this single split into JSON and output it as a dictionary

        Returns:
            (dict[str, any]): A dictionary of this split's data as valid JSON that we can store in a splits file
        """
        pass
