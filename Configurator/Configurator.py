from PySide6.QtCore import QObject, Signal
import json


class Configurator(QObject):
    Configure = Signal(dict)  # emit the settings when

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

        self.settings = {}  # define it here so that pycharm knows to intellisense it

        self.read_settings()

    def read_settings(self):
        """
        Read in the settings as JSON file to the internal settings dictionary
        """
        with open(self.file_path, 'r') as f:
            file_contents = f.read()

        settings = json.loads(file_contents)
        self.settings = settings  # also save it here so we can reference it and update it later?

        self.Configure.emit(self.settings)  # send the settings update

    def write_settings(self):
        """
        Writes the contents of the current settings to the settings file
        """
        with open(self.file_path, 'w') as f:
            f.write(self.settings)

    def update_setting(self, key: str, settings: dict):
        """


        Args:
            key:
            settings:
        """
        pass
