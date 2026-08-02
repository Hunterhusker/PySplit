from PySide6.QtCore import QObject, Signal

from Database.Repository import Repository
from Models.Game import Game
from pathlib import Path

from Settings.Settings import Settings

class Session(QObject):
    def __init__(self, settings_path: str, parent: Main):
        super().__init__()

        self.settings = Settings(settings_path)
        self.repository = Repository(self.settings.settings['db_path'])
        self.game = self.repository.load_game(1)
