from PySide6.QtCore import QObject, Signal
import json

from Styling.Style.styleBuilder import StyleBuilder


class Configurator(QObject):
    Configure = Signal(dict)  # emit the settings

    def __init__(self, settings_file_path: str, game_settings_file_path: str = None):
        super().__init__()
        self.settings_file_path = settings_file_path
        self.game_settings_file_path = game_settings_file_path

        # read and load the settings for the base program
        with open(self.settings_file_path, 'r') as f:
            settings_data = f.read()
            self.settings = json.loads(settings_data)

        if game_settings_file_path is not None:  # only if they define one
            # read in the settings for this particular game
            with open(self.game_settings_file_path, 'r') as f:
                game_data = f.read()
                self.game_settings = json.loads(game_data)

        else:
            self.game_settings = {}

        # the configurator has a style builder, since it doesn't need to know how to build the styles, just how configure and pass style updates along to the configured
        self.style = StyleBuilder(self.settings['style_path'], self.settings['var_path'])

    def write_settings(self):
        """
        Writes the contents of the current settings to the settings file
        """
        with open(self.settings_file_path, 'w') as f:
            f.write(self.settings)

    def update_setting(self, key: str, value: any):
        """
        Updates the settings for a key with the provided value

        Args:
            key:
            value:
        """
        pass

    def get_setting(self, key: str):
        ...
