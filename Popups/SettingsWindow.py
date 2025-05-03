from PySide6.QtWidgets import QVBoxLayout, QDialog, QDialogButtonBox, QPushButton, QWidget, QTabWidget
from PySide6.QtCore import Qt

from Popups.AssignButtonsTab import AssignButtonsTab
from Popups.SplitsTab import SplitsTab
from Popups.StyleTab import StyleTab


class SettingsWindow(QDialog):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        # create the tabs here before we add them, and give them a link to main
        self.keyWidget = AssignButtonsTab(mainWindow=parent)
        self.styleWidget = StyleTab(mainWindow=parent)
        self.splitsWidget = SplitsTab(mainWindow=parent)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.styleWidget, 'Style')
        self.tabs.addTab(self.keyWidget, 'Key Bindings')
        self.tabs.addTab(self.splitsWidget, 'Splits')

        # set up our standard dialog buttons
        self.dialogButtons = QDialogButtonBox()

        # create buttons for the button dialog
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
