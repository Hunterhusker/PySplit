from abc import abstractmethod, ABCMeta, ABC
from PySide6.QtCore import QObject, Slot


class ABCQObjectMeta(type(QObject), ABCMeta):
    """
    A generic QObject Meta Class that we can use to make Custom QObject templates
    """
    ...


class ABCListener(QObject, ABC, metaclass=ABCQObjectMeta):
    """
    An abstract object that we can define a template for all listeners for
    """
    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def listen(self):
        ...

    @abstractmethod
    def on_input_event(self, key):
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
    def on_press(self):  # a getter for the signal
        ...

    @abstractmethod
    def obj_to_str(self, obj):
        ...

    @abstractmethod
    def str_to_obj(self, obj_str):
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
    def serialize(self):
        ...

    @abstractmethod
    def deserialize(self):
        ...
