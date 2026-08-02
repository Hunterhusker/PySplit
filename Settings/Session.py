from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from Database.Repository import Repository
from Settings.Settings import Settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main


class Session(QObject):
    def __init__(self, settings_path: str, parent: "Main"):
        super().__init__()

        self.parent = parent

        self.settings = Settings(settings_path)
        self.repository = Repository(self.settings.settings['db_path'])
        self.game = self.repository.load_game(1)

    def open_save_run_dialog(self):
        """
        Opens a save dialog to save the run information
        """
        save_box = QMessageBox(self.parent)
        save_box.setWindowTitle("Save Results?")
        save_box.setText("Do you want to save the results of your last run?")
        save_box.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        save_box.setIcon(QMessageBox.Icon.Question)

        save_box.button(QMessageBox.StandardButton.No).setMinimumSize(75, 25)
        save_box.button(QMessageBox.StandardButton.Yes).setMinimumSize(75, 25)

        result = save_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.repository.save_run(self.game)
