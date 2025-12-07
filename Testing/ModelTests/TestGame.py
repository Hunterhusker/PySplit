"""
A completely useless test file that let me play with unittest and mock to learn them more before I touched something important
"""
import Models.Game
import unittest
from unittest.mock import patch, mock_open


TEST_GAME_JSON_STRING = """{
    "title": "TEST",
    "sub_title": "SUBTEST",
    "lifetime_attempts": 1,
    "session_attempts": 0,
    "display_pb": true,
    "splits": [
        {
            "split_name": "test_0",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        },
        {
            "split_name": "test_1",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        },
        {
            "split_name": "test_2",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        }
    ]
}"""

TEST_GAME_JSON_DICTIONARY = {
    "title": "TEST",
    "sub_title": "SUBTEST",
    "lifetime_attempts": 1,
    "session_attempts": 0,
    "display_pb": True,
    "splits": [
        {
            "split_name": "test_0",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        },
        {
            "split_name": "test_1",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        },
        {
            "split_name": "test_2",
            "pb_time_ms": 0,
            "pb_segment_ms": 1,
            "gold_segment_ms": 2
        }
    ]
}


class TestGame(unittest.TestCase):
    def test_game_from_json_str(self):
        game = Models.Game.Game.from_json_str(TEST_GAME_JSON_STRING)

        self.assertEqual(len(game.splits), 3, 'An unexpected number of splits were created for the test game config!')

        self.assertEqual(game.title, 'TEST', 'The title does not match the one in the example json.')
        self.assertEqual(game.sub_title, 'SUBTEST', 'The title does not match the one in the example json.')

        self.assertEqual(game.lifetime_attempts, 1, 'The lifetime attempts does not match the one in the example json.')
        self.assertEqual(game.session_attempts, 0, 'The session attempts does not match the one in the example json.')

        gold_total = 0
        pb_total = 0

        for i in range(0, len(game.splits)):
            curr = game.splits[i]

            self.assertEqual(curr.split_name, f'test_{i}', f'The split at index {i} on the test game loaded from json has the incorrect name: "{curr.split_name}".')
            self.assertEqual(curr.pb_time_ms, 0, f'The split at index {i} has the incorrect pb time in milliseconds of {curr.pb_time_ms}.')
            self.assertEqual(curr.pb_segment_ms, 1, f'The split at index {i} has the incorrect pb segment time in milliseconds of {curr.pb_segment_ms}.')
            self.assertEqual(curr.gold_segment_ms, 2, f'The split at index {i} has the incorrect gold segment time in milliseconds of {curr.gold_segment_ms}.')

            # accumulate the totals
            pb_total += curr.pb_segment_ms
            gold_total += curr.gold_segment_ms

            self.assertEqual(curr.pb_segment_total_ms, pb_total, f'The accumulated value for pbs up to split {i} was {curr.pb_segment_total_ms} but should have been {pb_total}!')
            self.assertEqual(curr.gold_segment_total_ms, gold_total, f'The accumulated value for golds up to split {i} was {curr.gold_segment_total_ms} but should have been {gold_total}!')

    @patch('builtins.open', new_callable=mock_open, read_data=TEST_GAME_JSON_STRING)
    def test_game_from_json_file(self, mock_file):
        game = Models.Game.Game.from_json_file('Foo.json')

        self.assertEqual(len(game.splits), 3, 'An unexpected number of splits were created for the test game config!')

        self.assertEqual(game.title, 'TEST', 'The title does not match the one in the example json.')
        self.assertEqual(game.sub_title, 'SUBTEST', 'The title does not match the one in the example json.')

        self.assertEqual(game.lifetime_attempts, 1, 'The lifetime attempts does not match the one in the example json.')
        self.assertEqual(game.session_attempts, 0, 'The session attempts does not match the one in the example json.')

        gold_total = 0
        pb_total = 0

        for i in range(0, len(game.splits)):
            curr = game.splits[i]

            self.assertEqual(curr.split_name, f'test_{i}', f'The split at index {i} on the test game loaded from json has the incorrect name: "{curr.split_name}".')
            self.assertEqual(curr.pb_time_ms, 0, f'The split at index {i} has the incorrect pb time in milliseconds of {curr.pb_time_ms}.')
            self.assertEqual(curr.pb_segment_ms, 1, f'The split at index {i} has the incorrect pb segment time in milliseconds of {curr.pb_segment_ms}.')
            self.assertEqual(curr.gold_segment_ms, 2, f'The split at index {i} has the incorrect gold segment time in milliseconds of {curr.gold_segment_ms}.')

            # accumulate the totals
            pb_total += curr.pb_segment_ms
            gold_total += curr.gold_segment_ms

            self.assertEqual(curr.pb_segment_total_ms, pb_total, f'The accumulated value for pbs up to split {i} was {curr.pb_segment_total_ms} but should have been {pb_total}!')
            self.assertEqual(curr.gold_segment_total_ms, gold_total, f'The accumulated value for golds up to split {i} was {curr.gold_segment_total_ms} but should have been {gold_total}!')

    def test_game_from_json(self):
        game = Models.Game.Game.from_json(TEST_GAME_JSON_DICTIONARY)

        self.assertEqual(len(game.splits), 3, 'An unexpected number of splits were created for the test game config!')

        self.assertEqual(game.title, 'TEST', 'The title does not match the one in the example json.')
        self.assertEqual(game.sub_title, 'SUBTEST', 'The title does not match the one in the example json.')

        self.assertEqual(game.lifetime_attempts, 1, 'The lifetime attempts does not match the one in the example json.')
        self.assertEqual(game.session_attempts, 0, 'The session attempts does not match the one in the example json.')

        gold_total = 0
        pb_total = 0

        for i in range(0, len(game.splits)):
            curr = game.splits[i]

            self.assertEqual(curr.split_name, f'test_{i}', f'The split at index {i} on the test game loaded from json has the incorrect name: "{curr.split_name}".')
            self.assertEqual(curr.pb_time_ms, 0, f'The split at index {i} has the incorrect pb time in milliseconds of {curr.pb_time_ms}.')
            self.assertEqual(curr.pb_segment_ms, 1, f'The split at index {i} has the incorrect pb segment time in milliseconds of {curr.pb_segment_ms}.')
            self.assertEqual(curr.gold_segment_ms, 2, f'The split at index {i} has the incorrect gold segment time in milliseconds of {curr.gold_segment_ms}.')

            # accumulate the totals
            pb_total += curr.pb_segment_ms
            gold_total += curr.gold_segment_ms

            self.assertEqual(curr.pb_segment_total_ms, pb_total, f'The accumulated value for pbs up to split {i} was {curr.pb_segment_total_ms} but should have been {pb_total}!')
            self.assertEqual(curr.gold_segment_total_ms, gold_total, f'The accumulated value for golds up to split {i} was {curr.gold_segment_total_ms} but should have been {gold_total}!')

    def test_game_from_dict_to_dict(self):
        game = Models.Game.Game.from_json(TEST_GAME_JSON_DICTIONARY)
        tmp_dictionary = game.to_dict()
        self.assertEqual(tmp_dictionary, TEST_GAME_JSON_DICTIONARY)

    def test_game_from_string_to_json_string(self):
        game = Models.Game.Game.from_json_str(TEST_GAME_JSON_STRING)
        tmp_string = game.to_json()
        self.assertEqual(tmp_string, TEST_GAME_JSON_STRING)

        self.assertEqual(str(game), tmp_string)

    def test_game_from_string_to_dict(self):
        game = Models.Game.Game.from_json_str(TEST_GAME_JSON_STRING)
        tmp_dictionary = game.to_dict()
        self.assertEqual(tmp_dictionary, TEST_GAME_JSON_DICTIONARY)

    def test_game_from_dict_to_json_string(self):
        game = Models.Game.Game.from_json(TEST_GAME_JSON_DICTIONARY)
        tmp_string = game.to_json()
        self.assertEqual(tmp_string, TEST_GAME_JSON_STRING)

        self.assertEqual(str(game), tmp_string)


TEST_SINGLE_SPLIT_DICT = {
    "split_name": "test_0",
    "pb_time_ms": 0,
    "pb_segment_ms": 1,
    "gold_segment_ms": 2
}

TEST_SINGLE_SPLIT_STRING = """{
    "split_name": "test_0",
    "pb_time_ms": 0,
    "pb_segment_ms": 1,
    "gold_segment_ms": 2
}"""


class TestSplits(unittest.TestCase):
    def test_game_split_from_json_str(self):
        self.assertEqual(1, 1)
