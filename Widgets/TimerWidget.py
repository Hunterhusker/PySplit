from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QFrame
from PySide6.QtCore import Slot, Qt

from helpers.TimerFormat import format_wall_clock_from_ms


class TimerWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.main_timer_label = QLabel("00.000", self)
        self.main_timer_label.setObjectName('TimerLabel')
        self.main_timer_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addStretch(0)
        self.layout.addWidget(self.main_timer_label)
        self.layout.addStretch(0)

        self.layout.setAlignment(self.main_timer_label, Qt.AlignRight)

        self.setObjectName('TimerFrame')

        self.setLayout(self.layout)

    @Slot(int)
    def update_time(self, time: int):
        timer_string = format_wall_clock_from_ms(time)

        self.main_timer_label.setText(timer_string)
