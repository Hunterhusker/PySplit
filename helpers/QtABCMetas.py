"""
A module to contain all the ABC metaclasses we had to build so that they do not need to be redefined
"""
from abc import ABCMeta
from PySide6.QtWidgets import QWidget, QFrame


class QWidgetABCMeta(type(QWidget), ABCMeta):
    ...


class QFrameABCMeta(type(QFrame), ABCMeta):
    ...
