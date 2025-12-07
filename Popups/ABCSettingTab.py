from abc import abstractmethod, ABC
from PySide6.QtWidgets import QWidget
from helpers.QtABCMetas import QWidgetABCMeta


class ABCSettingTab(QWidget, ABC, metaclass=QWidgetABCMeta):
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
