"""
This is a listener that listens to listeners so that we only need to bring one listener into any object to take input in various forms
"""
from PySide6.QtCore import Slot, Signal

from abc import ABC
from Listeners.ABCListener import ABCListener, ABCListenedObject


class AggregateListener(ABCListener, ABC):
    source = None
    event_object = None
    listeners = {}

    def __init__(self, listeners: list[ABCListener] = None):
        super().__init__()

        if listeners is not None:
            for listener in listeners:
                self.add_listener(listener)

        self.listening = False

    def listen(self):
        self.listening = True
        for listener in self.listeners:
            self.listeners[listener].listen()  # this one has to be async, or we'll break a lot here

    @Slot(object)
    def on_input_event(self, input_event):
        if self.listening:
            self.on_event.emit(input_event)

    @Slot()
    def pause_listening(self):
        self.listening = False

    @Slot()
    def resume_listening(self):
        self.listening = True

    @Slot()
    def quit(self):
        self.listening = False

        for listener in self.listeners:
            self.listeners[listener].quit()

    def event_object_from_dict(self, event_dict: dict[str, str]):
        source = event_dict['source']
        listener = self.listeners[source]
        return listener.event_type().from_dict(event_dict)

    @property
    def source(self):
        return 'all'  # we have no one source as we are the aggregator

    def add_listener(self, listener: ABCListener):
        key = listener.source

        self.listeners[key] = listener
        listener.on_event.connect(self.on_input_event)

    def remove_listener(self, listener: ABCListener):
        key = listener.source

        if key in self.listeners.keys():
            self.listeners[key].quit()
            self.on_event.disconnect(listener.on_input_event)
            del self.listeners[key]
