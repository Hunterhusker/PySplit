from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout, QFrame
from PySide6.QtCore import Slot, Qt

from helpers.TimerFormat import format_wall_clock_from_ms


class TimerWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.MainTimerLabel = QLabel("00.000", self)
        self.MainTimerLabel.setObjectName('TimeLabel')
        self.MainTimerLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addStretch(0)
        self.layout.addWidget(self.MainTimerLabel)
        self.layout.addStretch(0)

        self.layout.setAlignment(self.MainTimerLabel, Qt.AlignRight)

        self.setObjectName('TimeFrame')
        self.setStyleSheet("""
            #TimeFrame {
                border-bottom: 1px solid #bbbbbb;
                border-top: 1px solid #bbbbbb;
                border-left: none;
                border-right: none;
            }
            
            #TimeLabel {
                border-bottom: none;
                border-top: none;
                border-left: none;
                border-right: none;
            }
        """)

        self.setLayout(self.layout)

    @Slot(int)
    def update_time(self, time: int):
        timer_string = format_wall_clock_from_ms(time)

        self.MainTimerLabel.setText(timer_string)
