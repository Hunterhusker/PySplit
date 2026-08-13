from __future__ import annotations
import json


# TODO : Make id field nullable and default to null so that we can load from a JSON w/o id fields or DB with id fields
class Split:
    """A class that represents a single split in a speedrun"""
    def __init__(self, id: int, split_name: str, pb_segment_ms: int, gold_segment_ms: int, pb_segment_total_ms: int = 0, gold_segment_total_ms: int = 0):
        self.id = id
        self.split_name = split_name
        self.pb_segment_ms = pb_segment_ms
        self.gold_segment_ms = gold_segment_ms
        self.pb_segment_total_ms = pb_segment_total_ms
        self.gold_segment_total_ms = gold_segment_total_ms
        self.current_segment_ms = None  # all splits should initialize as none, as they haven't been run yet

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

        return cls(
            json_dict.get('id', None),
            json_dict['split_name'],
            json_dict['pb_segment_ms'],
            json_dict['gold_segment_ms'],
            prev_pb_segment_total_ms,
            prev_gold_segment_total_ms
        )

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
            'id': self.id,
            'split_name': self.split_name,
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

    def update_bests(self, is_pb: bool):
        """
        Updates the best split segments
        """
        # if the split was golded, save it
        #print(f'Updating: {self.split_name} w/ curr: {self.current_segment_ms} gold: {self.gold_segment_ms} pb: {self.pb_segment_ms}')

        print(
            f"{self.split_name}: "
            f"current={self.current_segment_ms} "
            f"pb={self.pb_segment_ms} "
            f"pb_total={self.pb_segment_total_ms} "
            f"gold={self.gold_segment_ms} "
            f"gold_total={self.gold_segment_total_ms}"
        )

        if self.current_segment_ms is None:
            return

        if self.current_segment_ms < self.gold_segment_ms:
            self.gold_segment_ms = self.current_segment_ms

        if is_pb:
            self.pb_segment_ms = self.current_segment_ms

        # if self.current_segment_ms is not None and self.current_segment_ms < self.gold_segment_ms:
        #     #print(f'New gold!: {self.current_segment_ms} < {self.gold_segment_ms}')
        #     # update the total while we still know the old gold
        #     self.gold_segment_total_ms -= self.gold_segment_ms
        #     self.gold_segment_total_ms += self.current_segment_ms
        #
        #     # update the gold segment time to the new current segment time
        #     self.gold_segment_ms = self.current_segment_ms
        #
        # if is_pb:  # if this is the PB, then we should save that, doesn't matter if it was better
        #     # update the old PB totals
        #     self.pb_segment_total_ms -= self.pb_segment_ms
        #     self.pb_segment_total_ms += self.current_segment_ms
        #
        #     # update the pb segment time to the new current segment time
        #     self.pb_segment_ms = self.current_segment_ms

        #print(f'Updated: {self.split_name} to curr: {self.current_segment_ms} gold: {self.gold_segment_ms} pb: {self.pb_segment_ms}')
