from abc import ABC

from pynput.keyboard import Listener, Key, KeyCode
from PySide6.QtCore import Signal, Slot
from Listeners.ABCListener import ABCListener, ABCListenedObject


class KeyboardListener(ABCListener, ABC):
    """
    Runs a keyboard listener in another thread that uses callbacks to emit our own "key_pressed" event to control the timer
    """
    on_press = Signal(Key)
    listener = None
    listening = None

    def __init__(self):
        super().__init__()
        self.listening = True

    def run(self):
        self.listen()

    def listen(self):
        self.listener = Listener(on_press=self.on_input_event)
        self.listener.daemon = True
        self.listener.start()

    def on_input_event(self, key):
        if self.listening:  # only emit the event if the listener is currently "on"
            self.on_press.emit(KeyPressObject(key))

    @Slot()
    def pause_listening(self):
        if self.listening:
            self.listening = False

    @Slot()
    def resume_listening(self):
        if not self.listening:
            self.listening = True

    @Slot()
    def quit(self):
        """
        Stops the keyboard listener cleanly
        """
        self.listener.stop()


class KeyPressObject(ABCListenedObject):
    def __init__(self, obj: Key = None):
        if obj is not None:
            self.source = 'pynput'
            self.value = key_to_str(obj)
            self.obj = obj

            if isinstance(obj, KeyCode):
                self.type = 'simple'

            else:
                self.type = 'complex'

        else:  # if no obj is there, make it blank I guess
            self.source = ''
            self.value = ''
            self.obj = ''
            self.type = ''

    def __eq__(self, other):
        if isinstance(other, KeyPressObject):
            return self.obj == other.obj
        elif isinstance(other, KeyCode):
            return self.obj.char == other.char
        elif isinstance(other, Key):
            return self.obj.name == other.name

        return False

    def __hash__(self):
        return self.obj.__hash__()

    def __str__(self):
        return f'KeyPressObj({self.value})'

    def __repr__(self):
        return f'KeyPressObj{{\'source\': {self.source}, \'type\': {self.type_str}, \'value\': {self.value}}}'

    def serialize(self) -> dict[str, str]:
        """
        Converts the input object into a dictionary of strings that we can save to a file

        Returns:

        """
        return {
            'source': self.source,
            'type': self.type,
            'value': self.value
        }

    def deserialize(self, obj: dict[str, str]):
        """
        Makes an input obj from the provided serialized data that is what we would expect to have generated that JSON
          - useful for reading in an input from a JSON file and giving back the object that it represents

        Args:
            obj: (dict[str, str]) The serialized data that represents this input object

        Returns:
            (KeyPressObject) : A reference to the thing we just created
        """
        self.source = obj['source']
        self.type = obj['type']
        self.value = obj['value']

        # also get the obj just cause
        self.obj = str_to_key(self.value)

        return self


def key_to_str(key: Key) -> str:
    """
    Takes in a pynput key and returns a string for the key that we can safely display

    Args:
        key: (pynput Key)

    Returns:
        (str): A string representing the key that was pressed
    """
    if isinstance(key, KeyPressObject):
        key_str = key.value

    elif isinstance(key, KeyCode):
        key_str = key.char

    elif isinstance(key, Key):
        key_str = key.name

    else:
        raise TypeError(f'The provided key "{str(key)}" was not one of the supported key types for this Listener!')

    return key_str


def str_to_key(key_str: str) -> Key:
    """
    Converts a string to a key for the pynput library

    Args:
        key_str: (str) the string representing the key itself that we would like to

    Returns:
        (pynput.keyboard.Key): The key that the string represents
    """
    if 'Key.' in key_str:  # remove Key. from the string incase that made it over from a non-standard toStringing
        key_str = key_str.replace('Key.', '')

    if len(key_str) != 1:  # if it is more than one character then it can't be gotten as a char
        try:
            key = getattr(Key, key_str)

            return key

        except AttributeError as e:
            raise AttributeError(f'AttributeError: "{key_str}" is not a char or a special character, thus we cannot parse it')

    else:
        try:
            key = KeyCode.from_char(key_str)

            return key

        except:
            raise AttributeError(f'AttributeError: "{key_str}" is a char, but could not be parsed with pynput.keyboard.KeyCode.from_char(char)!')
