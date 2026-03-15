from __future__ import annotations
import json


class SplitDefinition:
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
