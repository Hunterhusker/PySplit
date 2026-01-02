from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QFrame
from PySide6.QtCore import Slot, Qt

from Widgets.SplitsWidget import SplitsWidget
from helpers.TimerFormat import format_wall_clock_from_ms


class TimerWidget(QFrame):
    def set_negative(self, state: bool):
        if self._negative == state:
            return

        self._negative = state
        label = self.main_timer_label

        label.setProperty("negative", state)
        label.style().unpolish(label)
        label.style().polish(label)
        label.update()

    def __init__(self, splitsWidget: SplitsWidget):
        super().__init__()

        self.layout = QVBoxLayout()
        self._negative = None
        self._splits_widget = splitsWidget

        self.main_timer_label = QLabel("", self)
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

        if time < 0 and not self._negative and self._splits_widget.started:
            self.set_negative(True)

        elif (self._negative and time >= 0) or not self._splits_widget.started:
            self.set_negative(False)

        self.main_timer_label.setText(timer_string)
