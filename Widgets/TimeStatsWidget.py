from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


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
