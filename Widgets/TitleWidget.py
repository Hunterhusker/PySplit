from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame


class TitleWidget(QFrame):
    def __init__(self, title, subtitle):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 3)
        self.layout.setSpacing(2)

        self.title_label = QLabel(title, self)
        self.title_label.setObjectName('TitleLabel')

        self.subtitle_label = QLabel(subtitle, self)
        self.subtitle_label.setObjectName('SubLabel')

        self.layout.addWidget(self.title_label)

        self.attempt_counter_hbox = QHBoxLayout()

        self.tries_today_label = QLabel('0', self)
        self.tries_today_label.setObjectName('triesTodayLabel')

        self.tries_total_label = QLabel('10', self)
        self.tries_total_label.setObjectName('triesTotalLabel')

        self.attempt_counter_hbox.addWidget(self.tries_today_label)
        self.attempt_counter_hbox.addWidget(self.subtitle_label)
        self.attempt_counter_hbox.addWidget(self.tries_total_label)

        self.layout.addLayout(self.attempt_counter_hbox)

        self.setObjectName('TitleFrame')

        self.setLayout(self.layout)
