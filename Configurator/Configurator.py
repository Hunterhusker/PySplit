from PySide6.QtCore import QObject, Signal
import json

from Configurator.Style.styleBuilder import StyleBuilder


class Configurator(QObject):
    Configure = Signal(dict)  # emit the settings
    ConfigureGame = Signal(dict)  # emit the game configuration

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

        self.settings = {}  # define it here so that pycharm knows to intellisense it

        self.read_settings()

        # the configurator has a style builder, since it doesn't need to know how to build the styles, just how configure and pass style updates along to the configured
        self.style = StyleBuilder(self.settings['style_path'], self.settings['var_path'])

    def read_settings(self):
        """
        Read in the settings as JSON file to the internal settings dictionary
        """
        with open(self.file_path, 'r') as f:
            file_contents = f.read()

        settings = json.loads(file_contents)

        self.settings = settings  # also save it here so we can reference it and update it later?

    def write_settings(self):
        """
        Writes the contents of the current settings to the settings file
        """
        with open(self.file_path, 'w') as f:
            f.write(self.settings)

    def read_game_settings(self):
        pass

    def write_game_settings(self):
        pass

    def update_setting(self, key: str, settings: dict):
        """


        Args:
            key:
            settings:
        """
        pass
