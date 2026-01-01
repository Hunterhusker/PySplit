from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout, QFrame
from PySide6.QtCore import Slot

from helpers.TimerFormat import format_wall_clock_from_ms


class TimeStatsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.sob_label = QLabel("FOO", self)

        # add everything to the layout
        self.layout.addWidget(self.sob_label)

        # finish up and set everything properly
        self.setLayout(self.layout)
        self.setObjectName("TimerStatsWidget")
