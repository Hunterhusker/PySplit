from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QLineEdit, QScrollArea
from PySide6.QtCore import Slot, Qt
from typing import TYPE_CHECKING

from Popups.ABCSettingTab import ABCSettingTab

if TYPE_CHECKING:
    from Main import Main


class SplitsTab(ABCSettingTab):
    """
    A tab to CRUD your splits
    """
    def __init__(self, mainWindow: 'Main' = None):
        super().__init__(parent=mainWindow)
        ...

    def apply(self):
        pass
