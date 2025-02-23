from PySide6.QtCore import Slot, Signal, QThread, QObject
import sys
import json


class SettingsParser(QObject):
    """
    Controls the settings file so that user configurations can persist
    """
    settings_loaded = Signal(dict)

    def __init__(self, filePath):
        super().__init__()

        self.filePath = filePath
        self.settings = {}

    def parseSettings(self):
        settings = {}

        with open(self.filePath) as f:
            file_contents = f.read()

        settings = json.loads(file_contents)
        self.settings = settings  # also save it here so we can reference it and update it later?

        print(self.settings)  # temp print of the settings we loaded

        self.settings_loaded.emit(settings)  # emit the load so that things can subscribe to the loading event

    def write_settings(self, settingsDict):
        ...
