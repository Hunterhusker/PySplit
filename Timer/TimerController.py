from PySide6.QtCore import QObject, Slot, Signal
import json

from Listeners.ABCListener import ABCListener
from Listeners.KeyboardListener import KeyPressObject


class TimerController(QObject):
    """
    A class that takes in input events and output timer control events
    """
    ControlEvent = Signal(str)

    def __init__(self, Listeners: list[ABCListener], event_map):
        super().__init__()  # do the basic init

        # save our listeners to a list just in case
        self.event_map = dict()
        self.listeners = []
        self.listening = True

        # subscribe to all the on_press events from the different listeners
        self.add_listeners(Listeners)

        # find the format of the input map
        if type(event_map) == dict:
            self.update_mapping(event_map)
        else:
            # update the input mapping
            self.import_mapping(event_map)

    @Slot(object)
    def input_event(self, event_obj):
        if event_obj in self.event_map:  # if the input was mapped, then we should trigger off it
            event = self.event_map[event_obj]

            if event == 'LOCK':  # the lock event is local and should be pressable w/o the listening turned on
                self.toggle_listening()
            elif self.listening:  # as long as we're listening then we should do this (and if it is not the lock command as that is local to the controller)
                self.ControlEvent.emit(event)

    def update_mapping(self, event_map: dict[KeyPressObject, str]):
        """
        Takes in a mapping of objects that an added listener can output and maps them to a string that the timer can read for control commands
            - will completely overwrite the

        Args:
            event_map: (dict[KeyPressObject, str]) A dictionary keyed by the output the listener will give when it sees this
        """
        self.event_map = event_map

    def get_mapping(self):
        """
        Gets the current mapping dictionary and translates it to what it would take to set it to that in the set_mapping() method

        Returns:
            (dict{object: str}): The object that would set this controller to listen the way that it currently is
        """
        return self.event_map

    def add_mapping(self, key, value):
        """
        Adds the key value pair to the event map and returns the updated list

        Args:
            key: (object) the thing you would like to trigger this event
            value: (str) the string that the controller should send to the timer

        Returns:
            (dict{str: object}): The current event map on this object
        """
        self.event_map[key] = value

        return self.event_map

    def remove_mapping(self, key):
        """
        Removes a mapping regardless of the value from the event map, these events will stop firing

        Args:
            key: (object) the key you would like to unmap

        Returns:
            (dict{object: str}) the updated event map that is used to control the timer
        """
        if key in self.event_map:
            del self.event_map[key]

        return self.event_map  # return what is left of the map

    def export_mapping(self) -> str:
        """
        Exports the current input config as a JSON string that we can store and load in later

        Returns:
            (dict[str, str]) : The JSON string representing the current inputs
        """
        export_list = []

        for mapping in self.event_map:
            tmp = mapping.serialize()  # our mapped objs must be ABCListenedObjects so we can do this
            tmp['event'] = self.event_map[mapping]

            export_list.append(tmp)

        return export_list

    def import_mapping(self, serialized_event_map: list[dict[str, str]]):
        """
        For importing the serialized event map data, not the built and ready event map
        Args:
            serialized_event_map: (list[dict[str, str]]) the serialized version of the event map, more than likely loaded from the file
        """
        new_map = {}

        for mapping in serialized_event_map:
            tmp = KeyPressObject().deserialize(mapping)

            if tmp.value == '':  # deal with unbound keys
                tmp.value = None

            new_map[tmp] = mapping['event']

        self.event_map = new_map

    def add_listener(self, listener: ABCListener):
        """
        Adds a single listener and starts listening to it

        Args:
            listener: (ABCListener) The listener to add to the list and begin listening to
        """
        self.listeners.append(listener)  # save it for later

        listener.on_press.connect(self.input_event)  # start listening to events from this

    def add_listeners(self, listeners: list[ABCListener]):
        """
        Adds a whole list of listeners to the controller and listens to them all

        Args:
            listeners: (list[ABCListener]) the list of listeners to add to this controller
        """
        for listener in listeners:
            self.add_listener(listener)

    def remove_listener(self, listener: ABCListener):
        """
        Removes a listener from the set of listeners that the controller is listening to

        Args:
            listener: (ABCListener) A listener that will emit an on_press signal with user input data that can perform actions
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

            listener.on_press.disconnect(self.input_event)

    def pause_listeners(self):
        if self.listening:
            self.listening = False

    def resume_listeners(self):
        if not self.listening:
            self.listening = True

    @Slot()
    def toggle_listening(self):
        self.listening = not self.listening
