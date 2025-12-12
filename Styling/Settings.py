from PySide6.QtCore import QObject, Signal
import json

from Models.Game import Game
from Styling.Style.styleBuilder import StyleBuilder


class Settings(QObject):
    # create some signals we can subscribe our objects to
    SettingsUpdate = Signal()
    InputMapUpdate = Signal()
    StylePathUpdate = Signal()
    GamePathUpdate = Signal()

    def __init__(self, settings_file_path: str):
        super().__init__()
        self.settings_file_path = settings_file_path

        # read and load the settings for the base program
        with open(self.settings_file_path, 'r') as f:
            settings_data = f.read()
            self.settings = json.loads(settings_data)

        self.style_path = self.settings['style_path']
        self.var_path = self.settings['var_path']
        self.game_path = self.settings['game_path']

        # the configurator has a style builder, since it doesn't need to know how to build the styles, just how configure and pass style updates along to the configured
        self.style = StyleBuilder(self.settings['style_path'], self.settings['var_path'])
        self.game = Game.from_json_file(self.settings['game_path'])

    def write_settings(self):
        """
        Writes the contents of the current settings to the settings file
        """
        self.style.export_style()
        self.style.export_vars()

        with open(self.settings_file_path, 'w') as f:
            f.write(json.dumps(self.settings, indent=4))

    def set_inputs(self, input_map):
        self.settings['inputs'] = input_map

        self.InputMapUpdate.emit()

    def get_inputs(self):
        return self.settings.get('inputs', {})