from abc import abstractmethod, ABC, ABCMeta
from PySide6.QtWidgets import QWidget


class WidgetABCMeta(type(QWidget), ABCMeta):
    pass


class ABCSettingTab(QWidget, metaclass=WidgetABCMeta):
    """
    Just an abstract base class to use to make sure all our tabs have some set methods we can call from the settings dialog
    """
    @abstractmethod
    def apply(self):
        """
        A method to take the settings defined on the tab and apply it to the Main widget

        Returns:
            None
        """
        ...
