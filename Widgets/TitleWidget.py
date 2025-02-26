from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame


class TitleWidget(QFrame):
    def __init__(self, title, subtitle):
        super().__init__()
        self.layout = QVBoxLayout()

        self.TitleLabel = QLabel(title, self)
        self.TitleLabel.setObjectName('TitleLabel')

        self.SubtitleLabel = QLabel(subtitle, self)
        self.SubtitleLabel.setObjectName('SubLabel')

        self.layout.addWidget(self.TitleLabel)
        self.layout.addWidget(self.SubtitleLabel)

        self.attemptCounterHBox = QHBoxLayout()

        self.triesTodayLabel = QLabel('0', self)
        self.triesTodayLabel.setObjectName('triesTodayLabel')

        self.triesTotalLabel = QLabel('10', self)
        self.triesTotalLabel.setObjectName('triesTotalLabel')

        self.attemptCounterHBox.addWidget(self.triesTodayLabel)
        self.attemptCounterHBox.addWidget(self.triesTotalLabel)

        self.layout.addLayout(self.attemptCounterHBox)

        self.setObjectName('TitleFrame')
        self.setStyleSheet("""
            #TitleFrame {
                border-bottom: 1px solid white;
                border-top: none;
                border-left: none;
                border-right: none;
            }

            QLabel {
                font-family: "Chakra Petch;
            }

            #TitleLabel {
                qproperty-alignment: AlignCenter;
                color: white;
                font-size: 14px;
            }

            #SubLabel {
                qproperty-alignment: AlignCenter;
                color: white;
                font-size: 10px;
            }
            
            #triesTodayLabel {
                qproperty-alignment: AlignLeft;
                font-size: 12px;
            }
            
            #triesTotalLabel {
                qproperty-alignment: AlignRight;
                font-size: 12px;
            }
        """)

        self.setLayout(self.layout)
