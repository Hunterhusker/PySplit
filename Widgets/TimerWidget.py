from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Slot

from helpers.TimerFormat import format_wall_clock_from_ms


class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.MainTimerLabel = QLabel("00.000", self)
        self.MainTimerLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self.layout.addWidget(self.MainTimerLabel)

        self.setLayout(self.layout)

    @Slot(int)
    def update_time(self, time: int):
        timer_string = format_wall_clock_from_ms(time)

        self.MainTimerLabel.setText(timer_string)
