import json
import sqlite3


class Splits:
    splits = None

    def __init__(self):
        self.splits = dict()

    def read_splits_from_file(file_path: str):
        """
        Reads the splits file at the given file path into a splits obj

        Args:
            file_path:

        Returns:

        """
        with open(file_path) as f:



if __name__ == '__main__':
    con = sqlite3.connect("conf/sqlite/test.db")

    cur = con.cursor()

    
