from PySide6.QtCore import QObject, Signal

from Configurator.SettingsParser import SettingsParser


class Configurator(QObject):
    Configure = Signal(str, dict)  # emit a signal with the configuration to change

    def __init__(self, filePath: str):
        # the configurator will need to be able to read settings in for us
        self.settingsParser = SettingsParser(filePath)
        self.settingsParser.parse_settings()  # on initial creation we should read the settings and publish them

