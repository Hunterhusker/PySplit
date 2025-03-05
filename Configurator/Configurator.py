from PySide6.QtCore import QObject, Signal

from Configurator.SettingsParser import SettingsParser


class Configurator(QObject):
    StyleConfigure = Signal(str, dict)  # emit a signal with the configuration to change
    InputConfigure = Signal(dict)

    def __init__(self, filePath: str):
        # the configurator will need to be able to read settings in for us
        self.settingsParser = SettingsParser(filePath)
        self.settingsParser.parse_settings()  # on initial creation we should read the settings and publish them

        self.settings = self.settingsParser.settings

    def configure(self):
        self.settingsParser.parse_settings()
        self.settings = self.settingsParser.settings

    def saveConfiguration(self):
        pass
