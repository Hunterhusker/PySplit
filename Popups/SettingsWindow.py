from PySide6.QtWidgets import QVBoxLayout, QDialog, QDialogButtonBox, QPushButton, QWidget, QTabWidget
from PySide6.QtCore import Qt

from Popups.ABCSettingTab import ABCSettingTab


class SettingsWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        
        self.dialogButtons = QDialogButtonBox()
        self.dialogButtons.addButton(QDialogButtonBox.Ok)
        self.dialogButtons.addButton(QDialogButtonBox.Apply)
        self.dialogButtons.addButton(QDialogButtonBox.Cancel)

        for button in self.dialogButtons.buttons():
            button.setFixedSize(80, 25)
            button.setAutoDefault(False)
            button.setDefault(False)

        self.dialogButtons.clicked.connect(self.button_event)

        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.dialogButtons)

        self.setLayout(self.layout)
        self.setWindowTitle('Settings')

    def apply_settings(self):
        """
        Applies the settings to the application, since each page will know what to emit
        """
        # get the currently open widget
        currWidget = self.tabs.currentWidget()

        currWidget.apply()  # and have it apply its changes!

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Ignore Return/Enter to prevent dialog accept
            event.ignore()
        else:
            super().keyPressEvent(event)

    def button_event(self, button: QPushButton):
        role = self.dialogButtons.buttonRole(button)

        if role == QDialogButtonBox.AcceptRole:
            self.apply_settings()  # apply as normal
            self.accept()  # accept the changes lol

        elif role == QDialogButtonBox.RejectRole:
            self.reject()

        elif role == QDialogButtonBox.ApplyRole:
            self.apply_settings()

    def add_tab(self, tab_widget: ABCSettingTab, name: str):
        """
        Adds the provided tab to the end of the tab list. Must provide an ABCSettingsTab so that it has the required structure.
        Args:
            tab_widget: (ABCSettingsTab) the settings popup window to add
            name: (str) the name of the tab
        """
        self.tabs.addTab(tab_widget, name)
