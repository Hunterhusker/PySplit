from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QPushButton, QMessageBox, QFrame, QWidget
from PySide6.QtCore import Slot, Signal, Qt


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Settings')

        self.mainLayout = QHBoxLayout()

        self.setLayout(self.mainLayout)
