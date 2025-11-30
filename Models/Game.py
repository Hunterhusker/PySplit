from __future__ import annotations

import json
from PySide6.QtCore import Signal, QObject


class Game(QObject):
    """A representation of a game and the splits we'd like to track during a run"""
    GameUpdated = Signal(QObject)

    def __init__(self, title: str, sub_title: str, splits: list[Split], lifetime_attempts: int, session_attempts: int, display_pb: bool = True):
        super().__init__()

        self.title = title
        self.sub_title = sub_title
        self.splits = splits
        self.lifetime_attempts = lifetime_attempts
        self.session_attempts = session_attempts
        self.display_pb = display_pb

    @classmethod
    def from_json(cls, json_dict: dict) -> Game:
        """
        Builds a game object from JSON
        Args:
            json_dict: (dict) the JSON representation of the game

        Returns:
            (Game) the game object that was detailed in the JSON
        """
        title = json_dict['title']
        sub_title = json_dict['sub_title']
        lifetime_attempts = json_dict['lifetime_attempts']
        session_attempts = json_dict.get('session_attempts', 0)

        prev_pb_segment_total_ms = 0
        prev_gold_segment_total_ms = 0

        # build the splits from the JSON in the game dictionary
        splits = []
        for split in json_dict['splits']:
            new_split = Split.from_json(split, prev_pb_segment_total_ms, prev_gold_segment_total_ms)

            prev_pb_segment_total_ms = new_split.pb_segment_total_ms
            prev_gold_segment_total_ms = new_split.gold_segment_total_ms

            splits.append(new_split)

        # call the constructor on the data we extracted from the JSON
        return cls(title, sub_title, splits, lifetime_attempts, session_attempts)

    @classmethod
    def from_json_str(cls, json_str: str) -> Game:
        """
        Builds a Game object from a string-JSON of the game
        Args:
            json_str: (str) the JSON that defines the game as a string

        Returns:
            (Game) the Game object that the JSON string defined
        """
        json_dict = json.loads(json_str)
        return cls.from_json(json_dict)

    @classmethod
    def from_json_file(cls, file_path: str) -> Game:
        """
        Read the JSON as a string from a file, and then make it into a Game
        Args:
            file_path: (str) the path to the file containing the JSON for the Game

        Returns:
            (Game) the game object outlined in the JSON file
        """
        with open(file_path, 'r') as f:  # read the JSON string from the file
            data = f.read()

        return cls.from_json_str(data)  # make it with the JSON string in the file

    def update_from_json(self, json_dict: dict) -> Game:
        """
        Updates the game object from JSON
        Args:
            json_dict: (dict) the JSON representation of the game
        """
        self.title = json_dict['title']
        self.sub_title = json_dict['sub_title']
        self.lifetime_attempts = json_dict['lifetime_attempts']
        self.session_attempts = json_dict.get('session_attempts', 0)

        prev_pb_segment_total_ms = 0
        prev_gold_segment_total_ms = 0

        # build the splits from the JSON in the game dictionary
        splits = []
        for split in json_dict['splits']:
            new_split = Split.from_json(split, prev_pb_segment_total_ms, prev_gold_segment_total_ms)

            prev_pb_segment_total_ms = new_split.pb_segment_total_ms
            prev_gold_segment_total_ms = new_split.gold_segment_total_ms

            splits.append(new_split)

        self.splits = splits

    def update_from_str(self, json_str: str) -> Game:
        """
        Builds a Game object from a string-JSON of the game
        Args:
            json_str: (str) the JSON that defines the game as a string

        Returns:
            (Game) the Game object that the JSON string defined
        """
        json_dict = json.loads(json_str)
        self.update_from_json(json_dict)

    def update_from_file(self, file_path: str) -> Game:
        """
        Read the JSON as a string from a file, and then make it into a Game
        Args:
            file_path: (str) the path to the file containing the JSON for the Game

        Returns:
            (Game) the game object outlined in the JSON file
        """
        with open(file_path, 'r') as f:  # read the JSON string from the file
            data = f.read()

        self.update_from_str(data)

    def to_dict(self):
        """
        Builds the Game object into a dictionary for use elsewhere
        Returns:
            (dict) the dictionary that represents the Game object
        """
        splits = []

        # build the splits from their own to_dict() and save it to add as nested dictionaries within this one
        for split in self.splits:
            splits.append(split.to_dict())

        return {
            'title': self.title,
            'sub_title': self.sub_title,
            'lifetime_attempts': self.lifetime_attempts,
            'display_pb': self.display_pb,
            'splits': splits
        }

    def to_json(self):
        """
        Builds a JSON string out of the game object for moving this object around in a human-readable format
        Returns:
            (str) the JSON string representing this Game object
        """
        return json.dumps(self.to_dict(), indent=4)

    def to_json_file(self, file_path: str):
        data = self.to_json()

        with open(file_path, 'w') as f:
            f.write(data)

    def __str__(self):
        """
        Builds a JSON string out of the game object for moving this object around in a human-readable format
        Returns:
            (str) the JSON string representing this Game object
        """
        return self.to_json()

    def add_attempt(self):
        self.session_attempts += 1
        self.GameUpdated.emit(self)


class Split:
    """A class that represents a single split in a speedrun"""
    def __init__(self, split_name: str, pb_time_ms: int, pb_segment_ms: int, gold_segment_ms: int, pb_segment_total_ms: int = 0, gold_segment_total_ms: int = 0):
        self.split_name = split_name
        self.pb_time_ms = pb_time_ms
        self.pb_segment_ms = pb_segment_ms
        self.gold_segment_ms = gold_segment_ms
        self.pb_segment_total_ms = pb_segment_total_ms
        self.gold_segment_total_ms = gold_segment_total_ms

    @classmethod
    def from_json(cls, json_dict: dict, prev_pb_segment_total_ms: int = 0, prev_gold_segment_total_ms: int = 0):
        """
        Makes a single split from the dictionary (aka JSON)
        Args:
            json_dict: (dict) the JSON dictionary representing the split
            prev_pb_segment_total_ms: (int) the total of the previously seen segments pb segment times in ms
            prev_gold_segment_total_ms: (int) the total of the previously seen segments gold segment times in ms

        Returns:
            (Split) the split detailed in the JSON object
        """
        # track the local segment totals
        prev_pb_segment_total_ms += json_dict['pb_segment_ms']
        prev_gold_segment_total_ms += json_dict['gold_segment_ms']

        return cls(json_dict['split_name'], json_dict['pb_time_ms'], json_dict['pb_segment_ms'], json_dict['gold_segment_ms'], prev_pb_segment_total_ms, prev_gold_segment_total_ms)

    @classmethod
    def from_json_str(cls, json_str: str, prev_pb_segment_total_ms: int = 0, prev_gold_segment_total_ms: int = 0):
        """
        Makes a split object from a json string representation
        Args:
            json_str: (str) the string representing the split as JSON as a string
            prev_pb_segment_total_ms: (int) the total of the previously seen segments pb segment times in ms
            prev_gold_segment_total_ms: (int) the total of the previously seen segments gold segment times in ms

        Returns:
            (Split) the Split object that the JSON string represents
        """
        json_dict = json.loads(json_str)
        return cls.from_json(json_dict, prev_pb_segment_total_ms, prev_gold_segment_total_ms)

    def __str__(self):
        """
        Turns the split object into a JSON string
        Returns:
            (str) the JSON object as a string
        """
        return self.to_json()

    def to_dict(self):
        """
        Makes a dictionary out of the Split
        Returns:
            (dict): the dictionary that has all the data for this object
        """
        return {
            'split_name': self.split_name,
            'pb_time_ms': self.pb_time_ms,
            'pb_segment_ms': self.pb_segment_ms,
            'gold_segment_ms': self.gold_segment_ms
        }

    def to_json(self):
        """
        Turns the split object into a JSON string
        Returns:
            (str) the JSON object as a string
        """
        return json.dumps(self.to_dict(), indent=4)
