from PySide6.QtCore import Slot, Signal, QObject
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

    def parse_settings(self):
        with open(self.filePath, 'r') as f:
            file_contents = f.read()

        settings = json.loads(file_contents)
        self.settings = settings  # also save it here so we can reference it and update it later?

        self.settings_loaded.emit(settings)  # emit the load so that things can subscribe to the loading event

    def write_settings(self, settingsDict):
        with open(self.filePath, 'w') as f:
            f.write(settingsDict)
