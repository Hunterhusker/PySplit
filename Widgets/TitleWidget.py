from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QSizePolicy, QFrame


class TitleWidget(QFrame):
    def __init__(self, title, subtitle):
        super().__init__()
        locLayout = QVBoxLayout()

        self.TitleLabel = QLabel(title, self)
        self.TitleLabel.setObjectName('TitleLabel')

        self.SubtitleLabel = QLabel(subtitle, self)
        self.SubtitleLabel.setObjectName('SubLabel')

        locLayout.addWidget(self.TitleLabel)
        locLayout.addWidget(self.SubtitleLabel)

        self.setObjectName('TitleFrame')
        self.setStyleSheet("""
            #TitleFrame { 
                border-bottom: 1px solid white; 
                border-top: none; 
                border-left: none; 
                border-right: none; 
            }

            QLabel {
                qproperty-alignment: AlignCenter;
                font-family: Chakra Petch Medium;
            }

            #TitleLabel {
                color: white;
                font-size: 14px;
            }

            #SubLabel {
                color: white;
                font-size: 10px;
            }
        """)

        self.setLayout(locLayout)
