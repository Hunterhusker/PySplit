from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QDialog, QDialogButtonBox, QPushButton, QMessageBox, \
    QFrame, QWidget, QTabWidget
from PySide6.QtCore import Slot, Signal, Qt


class SettingsWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        tabs = QTabWidget()
        tabs.addTab(TempWidget("One"), "Tab1")
        tabs.addTab(TempWidget("Two"), "Tab2")
        tabs.addTab(TempWidget("Three"), "Tab3")

        # store the tabs for later
        self.tabs = tabs

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)
        self.setWindowTitle('Settings')


class TempWidget(QWidget):
    def __init__(self, text: str = '', parent: QWidget = None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.lbl = QLabel(text, self)

        self.layout.addWidget(self.lbl)

        self.setLayout(self.layout)
