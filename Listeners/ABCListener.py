from abc import abstractmethod, ABCMeta, ABC
from PySide6.QtCore import QObject, Signal, Slot
from typing import ClassVar


class ABCQObjectMeta(type(QObject), ABCMeta):
    """
    A generic QObject Meta Class that we can use to make Custom QObject templates
    """
    ...


class ABCListener(QObject, ABC, metaclass=ABCQObjectMeta):
    """
    An abstract object that we can define a template for all listeners for
    """
    on_event = Signal(object)  # this is the way that our listeners broadcast an event, the on_press should probably emit this!

    listening = False
    event_type = type(None)
    _source = None  # fallback for the _source value check

    @abstractmethod
    def listen(self):
        ...

    @abstractmethod
    def on_input_event(self, event):
        """
        This is the thing that does the reacting to the event and passes it along to the subscribers
        Args:
            event: (object) how the event comes in to this listener

        emits:
            on_event: The signal to pass the events down the line
        """
        ...

    @Slot()
    @abstractmethod
    def pause_listening(self):
        ...

    @Slot()
    @abstractmethod
    def resume_listening(self):
        ...

    @Slot()
    @abstractmethod
    def quit(self):
        ...

    @abstractmethod
    def event_object_from_dict(self, event_dict: dict[str, str]):
        ...

    @property
    @abstractmethod
    def source(self):
        ...


class ABCListenedObject(ABC):
    """
    The thing that our implementations of these abstract listeners must output as what their listened event saw
    """
    @abstractmethod
    def __init__(self, obj):  # takes in an object and creates the source, type, and value strings for this thing
        ...

    @abstractmethod
    def __eq__(self, other):
        ...

    @abstractmethod
    def __str__(self):
        ...

    @abstractmethod
    def __repr__(self):
        ...

    @abstractmethod
    def __hash__(self):  # needed
        ...

    @abstractmethod
    def to_dict(self):
        ...

    @classmethod
    @abstractmethod
    def from_dict(self):
        ...
