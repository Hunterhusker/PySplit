from PySide6.QtCore import QObject, Signal
import json

from Styling.Style.styleBuilder import StyleBuilder


class Configurator(QObject):
    Configure = Signal(dict)  # emit the settings

    def __init__(self, settings_file_path: str):
        super().__init__()
        self.settings_file_path = settings_file_path

        # read and load the settings for the base program
        with open(self.settings_file_path, 'r') as f:
            settings_data = f.read()
            self.settings = json.loads(settings_data)

        # the configurator has a style builder, since it doesn't need to know how to build the styles, just how configure and pass style updates along to the configured
        self.style = StyleBuilder(self.settings['style_path'], self.settings['var_path'])

    def write_settings(self):
        """
        Writes the contents of the current settings to the settings file
        """
        self.style.export_style()
        self.style.export_vars()

        with open(self.settings_file_path, 'w') as f:
            f.write(json.dumps(self.settings, indent=4))

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
